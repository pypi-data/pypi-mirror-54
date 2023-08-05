#!/usr/bin/env python
#
#  Copyright (c) 2019 Red Hat, Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

__all__ = ['ncd_main']

# import system libraries
import signal
import time
import argparse
import copy
import sys
import socket
import os
import logging
import threading
from logging.handlers import RotatingFileHandler
from datetime import datetime

from netcontrold.lib import config
from netcontrold.lib import dataif
from netcontrold.lib import util
from netcontrold.lib import error


class RebalContext(dataif.Context):
    rebal_mode = False
    rebal_tick = 0
    rebal_tick_n = 0
    rebal_stat = {}
    apply_rebal = False


class DebugContext(dataif.Context):
    debug_mode = False


nlog = None


class CtlDThread(util.Thread):

    def __init__(self, eobj):
        util.Thread.__init__(self, eobj)

    def run(self):
        sock_file = config.ncd_socket

        try:
            os.unlink(sock_file)
        except OSError:
            if os.path.exists(sock_file):
                raise

        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

        nlog.info("starting ctld on %s" % sock_file)
        sock.bind(sock_file)
        sock.listen(1)

        while (not self.ncd_shutdown.is_set()):
            conn, client = sock.accept()

            try:
                cmd = conn.recv(16)

                rctx = RebalContext
                dctx = DebugContext

                if cmd == 'CTLD_DEBUG_ON':
                    if not dctx.debug_mode:
                        nlog.info("turning on debug mode ..")
                        dctx.debug_mode = True
                    else:
                        nlog.info("debug mode already on ..!")

                    conn.sendall("CTLD_ACK")

                elif cmd == 'CTLD_DEBUG_OFF':
                    if dctx.debug_mode:
                        nlog.info("turning off debug mode ..")
                        dctx.debug_mode = False
                    else:
                        nlog.info("debug mode already off ..!")

                    conn.sendall("CTLD_ACK")

                elif cmd == 'CTLD_REBAL_ON':
                    if not rctx.rebal_mode:
                        nlog.info("turning on rebalance mode ..")
                        rctx.rebal_mode = True
                    else:
                        nlog.info("rebalance mode already on ..!")

                    conn.sendall("CTLD_ACK")

                elif cmd == 'CTLD_REBAL_OFF':
                    if rctx.rebal_mode:
                        nlog.info("turning off rebalance mode ..")
                        rctx.rebal_mode = False
                    else:
                        nlog.info("rebalance mode already off ..!")

                    conn.sendall("CTLD_ACK")

                elif cmd == 'CTLD_REBAL_CNT':
                    n = 0
                    if rctx.rebal_mode:
                        n = len(rctx.rebal_stat)

                    conn.sendall("CTLD_DATA_ACK %6d" % (len(str(n))))
                    conn.sendall(str(n))

                elif cmd == 'CTLD_STATUS':
                    status = "debug mode:"
                    if dctx.debug_mode:
                        status += " on\n"
                    else:
                        status += " off\n"

                    status += "rebalance mode:"
                    if rctx.rebal_mode:
                        status += " on\n"
                    else:
                        status += " off\n"

                    status += "rebalance events:\n"
                    for i in sorted(rctx.rebal_stat.keys()):
                        status += "%-4s: %s\n" % (i + 1, rctx.rebal_stat[i])

                    conn.sendall("CTLD_DATA_ACK %6d" % (len(status)))
                    conn.sendall(status)

                else:
                    nlog.info("unknown control command %s" % cmd)

            finally:
                conn.close()

        return


def pmd_load(pmd):
    """
    Calculate pmd load.

    Parameters
    ----------
    pmd : object
        Dataif_Pmd object.
    """

    # Given we have samples of rx packtes, processing and idle cpu
    # cycles of a pmd, calculate load on this pmd.
    rx_sum = sum([j - i for i, j in zip(pmd.rx_cyc[:-1], pmd.rx_cyc[1:])])
    idle_sum = sum(
        [j - i for i, j in zip(pmd.idle_cpu_cyc[:-1], pmd.idle_cpu_cyc[1:])])
    proc_sum = sum(
        [j - i for i, j in zip(pmd.proc_cpu_cyc[:-1], pmd.proc_cpu_cyc[1:])])

    try:
        cpp = (idle_sum + proc_sum) / rx_sum
        pcpp = proc_sum / rx_sum
        pmd_load = float((pcpp * 100) / cpp)
    except ZeroDivisionError:
        # When a pmd is really idle and also yet to be picked for
        # rebalancing other rxqs, its rx packets count could still
        # be zero, hence we get zero division exception.
        # It is okay to declare this pmd as idle again.
        pmd_load = 0

    return pmd_load


