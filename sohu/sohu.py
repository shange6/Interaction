#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   zfbWeb.py
@Time    :   2025/11/19 18:15:25
@Author  :   shange
@Email   :   106708617@qq.com
'''


import asyncio
from typing import Optional
from playwright.async_api import Playwright, Browser, BrowserContext, Page, Locator, ElementHandle
from playwright.async_api import async_playwright, expect

class Template():
    def __init__(self, logger):
        self.log = logger.bind()
        self.logs = logger.bind(name="success")
        self.logf = logger.bind(name="failure")
        self.logo = logger.bind(name="other")
        self.logo.info("初始化开始")
        self.poro = "http"
        self.host = "localhost"
        self.port = "12345"        
        self.endpoint_url = f"{self.poro}://{self.host}:{self.port}"
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.home_url = r"https://c.alipay.com/page/life-account/index?appId=2030064008001339"
        self.home_url = r"https://tv.sohu.com/s/center/index.html#/video/list"

    async def close(self):
        await asyncio.sleep(1)
        # 1. 关闭页面
        if self.page and not self.page.is_closed():
            await self.page.close()
            self.logo.info("页面已关闭")            
        # 2. 关闭上下文（无论是否保留浏览器，都应关闭上下文）
        if self.context:
            await self.context.close()
            self.logo.info("浏览器上下文已关闭")            
        # 3. 若不保留浏览器，关闭浏览器实例
        if self.browser:
            await self.browser.close()
            self.logo.info("浏览器已关闭")            
        # 4. 停止Playwright
        if self.playwright:
            await self.playwright.stop()
            self.logo.info("Playwright已停止")

    async def get_existing_browsers(self, endpoint_url: str):
        self.logo.info(f"开始连接现有浏览器({endpoint_url})")
        self.browser = await self.playwright.chromium.connect_over_cdp(endpoint_url)
        self.context = self.browser.contexts[0] if self.browser.contexts else await self.browser.new_context()
        self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()
        self.logo.info(f"成功连接现有浏览器({endpoint_url})")

    async def get_new_browser(self):
        self.logo.info("开始获取新建浏览器")
        self.context = await self.playwright.chromium.launch_persistent_context(
            headless=False,
            user_data_dir="C:\\Users\\shange\\AppData\\Local\\Temp\\alipay_data",
            # executable_path=r"C:\Users\shange\AppData\Local\ms-playwright\chromium-1148\chrome-win\chrome.exe",
            args=[
                # "--incognito",    # 隐身模式，不持久化任何用户数据（缓存、Cookie 等）
                # "--no-sandbox", 
                # "--no-first-run",
                # "--no-default-browser-check"
                "--remote-debugging-port=12345",
                # "--new-window http://www.jd.com"
                # "--disable-dev-shm-usage",
                # "--disable-features=VizDisplayCompositor",
                # "--disable-features=LockProfileCookieDatabase",
                # "--disable-blink-features=AutomationControlled",
            ],
            viewport={"width": 1200, "height": 800},
            ignore_default_args=["--enable-automation"],
            timeout=30000
        )        
        self.browser = self.context.browser
        self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()
        # 隐藏webdriver属性
        await self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            window.chrome = { runtime: {} };
        """)
        self.logo.info("成功获取新建浏览器")

    async def get_page(self):
        self.playwright = await async_playwright().start()
        try:
            await self.get_existing_browsers(self.endpoint_url)
        except Exception as e:
            self.logo.debug(f"失败连接现有浏览器({self.endpoint_url})")
            await self.get_new_browser()
        # cookies = [
        #     {"name": "key", "value": "value", "domain": ".alipay.com", "path": "/"},
        #     {"name": "key2", "value": "value2", "domain": ".alipay.com", "path": "/"}
        # ]
        # await self.context.add_cookies(cookies)

    async def run(self):
        await self.get_page()
        await self.page.goto(self.home_url, wait_until="networkidle")
        self.logo.debug(f"打开登录页面: {self.page.url}")
        await asyncio.sleep(2)
        await self.page.pause()
        await self.page.get_by_text("发布作品").click()
        self.logo.debug("进入发布作品页面")
        await asyncio.sleep(1)
        file_input = self.page.locator('input[type="file"]')
        self.logo.debug("选择文件上传控件")
        await asyncio.sleep(1)
        await file_input.set_input_files(r"C:\\Users\\shange\\Videos\\11月11日.mp4")
        self.logo.debug("设置上传文件路径")
        await asyncio.sleep(3)






        
        await self.page.pause()  # 暂停页面，方便调试观察
        storage = await self.context.storage_state(path="./state.json")


