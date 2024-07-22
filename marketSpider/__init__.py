# 此类用于爬取链接中带有market的数据
import os, sys

import requests
from lxml import etree
import re
import base64
import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import fontPreview


class MarketSpider:
    def __init__(self, header) -> None:
        self.header = header
        self.marketTitle = None
    # 保存为html文件。防止多次请求
    def getMarketHtml(self, url):
        response = requests.get(url, verify=False, headers=self.header)
        try:
            with open("market.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("写入成功")
        except Exception as e:
            print(e)
    def get_third_font_face(self, html):
        font_face_blocks = re.findall(r"@font-face\s*{[^}]*}", html)
        # 获取第三个 @font-face 规则块
        if len(font_face_blocks) >= 3:
            font_face_blocks = re.findall(r"@font-face\s*{[^}]*}", html)
            font_url = re.search(r"src:\s*url\(([^)]+)\)", font_face_blocks[2]).group(1)
            return font_url
        else:
            return ''
    # 获取字体文件并且下载
    def getFontFile(self, htmlFile="market.html"):
        with open(htmlFile, "r", encoding="utf-8") as f:
            html = f.read()
        fontFile = self.get_third_font_face(html)
        if fontFile == '':
            print("未匹配到字体文件！")
            return
        parts = fontFile.split(",")
        if len(parts) != 2:
            print("无效的数据URL！")
            return
        # 获取数据部分
        data = parts[1]
        try:
            # 将数据进行解码
            data_bytes = base64.b64decode(data)
            # 将解码后的数据保存到文件
            with open("font.woff", "wb") as file:
                file.write(data_bytes)
            print("字体文件下载成功！")
        except Exception as e:
            print("文件下载失败:", str(e))

    # 重新格式化内容
    def getContent(self, htmlFile="market.html") -> bool:
        with open(htmlFile, "r", encoding="utf-8") as f:
            html = f.read()

        if not html:
            print("文件为空！")
            return False

        content = etree.HTML(html)
        content = content.xpath('string(//*[@id="resolved"])')
        content = json.loads(content)
        contents = content["appContext"]["__connectedAutoFetch"]["manuscript"]["data"][
            "manuscriptData"
        ]["pTagList"] # 获取内容
        with open(self.marketTitle, "w", encoding="utf-8") as f:
            for item in contents:
                f.write(item + "\n")
        print("内容获取成功！")
        return True


# 此类用来重新打开之前爬取的数据，重新解析，将其中的错误字体解析出来，然后将字体解析出来的数据替换正确的数据
class MarketParse:
    def __init__(self):
        self.glyfDict = {}

    def replace_text(self, text, replacement_dict): # 替换文本
        result = []
        for char in text:
            if char in replacement_dict:
                result.append(replacement_dict[char])
            else:
                result.append(char)
        return "".join(result)

    def parse(self): # 解析字体文件
        self.glyfDict = fontPreview.FontPreview().preview("font.woff", "images")
        with open("content.txt", "r", encoding="utf-8") as f:
            content = f.read()

        content = self.replace_text(content, self.glyfDict)

        with open("contents.txt", "w", encoding="utf-8") as f:
            f.write(content)


m = MarketSpider(
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
)
m.getContent()
m.getFontFile()
p = MarketParse()
p.parse()