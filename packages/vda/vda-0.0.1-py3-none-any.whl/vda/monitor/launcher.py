import os

from vda.common.constant import MAX_HASH_CODE
from vda.common.configure import cfg
from vda.monitor.manager import launch_workers
from vda.monitor.worker import worker_func


def launch_monitor():
    membership_path = cfg.get("monitor", "membership_path")
    worker_cnt = cfg.getint("monitor", "worker_cnt")
    interval = cfg.gettime("monitor", "monitor_interval")
    ppid = os.getpid()
    launch_workers(
        membership_path, worker_cnt, worker_func,
        interval, ppid, MAX_HASH_CODE)