def update_pmd_load(pmd_map):
    """
    Update pmd for its current load level.

    Parameters
    ----------
    pmd_map : dict
        mapping of pmd id and its Dataif_Pmd object.
    """
    for pmd in pmd_map.values():
        pmd.pmd_load = pmd_load(pmd)

    return None


def rebalance_dryrun_iq(pmd_map):
    """
    Rebalance pmds based on their current load of traffic in it and
    it is just a dry-run. In every iteration of this dry run, we keep
    re-assigning rxqs to suitable pmds, at the same time we use
    actual load on each rxq to reflect the estimated pmd load after
    every optimization.

    To re-pin rxqs, the logic used is to move idle (or less loaded)
    rx queues into idle (or less loaded) pmds so that, busier rxq is
    given more processing cycles by busy pmd.

    Parameters
    ----------
    pmd_map : dict
        mapping of pmd id and its Dataif_Pmd object.
    """

    if len(pmd_map) <= 1:
        nlog.debug("not enough pmds to rebalance ..")
        return pmd_map

    # Calculate current load on every pmd.
    update_pmd_load(pmd_map)

    # Sort pmds in pmd_map based on the rxq load, in descending order.
    # Pick the pmd which is more loaded from one end of the list.
    pmd_load_list = sorted(
        pmd_map.values(), key=lambda o: o.pmd_load, reverse=True)

    # Split list into busy and less loaded.
    bpmd_load_list = []
    ipmd_load_list = []
    for pmd in pmd_load_list:
        # pmd load of above configured threshold
        if pmd.pmd_load > config.ncd_pmd_core_threshold:
            bpmd_load_list.append(pmd)

        # skip pmd when its rxq count is one i.e pmd has just one rxq,
        # and this rxq is already busy (hencs, pmd was busy).
        elif (pmd.count_rxq() == 1 and
              pmd.pmd_load >= config.ncd_pmd_core_threshold):
            continue
        # rest of the pmds are less loaded (or idle).
        else:
            ipmd_load_list.insert(0, pmd)

    ipmd = None
    ipmd_gen = (o for o in ipmd_load_list)

    for pmd in bpmd_load_list:
        # As busy and idles (or less loaded) pmds are identified,
        # move less loaded rxqs from busy pmd into idle pmd.
        for port in pmd.port_map.values():
            # A port under dry-run may be empty now.
            if len(port.rxq_map) == 0:
                continue

            # As we pick one or more rxqs for every port in this pmd,
            # we leave atleast one rxq, not to make this busy pmd as
            # idle again.
            if pmd.count_rxq() <= 1:
                continue

            if not ipmd or (ipmd.numa_id != port.numa_id):
                for ipmd in ipmd_gen:
                    # Current pmd and rebalancing pmd should be in same numa.
                    if (ipmd.numa_id == port.numa_id):
                        break
                else:
                    ipmd_gen = (o for o in ipmd_load_list)

            if not ipmd:
                nlog.debug("no rebalancing pmd on this numa..")
                continue

            # Sort rxqs based on their current load, in ascending order.
            pmd_proc_cyc = sum(pmd.proc_cpu_cyc)
            rxq_load_list = sorted(port.rxq_map.values(),
                                   key=lambda o:
                                   ((sum(o.cpu_cyc) * 100) / pmd_proc_cyc))

            # pick one rxq to rebalance and this was least loaded in this pmd.
            try:
                rxq = rxq_load_list.pop(0)
            except IndexError:
                raise error.ObjConsistencyExc("rxq found empty ..")

            # move this rxq into the rebalancing pmd.
            iport = ipmd.add_port(port.name, id=port.id, numa_id=port.numa_id)
            nlog.info("moving rxq %d (port %s) from pmd %d into idle pmd %d .."
                      % (rxq.id, port.name, pmd.id, ipmd.id))
            irxq = iport.add_rxq(rxq.id)
            assert(iport.numa_id == port.numa_id)

            # Copy cpu cycles of this rxq into its clone in
            # in rebalancing pmd (for dry-run).
            irxq.cpu_cyc = copy.deepcopy(rxq.cpu_cyc)

            # Add cpu cycles of this rxq into processing cycles of
            # the rebalancing pmd, so that its current pmd load
            # level reflects this change.
            for i in range(0, config.ncd_samples_max):
                ipmd.proc_cpu_cyc[i] += irxq.cpu_cyc[i]
                ipmd.idle_cpu_cyc[i] -= irxq.cpu_cyc[i]

            # No more tracking of this rxq in current pmd.
            port.del_rxq(rxq.id)

            # Until dry-run is completed and rebalance completed,
            # this rxq should know its current pmd, even it is
            # with rebalancing pmd. Only then, we can derive cpu
            # usage of this rxq from its current pmd (as we scan
            # data in each sampling interval).
            opmd = rxq.pmd
            oport = opmd.find_port_by_name(port.name)
            oport.rxq_rebalanced[rxq.id] = ipmd.id
            irxq.pmd = opmd

            # Similar updates in original pmd as well.
            for i in range(0, config.ncd_samples_max):
                opmd.proc_cpu_cyc[i] -= irxq.cpu_cyc[i]
                opmd.idle_cpu_cyc[i] += irxq.cpu_cyc[i]

            # check if rebalancing pmd has got enough work.
            update_pmd_load(pmd_map)
            if ipmd.pmd_load >= config.ncd_pmd_core_threshold:
                nlog.info("removing pmd %d from idle pmd list" % ipmd.id)
                ipmd_load_list.remove(ipmd)
                ipmd = None

    return pmd_map


