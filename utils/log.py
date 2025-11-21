#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   log.py
@Time    :   2024/01/22 20:50:33
@Author  :   shange
@Mail    :   106708617@qq.com
@Version :   1.0
@Desc    :   None
'''

import sys
import os
from loguru import logger

current_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(current_dir, "..", "log")
os.makedirs(log_dir, exist_ok=True)
success_path = os.path.join(log_dir, "success.log")
failure_path = os.path.join(log_dir, "failure.log")
other_path = os.path.join(log_dir, "other.log")

logger.remove(0)
logger.add(
	sink=sys.stderr,
	level="DEBUG",
	format="<green>{time:YYYY-MM-DD hh:mm:ss}|</><lvl>{level:8}</><cyan>|{module} {name} {line:3}|</><lvl>{message}</>",
	colorize=True
)
logger.add(
	sink=success_path,
	level="INFO",
	filter=lambda record: record["extra"].get("name") == "success",
	format="{message}",
	colorize=False
)
logger.add(
	sink=failure_path,
	level="INFO",
	filter=lambda record: record["extra"].get("name") == "failure",
	format="{message}",
	colorize=False
)
logger.add(
	sink=other_path,
	# level="INFO",
	level="DEBUG",
	filter=lambda record: record["extra"].get("name") == "other",
	format="<green>{time:YYYY-MM-DD hh:mm:ss}|</><lvl>{level:8}</><cyan>|{module} {name} {line:3}|</><lvl>{message}</>",
	colorize=False
)