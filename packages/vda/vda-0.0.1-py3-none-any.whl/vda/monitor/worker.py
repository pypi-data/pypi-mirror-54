import time
import os


def worker_func(code_range, interval, ppid, logger):
    while True:
        time.sleep(interval)
        logger.info("worker: %s %d", code_range, interval)
        pid = os.getpid()
        if pid != ppid:
            return