def rebalance_dryrun_rr(pmd_map):
    """
    Rebalance pmds based on their current load of traffic in it and
    it is just a dry-run. In every iteration of this dry run, we keep
    re-assigning rxqs to suitable pmds, at the same time we use
    actual load on each rxq to reflect the estimated pmd load after
    every optimization.

    To re-pin rxqs, the logic used is to round robin rxqs based on
    their load put on pmds.

    Parameters
    ----------
    pmd_map : dict
        mapping of pmd id and its Dataif_Pmd object.
    """

    if len(pmd_map) <= 1:
        nlog.debug("not enough pmds to rebalance ..")
        return pmd_map

    # Calculate current load on every pmd.
    update_pmd_load(pmd_map)

    # Sort pmds in pmd_map based on the id (i.e constant order)
    pmd_list_forward = sorted(pmd_map.values(), key=lambda o: o.id)
    pmd_list_reverse = pmd_list_forward[::-1]
    pmd_list = pmd_list_forward
    idx_forward = True

    # Sort rxqs in across the pmds based on cpu cycles consumed,
    # in ascending order.
    rxq_list = []
    for pmd in pmd_list:
        for port in pmd.port_map.values():
            rxq_list += port.rxq_map.values()

    rxq_load_list = sorted(
        rxq_list, key=lambda o: sum(o.cpu_cyc), reverse=True)

    rpmd = None
    rpmd_gen = (o for o in pmd_list)
    for rxq in rxq_load_list:
        port = rxq.port
        pmd = rxq.pmd

        if len(port.rxq_map) == 0:
            continue

        for rpmd in rpmd_gen:
            # Current pmd and rebalancing pmd should be in same numa.
            if (rpmd.numa_id == port.numa_id):
                break
        else:
            rpmd_gen = (o for o in pmd_list)
            rpmd = None

        if not rpmd:
            nlog.debug("no rebalancing pmd on numa(%d) for port %s rxq %d.."
                       % (port.numa_id, port.name, rxq.id))
            continue

        if pmd_list.index(rpmd) == (len(pmd_list) - 1):
            if idx_forward:
                pmd_list = pmd_list_reverse
                idx_forward = False
            else:
                pmd_list = pmd_list_forward
                idx_forward = False
            rpmd_gen = (o for o in pmd_list)

        if pmd.id == rpmd.id:
            nlog.info("no change needed for rxq %d (port %s) in pmd %d"
                      % (rxq.id, port.name, pmd.id))
            continue

        # move this rxq into the rebalancing pmd.
        rport = rpmd.add_port(port.name, port.id, port.numa_id)
        nlog.info("moving rxq %d (port %s) from pmd %d into pmd %d .."
                  % (rxq.id, port.name, pmd.id, rpmd.id))
        rrxq = rport.add_rxq(rxq.id)
        assert(rport.numa_id == port.numa_id)

        # Copy cpu cycles of this rxq into its clone in
        # in rebalancing pmd (for dry-run).
        rrxq.cpu_cyc = copy.deepcopy(rxq.cpu_cyc)

        # No more tracking of this rxq in current pmd.
        port.del_rxq(rxq.id)

        # Until dry-run is completed and rebalance completed,
        # this rxq should know its current pmd, even it is
        # with rebalancing pmd. Only then, we can derive cpu
        # usage of this rxq from its current pmd (as we scan
        # data in each sampling interval).
        opmd = rxq.pmd
        oport = opmd.find_port_by_name(port.name)
        oport.rxq_rebalanced[rxq.id] = rpmd.id
        rrxq.pmd = opmd

    return pmd_map


