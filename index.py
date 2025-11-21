
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   index.py
@Time    :   2025/11/21 14:56:55
@Author  :   shange
@Email   :   106708617@qq.com
'''



import asyncio
from utils.log import logger
from sohu.sohu import Template


async def run_template(logger):
    template = Template(logger)
    try:
        await template.run()
    finally:
        await template.close()


if __name__ == "__main__":
    asyncio.run(run_template(logger))