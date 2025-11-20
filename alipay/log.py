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
from loguru import logger

success_path = "./log/success.log"
failure_path = "./log/failure.log"
other_path = "./log/jdjx.log"

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
	level="INFO",
	filter=lambda record: record["extra"].get("name") == "other",
	format="<green>{time:YYYY-MM-DD hh:mm:ss}|</><lvl>{level:8}</><cyan>|{module} {name} {line:3}|</><lvl>{message}</>",
	colorize=False
)