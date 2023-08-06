import os
from configparser import ConfigParser

from vda.common.constant import LC_PATH, DEFAULT_CFG_FILE, VDA_CFG_FILE


class VdaConfigParser(ConfigParser):

    def getlist(self, section, option):
        return self.get(section, option).split()

    def getsize(self, section, option):
        val = self.get(section, option)
        count = int(val[:-1])
        unit = val[-1:]
        if unit == "T" or unit == "t":
            return count*1024*1024*1024*1024
        elif unit == "G" or unit == "g":
            return count*1024*1024*1024
        elif unit == "M" or unit == "m":
            return count*1024*1024
        elif unit == "K" or unit == "k":
            return count*1024
        else:
            raise TypeError("invalid unit: %s %s" % (val, unit))

    def gettime(self, section, option):
        val = self.get(section, option)
        count = int(val[:-1])
        unit = val[-1:]
        if unit == "H" or unit == "h":
            return count*3600
        elif unit == "M" or unit == "m":
            return count*60
        elif unit == "S" or unit == "s":
            return count
        else:
            raise TypeError("invalid unit: %s %s" % (val, unit))


def load_cfg():
    cfg = VdaConfigParser()
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    default_path = os.path.join(curr_dir, DEFAULT_CFG_FILE)
    cfg.read(default_path)
    cfg_path = os.path.join(LC_PATH, VDA_CFG_FILE)
    if os.path.isfile(cfg_path):
        cfg.read(cfg_path)
    return cfg


cfg = load_cfg()