def pmd_load_variance(pmd_map):
    """
    Get load variance on a set of pmds.

    Parameters
    ----------
    pmd_map : dict
        mapping of pmd id and its Dataif_Pmd object.
    """
    pmd_load_list = list(map(lambda o: o.pmd_load, pmd_map.values()))
    return util.variance(pmd_load_list)


def pmd_need_rebalance(pmd_map):
    """
    Check whether all the pmds have load below its threshold.

    Parameters
    ----------
    pmd_map : dict
        mapping of pmd id and its Dataif_Pmd object.
    """

    pmd_loaded = 0
    for pmd in pmd_map.values():
        if (pmd.pmd_load >= config.ncd_pmd_core_threshold and
                pmd.count_rxq() > 1):
            nlog.debug("pmd %d is loaded more than %d threshold" %
                       (pmd.id, config.ncd_pmd_core_threshold))
            pmd_loaded += 1

    if (len(pmd_map) > pmd_loaded > 0):
        return True

    return False


def port_drop_ppm(port):
    """
    Return packet drops from the port stats.

    """
    rx_sum = sum([j - i for i, j in zip(port.rx_cyc[:-1], port.rx_cyc[1:])])
    rxd_sum = sum(
        [j - i for i, j in zip(port.rx_drop_cyc[:-1], port.rx_drop_cyc[1:])])
    tx_sum = sum([j - i for i, j in zip(port.tx_cyc[:-1], port.tx_cyc[1:])])
    txd_sum = sum(
        [j - i for i, j in zip(port.tx_drop_cyc[:-1], port.tx_drop_cyc[1:])])

    psum = (rx_sum + tx_sum)
    if psum == 0:
        return 0

    dsum = (rxd_sum + txd_sum)
    return (1000000 * dsum) / psum


def collect_data(n_samples, s_sampling):
    """
    Collect various stats and rxqs mapping of every pmd in the vswitch.

    Parameters
    ----------
    n_samples : int
        number of samples

    s_sampling: int
        sampling interval
    """

    ctx = dataif.Context
    rctx = RebalContext

    # collect samples of pmd and rxq stats.
    for i in range(0, n_samples):
        dataif.get_port_stats()
        dataif.get_pmd_stats(ctx.pmd_map)
        dataif.get_pmd_rxqs(ctx.pmd_map)
        time.sleep(s_sampling)

    update_pmd_load(ctx.pmd_map)
    rctx.rebal_tick += n_samples

    return ctx


def rebalance_switch(pmd_map):
    """
    Issue appropriate actions in vswitch to rebalance.

    Parameters
    ----------
    pmd_map : dict
        mapping of pmd id and its Dataif_Pmd object.
    """

    port_to_pmdq = {}
    numa = 0
    for pmd_id, pmd in pmd_map.items():
        # leave one pmd in every numa as non-isolated.
        if pmd.numa_id == numa:
            numa += 1
            continue

        for port_name, port in pmd.port_map.items():
            if port_name not in port_to_pmdq and len(port.rxq_map) != 0:
                port_to_pmdq[port_name] = ""
            for rxq_id in port.rxq_map:
                port_to_pmdq[port_name] += "%d:%d," % (rxq_id, pmd_id)

    cmd = ""
    for port_name, pmdq in port_to_pmdq.items():
        cmd += "-- set Interface %s other_config:pmd-rxq-affinity=%s " % (
            port_name, pmdq)

    return "ovs-vsctl %s" % cmd


