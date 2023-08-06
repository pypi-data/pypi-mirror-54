import time

from vda.agent.agent import launch_server


def dn_configure(seq, body):
    print("dn_configure enter: %d %s" % (seq, body))
    time.sleep(3)
    ret = ["abc"]
    print("dn_configure exit: %s" % ret)
    return ret


def launch_data_node():
    launch_server("0.0.0.0", 9001, 10, dn_configure)
