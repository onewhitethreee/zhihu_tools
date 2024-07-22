# 此类用于爬取链接中带有market的数据
import os, sys

import requests
from lxml import etree
import re
import base64
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import fontPreview


class MarketSpider:
    def __init__(self, header) -> None:
        self.header = header
        self.fontConfig = None

    # 保存为html文件。防止多次请求
    def getMarketHtml(self, url):

        response = requests.get(url, verify=False, headers=self.header)
        try:
            with open("market.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("写入成功")
        except Exception as e:
            print(e)

    # 获取字体文件
    def getFontFile(self, htmlFile="market.html"):
        with open(htmlFile, "r", encoding="utf-8") as f:
            html = f.read()
        fontFile = re.search(r"url\((.*?)\)", html).group(1)

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
        content = content.xpath('//*[@id="manuscript"]/p/text()')
        with open("content.txt", "w+", encoding="utf-8") as f:
            for i in content:
                f.write(i + "\n")
        print("内容写入成功！")
        return True


# 此类用来重新打开之前爬取的数据，重新解析，将其中的错误字体解析出来，然后将字体解析出来的数据替换正确的数据
class MarketParse:
    def __init__(self):
        self.glyfDict = {}

    def replace_text(self, text, replacement_dict):
        result = []
        for char in text:
            if char in replacement_dict:
                result.append(replacement_dict[char])
            else:
                result.append(char)
        return "".join(result)

    def parse(self):
        self.glyfDict = fontPreview.FontPreview().preview("font.woff", "images")
        with open("content.txt", "r", encoding="utf-8") as f:
            content = f.read()

        content = self.replace_text(content, self.glyfDict)

        with open("contents.txt", "w", encoding="utf-8") as f:
            f.write(content)


m = MarketParse()

m.parse()
print(m.glyfDict)
