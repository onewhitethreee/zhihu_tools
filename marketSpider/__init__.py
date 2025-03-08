# 此类用于爬取链接中带有market的数据
import os, sys

import requests
from lxml import etree
import re
import base64
import sys
import os
import json
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import fontPreview


class MarketSpider:
    def __init__(self, header) -> None:
        self.header = header
        self.marketTitle = None
        self.glyfDict = {}
        self.url = None  # 保存初始URL

    def getMarketHtml(self, url):
        self.url = url  # 保存URL
        response = requests.get(url, verify=False, headers=self.header)
        try:
            with open("market.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            logging.info("文章请求成功！")
        except Exception as e:
            logging.error("文章请求失败：", str(e))

    def re_fetch_article(self):
        """
        重新请求文章，更新HTML和字体文件
        """
        logging.info("重新请求文章...")
        self.getMarketHtml(self.url)  # 重新下载HTML
        self.getFontFile()  # 重新获取字体文件
        self.getContent()

        # 获取字体文件并且下载

    def getFontFile(self, htmlFile="market.html"):
        with open(htmlFile, "r", encoding="utf-8") as f:
            html = f.read()
        fontFile = self.get_third_font_face(html)
        if fontFile == "":
            logging.error("未匹配到字体文件！")
            return
        parts = fontFile.split(",")
        if len(parts) != 2:
            logging.error("无效的字体数据URL！")
            return
        # 获取数据部分
        data = parts[1]
        try:
            # 将数据进行解码
            data_bytes = base64.b64decode(data)
            # 将解码后的数据保存到文件
            with open("font.woff", "wb") as file:
                file.write(data_bytes)
            logging.info("字体文件下载成功！")
        except Exception as e:
            logging.error("字体文件下载失败:", str(e))

    # 获取第三个字体文件。应该为被动调用
    def get_third_font_face(self, font_re):
        font_face_blocks = re.findall(r"@font-face\s*{[^}]*}", font_re)
        # 获取第三个 @font-face 规则块
        if len(font_face_blocks) >= 3:
            font_face_blocks = re.findall(r"@font-face\s*{[^}]*}", font_re)
            font_url = re.search(r"src:\s*url\(([^)]+)\)", font_face_blocks[2]).group(1)
            return font_url
        else:
            return ''

    # 获取正文
    def getContent(self, htmlFile="market.html") -> bool:
        with open(htmlFile, "r", encoding="utf-8") as f:
            html = f.read()

        if not html:
            logging.error("在获取文件的时候出错了！")
            return False

        content = etree.HTML(html)
        content = content.xpath('string(//*[@id="resolved"])')
        content = json.loads(content)
        contents = content["appContext"]["__connectedAutoFetch"]["manuscript"]["data"][
            "manuscriptData"
        ]["pTagList"]  # 获取内容

        self.marketTitle = content["appContext"]["__connectedAutoFetch"]["manuscript"]["data"][
                               "manuscriptData"
                           ]["title"] + ".txt"  # 获取标题
        with open(self.marketTitle + ".temp", "w", encoding="utf-8") as f:
            for item in contents:
                f.write(item + "\n")
        logging.info("内容获取成功！")
        return True

    # 替换正文中的文字
    def replace_text(self, text, replacement_dict):
        result = []
        for char in text:
            if char in replacement_dict:
                result.append(replacement_dict[char])
            else:
                result.append(char)
        return "".join(result)

    # 解析字体文件
    def parse(self):
        font_preview = fontPreview.FontPreview()
        font_preview.set_market_spider(self)  # 关联MarketSpider实例
        self.glyfDict = font_preview.preview("font.woff", "images")
        logging.info(f"字体映射表: {self.glyfDict}")  # 打印映射表以验证
        with open(self.marketTitle + ".temp", "r", encoding="utf-8") as f:
            content = f.read()
        content = self.replace_text(content, self.glyfDict)
        with open(self.marketTitle, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info("文章解析成功！")

    def spider(self, url):
        self.getMarketHtml(url)
        self.getFontFile()
        if self.getContent():
            self.parse()

