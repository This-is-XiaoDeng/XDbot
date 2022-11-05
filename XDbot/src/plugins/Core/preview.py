#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import __commands__ as commands
import nonebot.adapters.onebot.v11
import nonebot.params
import os.path
from playwright.async_api import async_playwright


@commands.preview.handle()
async def preview_handle(
    url: nonebot.adapters.onebot.v11.Message = nonebot.params.CommandArg()
):
    async with async_playwright() as p:
        browser = await p.firefox.launch()
        page = await browser.new_page()
        await page.goto(str(url))
        await page.screenshot(path="./data/preview.png", full_page=True)
        await browser.close()
    await commands.preview.finish(
        nonebot.adapters.onebot.v11.Message(
            nonebot.adapters.onebot.v11.MessageSegment.image(
                f"file:///{os.path.abspath('./data/preview.png')}"
            )
        )
    )
