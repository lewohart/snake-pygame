# -*- coding: UTF-8 -*-

import time
import logging
import traceback
import json


class Formatter(object):
    def format(self, record):
        d = {
            "level": record.levelname,
            # can't use "time" as a field name otherwise the whole record
            # is missing from logs.devops.jive.com
            "log_time": time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(record.created)
            ),
            "message": record.getMessage(),
            "name": record.name,
        }
        if record.exc_info:
            d["exception"] = "".join(traceback.format_exception(*record.exc_info))

        # our custom way to pass contextual information
        if hasattr(record, "context"):
            d.update(record.context)
        return json.dumps(d)


def setup_logging(verbose: bool):
    handler = logging.StreamHandler()
    handler.setFormatter(Formatter())
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.DEBUG if verbose else logging.INFO)
