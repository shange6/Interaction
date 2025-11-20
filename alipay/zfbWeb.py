#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   zfbWeb.py
@Time    :   2025/11/19 18:15:25
@Author  :   shange
@Email   :   106708617@qq.com
'''


import os
import re
import time
import pillow_avif
import asyncio
from log import logger
from PIL import Image, ImageDraw, ImageFont
from playwright.async_api import Page, Locator, ElementHandle
from playwright.async_api import async_playwright, expect

class AlipayWeb():
    def __init__(self):
        self.log = logger.bind()
        self.logs = logger.bind(name="success")
        self.logf = logger.bind(name="failure")
        self.logo = logger.bind(name="other")
        self.logo.info("初始化开始")
        self.playwright = None
        self.browser = None  # 浏览器实例（Browser类型）
        self.context = None  # 浏览器上下文（BrowserContext类型）
        self.page = None
        self.home_url = r"https://c.alipay.com/page/life-account/index?appId=2030064008001339"
        self.login_url = r"https://passport.jd.com/new/login.aspx"  # 注意：此处是京东登录页，建议改为支付宝登录页

    async def close(self):
        """关闭资源（统一在一个事件循环中执行）"""
        try:
            # 1. 关闭页面
            if self.page:
                await self.page.close()
                self.logo.info("页面已关闭")
            
            # 2. 关闭上下文（优先关闭上下文，再关闭浏览器）
            if self.context:
                await self.context.close()
                self.logo.info("浏览器上下文已关闭")
            
            # 3. 关闭浏览器（如果存在独立浏览器实例）
            if self.browser and self.browser != self.context:  # 避免重复关闭
                await self.browser.close()
                self.logo.info("浏览器已关闭")
            
            # 4. 停止Playwright
            if self.playwright:
                await self.playwright.stop()
                self.logo.info("Playwright已停止")
        except Exception as e:
            self.logo.error(f"关闭资源时出错: {str(e)}")

    async def get_page(self):
        """连接现有浏览器或新建浏览器（修正对象类型）"""
        endpoint_url = "http://localhost:12345"
        try:
            self.logo.info(f"连接现有浏览器({endpoint_url})")
            self.playwright = await async_playwright().start()
            # 连接现有浏览器（返回Browser类型）
            self.browser = await self.playwright.chromium.connect_over_cdp(endpoint_url)
            
            # 获取现有上下文（如果无上下文则新建）
            if self.browser.contexts:
                self.context = self.browser.contexts[0]
            else:
                self.context = await self.browser.new_context()
            
            # 获取现有页面（如果无页面则新建）
            if self.context.pages:
                self.page = self.context.pages[0]
            else:
                self.page = await self.context.new_page()
            
            self.logo.info(f"连接现有浏览器成功({endpoint_url})")
        except Exception as e:            
            self.logo.info(f"连接现有浏览器失败({endpoint_url})，错误: {str(e)}")
            self.logo.info("获取新建浏览器")
            
            self.playwright = await async_playwright().start()
            # 启动持久化上下文（返回BrowserContext类型）
            self.context = await self.playwright.chromium.launch_persistent_context(
                headless=False,  # 调试时建议设为False，方便观察
                user_data_dir="C:\\Users\\shange\\AppData\\Local\\Temp\\alipay_data",  # 独立目录，避免冲突
                # executable_path=r"C:\Users\shange\AppData\Local\ms-playwright\chromium-1148\chrome-win\chrome.exe",
                args=[
                    "--incognito",
                    "--no-sandbox", 
                    "--disable-dev-shm-usage",
                    "--remote-debugging-port=12345",
                    "--disable-features=LockProfileCookieDatabase",
                    # 移除无关参数：--new-window http://www.jd.com（避免强制打开京东页面）
                ]
            )
        
            # 新建页面
            self.page = await self.context.new_page()
            self.logo.info("获取新建浏览器成功")

    async def run(self):
        """主逻辑执行"""
        await self.get_page()
        # 打开目标页面并等待加载（避免程序立即结束）
        await self.page.goto(self.home_url, wait_until="networkidle")
        self.logo.info(f"已打开页面: {self.page.url}")
        # 停留5秒观察效果（可根据需要调整）
        await asyncio.sleep(5)

# 统一事件循环管理（关键修正）
async def main():
    alipay = AlipayWeb()
    try:
        await alipay.run()
    finally:
        await alipay.close()  # 在同一个事件循环中关闭资源

if __name__ == "__main__":
    try:
        asyncio.run(main())  # 仅创建一次事件循环
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}")