def ncd_kill(signal, frame):
    nlog.critical("Got signal %s, dump current state of PMDs .." % signal)
    nlog.debug(frame.f_locals['ctx'].pmd_map)
    nlog.debug(frame.f_locals['ctx'].port_to_cls)

    raise error.NcdShutdownExc


def ncd_main(argv):
    # input options
    argpobj = argparse.ArgumentParser(
        prog='ncd.py', description='control network load on pmd')

    argpobj.add_argument('-s', '--sample-interval',
                         type=int,
                         default=10,
                         help='seconds between each sampling (default: 10)')

    deb_group = argpobj.add_mutually_exclusive_group()
    reb_group = argpobj.add_mutually_exclusive_group()

    deb_group.add_argument('-d', '--debug',
                           required=False,
                           action='store_true',
                           default=False,
                           help='operate in debug mode',
                           )

    reb_group.add_argument('--debug-cb',
                           type=str,
                           default='ncd_cb_pktdrop',
                           help='debug mode callback '
                                '(default: ncd_cb_pktdrop)')

    reb_group.add_argument('-r', '--rebalance',
                           required=False,
                           action='store_true',
                           default=True,
                           help="operate in rebalance mode",
                           )

    reb_group.add_argument('--rebalance-interval',
                           type=int,
                           default=60,
                           help='seconds between each re-balance '
                                '(default: 60)')

    reb_group.add_argument('--rebalance-n',
                           type=int,
                           default=1,
                           help='rebalance dry-runs at the max (default: 1)')

    reb_group.add_argument('--rebalance-iq',
                           action='store_true',
                           default=False,
                           help='rebalance by idle-queue logic '
                                '(default: False)')

    argpobj.add_argument('-q', '--quiet',
                         action='store_true',
                         default=False,
                         help='no logging in terminal (default: False)')

    argpobj.add_argument('-v', '--verbose',
                         action='store_true',
                         default=False,
                         help='debug logging (default: False)')

    args = argpobj.parse_args(argv)

    # check input to ncd
    ncd_debug = args.debug
    ncd_debug_cb = args.debug_cb
    ncd_rebal = args.rebalance

    if ncd_debug and not util.exists(ncd_debug_cb):
        print("no such program %s exists!" % ncd_debug_cb)
        sys.exit(1)

    # set verbose level
    fh = RotatingFileHandler(config.ncd_log_file,
                             maxBytes=(config.ncd_log_max_KB * 1024),
                             backupCount=config.ncd_log_max_backup_n)

    fh_fmt = logging.Formatter(
        "%(asctime)s|%(name)s|%(levelname)s|%(message)s")
    fh.setFormatter(fh_fmt)
    if args.verbose:
        fh.setLevel(logging.DEBUG)
    else:
        fh.setLevel(logging.INFO)

    ch = logging.StreamHandler(sys.stdout)
    ch_fmt = logging.Formatter("%(message)s")
    ch.setFormatter(ch_fmt)
    ch.setLevel(logging.INFO)

    global nlog
    nlog = logging.getLogger('ncd')
    nlog.setLevel(logging.DEBUG)
    nlog.addHandler(fh)
    if not args.quiet:
        nlog.addHandler(ch)

    ctx = dataif.Context
    ctx.nlog = nlog
    pmd_map = ctx.pmd_map

    # set sampling interval to collect data
    ncd_sample_interval = args.sample_interval

    # set interval between each re-balance
    ncd_rebal_interval = args.rebalance_interval

    # set rebalance dryrun count
    ncd_rebal_n = args.rebalance_n

    # set idle queue rebalance algorithm
    ncd_iq_rebal = args.rebalance_iq

    # set rebalance method.
    if ncd_iq_rebal:
        rebalance_dryrun = rebalance_dryrun_iq
    else:
        # round robin logic to rebalance.
        rebalance_dryrun = rebalance_dryrun_rr

        # restrict only one dry run for rr mode.
        ncd_rebal_n = 1

    # set check point to call rebalance in vswitch
    rctx = RebalContext
    rctx.rebal_tick_n = ncd_rebal_interval / ncd_sample_interval

    # rebalance dryrun iteration
    rebal_i = 0

    if ncd_rebal:
        # adjust length of the samples counter
        config.ncd_samples_max = min(
            ncd_rebal_interval / ncd_sample_interval, config.ncd_samples_max)

        rctx.rebal_mode = True

    # set signal handler to abort ncd
    signal.signal(signal.SIGINT, ncd_kill)
    signal.signal(signal.SIGTERM, ncd_kill)

    dctx = DebugContext
    if ncd_debug:
        dctx.debug_mode = True

    # start ctld thread to monitor control command and dispatch
    # necessary action.
    shutdown_event = threading.Event()
    tobj = CtlDThread(shutdown_event)
    tobj.daemon = True

    try:
        tobj.start()
    except threading.ThreadError:
        nlog.info("failed to start ctld thread ..")
        sys.exit(1)

    # The first sample do not have previous sample to calculate
    # current difference (as we use this later). So, do one extra
    # sampling to over write first sample and rotate left on the
    # samples right away to restore consistency of sample progress.
    collect_data(int(config.ncd_samples_max) + 1, ncd_sample_interval)

    if ncd_rebal:
        if len(pmd_map) < 2:
            nlog.info("required at least two pmds to check rebalance..")
            sys.exit(1)

    good_var = pmd_load_variance(pmd_map)
    nlog.info("initial pmd load variance: %d" % good_var)
    pmd_map_balanced = copy.deepcopy(pmd_map)

    nlog.info("initial pmd load:")
    for pmd_id in sorted(pmd_map.keys()):
        pmd = pmd_map[pmd_id]
        nlog.info("pmd id %d load %d" % (pmd_id, pmd.pmd_load))

    nlog.info("initial port drops:")
    for pname in sorted(ctx.port_to_cls.keys()):
        port = ctx.port_to_cls[pname]
        nlog.info("port %s drop %d ppm" % (port.name, port_drop_ppm(port)))

    # begin rebalance dry run
    while (1):
        try:
            # dry-run only if atleast one pmd over loaded.
            # or, atleast in mid of dry-runs.
            if rctx.rebal_mode:
                if (pmd_need_rebalance(pmd_map) or rebal_i):
                    # dry run on collected stats
                    pmd_map = rebalance_dryrun(pmd_map)
                    rebal_i += 1

            # collect samples of pmd and rxq stats.
            collect_data(config.ncd_samples_max, ncd_sample_interval)

            if dctx.debug_mode and not rebal_i:
                pmd_cb_list = []
                for pname in sorted(ctx.port_to_cls.keys()):
                    port = ctx.port_to_cls[pname]
                    drop = port_drop_ppm(port)
                    if drop > config.ncd_cb_pktdrop_min:
                        nlog.info("port %s drop %d ppm above %d ppm" %
                                  (port.name, drop, config.ncd_cb_pktdrop_min))
                        for pmd_id in sorted(pmd_map.keys()):
                            pmd = pmd_map[pmd_id]
                            if (pmd.find_port_by_name(port.name)):
                                pmd_cb_list.insert(0, pmd_id)

                if (len(pmd_cb_list) > 0):
                    pmds = " ".join(list(map(str, set(pmd_cb_list))))
                    cmd = "%s %s" % (ncd_debug_cb, pmds)
                    nlog.info("executing callback %s" % cmd)
                    data = util.exec_host_command(cmd)
                    nlog.info(data)

            if rctx.rebal_mode:
                cur_var = pmd_load_variance(pmd_map)

            # if no dry-run, go back to collect data again.
            if rctx.rebal_mode and not rebal_i:
                nlog.info("no dryrun done performed. current pmd load:")
                for pmd_id in sorted(pmd_map.keys()):
                    pmd = pmd_map[pmd_id]
                    nlog.info("pmd id %d load %d" % (pmd_id, pmd.pmd_load))

                nlog.info("current pmd load variance: %d" % cur_var)
                nlog.info("current port drops:")
                for pname in sorted(ctx.port_to_cls.keys()):
                    port = ctx.port_to_cls[pname]
                    nlog.info("port %s drop %d ppm" %
                              (port.name, port_drop_ppm(port)))

                continue

            if rctx.rebal_mode and rebal_i:
                # compare previous and current state of pmds.
                nlog.info("pmd load variance: best %d, dry run(%d) %d" %
                          (good_var, rebal_i, cur_var))

                if (cur_var < good_var):
                    diff = (good_var - cur_var) * 100 / good_var
                    if diff > config.ncd_pmd_load_improve_min:
                        good_var = cur_var
                        pmd_map_balanced = copy.deepcopy(pmd_map)
                        rctx.apply_rebal = True

                nlog.info("pmd load in dry run(%d):" % rebal_i)
                for pmd_id in sorted(pmd_map.keys()):
                    pmd = pmd_map[pmd_id]
                    nlog.info("pmd id %d load %d" % (pmd_id, pmd.pmd_load))

                # check if we reached maximum allowable dry-runs.
                if rebal_i < ncd_rebal_n:
                    # continue for more dry runs.
                    continue

                # check if balance state of all pmds is reached
                if rctx.apply_rebal:
                    # check if rebalance call needed really.
                    if (rctx.rebal_tick > rctx.rebal_tick_n):
                        rctx.rebal_tick = 0
                        cmd = rebalance_switch(pmd_map_balanced)
                        rctx.rebal_stat[len(rctx.rebal_stat)] = datetime.now()
                        nlog.info(
                            "vswitch command for current optimization is: %s"
                            % cmd)
                        rctx.apply_rebal = False

                        if (util.exec_host_command(cmd) == 1):
                            nlog.info(
                                "problem running this command.. "
                                "check vswitch!")
                            sys.exit(1)

                        # sleep for few seconds before thrashing current
                        # dry-run
                        nlog.info(
                            "waiting for %d seconds "
                            "before new dry runs begin.."
                            % config.ncd_vsw_wait_min)
                        time.sleep(config.ncd_vsw_wait_min)
                    else:
                        nlog.info("minimum rebalance interval not met!"
                                  " now at %d sec"
                                  % (rctx.rebal_tick * ncd_sample_interval))
                else:
                    nlog.info("no new optimization found ..")

                # reset collected data
                pmd_map.clear()
                ctx.port_to_cls.clear()

                collect_data(config.ncd_samples_max + 1, ncd_sample_interval)

                good_var = pmd_load_variance(pmd_map)
                pmd_map_balanced = copy.deepcopy(pmd_map)
                rebal_i = 0

                nlog.info("dry-run reset. current pmd load:")
                for pmd_id in sorted(pmd_map.keys()):
                    pmd = pmd_map[pmd_id]
                    nlog.info("pmd id %d load %d" % (pmd_id, pmd.pmd_load))

                nlog.info("current pmd load variance: %d" % good_var)
                nlog.info("current port drops:")
                for pname in sorted(ctx.port_to_cls.keys()):
                    port = ctx.port_to_cls[pname]
                    nlog.info("port %s drop %d ppm" %
                              (port.name, port_drop_ppm(port)))

                if dctx.debug_mode and not rebal_i:
                    pmd_cb_list = []
                    for pname in sorted(ctx.port_to_cls.keys()):
                        port = ctx.port_to_cls[pname]
                        drop = port_drop_ppm(port)
                        if drop > config.ncd_cb_pktdrop_min:
                            nlog.info("port %s drop %d ppm above %d ppm" %
                                      (port.name, drop,
                                       config.ncd_cb_pktdrop_min))
                            for pmd_id in sorted(pmd_map.keys()):
                                pmd = pmd_map[pmd_id]
                            if (pmd.find_port_by_name(port.name)):
                                pmd_cb_list.insert(0, pmd_id)

                    if (len(pmd_cb_list) > 0):
                        pmds = " ".join(list(map(str, set(pmd_cb_list))))
                        cmd = "%s %s" % (ncd_debug_cb, pmds)
                        nlog.info("executing callback %s" % cmd)
                        data = util.exec_host_command(cmd)
                        nlog.info(data)

        except error.NcdShutdownExc:
            nlog.info("Exiting NCD ..")
            tobj.ncd_shutdown.set()
            sys.exit(1)

    tobj.join()


if __name__ == "__main__":
    ncd_main(sys.argv[1:])
    sys.exit(0)
