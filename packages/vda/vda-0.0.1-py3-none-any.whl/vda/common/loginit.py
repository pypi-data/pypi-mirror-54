import os
import logging
import logging.config
import json

from vda.common.constant import LC_PATH, LOGGER_CFG_FILE


logger_cfg_path = os.path.join(LC_PATH, LOGGER_CFG_FILE)


def loginit():
    if os.path.isfile(logger_cfg_path):
        with open(logger_cfg_path) as f:
            logger_cfg = json.load(f)
            logging.config.dictConfig(logger_cfg)
