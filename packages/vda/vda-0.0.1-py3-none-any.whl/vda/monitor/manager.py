from multiprocessing import Process
import os
import time
import json
import logging
from collections import namedtuple

logger = logging.getLogger(__name__)

Membership = namedtuple("Membership", ["total", "idx"])
CodeRange = namedtuple("CodeRange", ["start", "stop", "length"])


def get_membership(file_path, max_hash_code):
    logger.info("membership file_path: %s", file_path)
    if os.path.isfile(file_path):
        with open(file_path) as f:
            raw = json.load(f)
            membership = Membership(
                int(raw["total"]), int(raw["idx"]))
            logger.info("read mebmership from file: %s", membership)
    else:
        membership = Membership(1, 0)
        logger.info("default membership: %s", membership)
    assert(membership.total < max_hash_code)
    assert(membership.idx < membership.total)
    return membership


def calc_range(node_cnt, start, stop):
    total = stop - start
    per_node = total // node_cnt
    remains = total % node_cnt
    cr_list = []
    prev_stop = start
    for i in range(node_cnt-1):
        cr_start = prev_stop
        cr_stop = cr_start + per_node
        if remains > 0:
            cr_stop += 1
            remains -= 1
        cr = CodeRange(cr_start, cr_stop, cr_stop-cr_start)
        cr_list.append(cr)
        prev_stop = cr_stop
    cr_start = prev_stop
    cr_stop = stop
    cr = CodeRange(cr_start, cr_stop, cr_stop-cr_start)
    cr_list.append(cr)
    return cr_list


def get_cr_list(membership, worker_cnt, max_hash_code):
    cr_list = calc_range(membership.total, 0, max_hash_code)
    cr = cr_list[membership.idx]
    sub_cr_list = calc_range(worker_cnt, cr.start, cr.stop)
    return sub_cr_list


def launch_workers(
        membership_path, worker_cnt, worker_func,
        interval, ppid, max_hash_code):
    logger.info(
        "launch_workers: %s %s %s %d %d %d",
        membership_path, worker_cnt, worker_func,
        interval, ppid, max_hash_code)
    membership = get_membership(membership_path, max_hash_code)
    proc_list = []
    cr_list = get_cr_list(membership, worker_cnt, max_hash_code)
    for cr in cr_list:
        p = Process(target=worker_func, args=(
            cr, interval, ppid, logger), daemon=True)
        p.start()
        proc_list.append(p)
    while True:
        time.sleep(99999)
