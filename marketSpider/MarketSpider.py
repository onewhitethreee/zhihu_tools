# 此类用于爬取链接中带有market的数据

import requests
from lxml import etree
import re
import base64
from fontTools.ttLib import TTFont


class MarketSpider:
    def __init__(self, header) -> None:
        self.header = header
        self.fontConfig = None

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


    def uni_to_char(self, uni_code):
        return chr(int(uni_code[3:], 16))
    
    def getFontData(self, ttf_file="font.ttf"):
        # 加载WOFF文件
        font = TTFont(ttf_file)
        glyph_dict = {}

        for k, v in font.getBestCmap().items():
            # 将字体编码转换为十六进制
            print(chr(k), (v))

        return glyph_dict

    # 重新格式化内容
    def reFormat(self, content):
        content = content.replace(" ", "")

    def getContent(self, htmlFile="market.html"):
        with open(htmlFile, "r", encoding="utf-8") as f:
            html = f.read()
        content = etree.HTML(html)
        content = content.xpath('//*[@id="manuscript"]/p/text()')
        with open("content.txt", "w+", encoding="utf-8") as f:
            for i in content:
                f.write(i + "\n")
        # self.reFormat(content)


url = "https://www.zhihu.com/market/paid_column/1697665987405680640/section/1760605614483570688"

headers = {
    "User-Agent": "com.zhihu.android/Futureve/10.3.0 Mozilla/5.0 (Linux; Android 6.0.1; SM-J700M Build/MMB29K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/192.0.0.34.85;]",
    "Cookie": "_xsrf=bW5169FnALFDDvlFtacOWCNBbYFWZaBZ; KLBRSID=2177cbf908056c6654e972f5ddc96dc2|1713556508|1713556502; z_c0=2|1:0|10:1713556499|4:z_c0|92:Mi4xdjYwSVR3QUFBQUFBME5WSlRhUjlHQXdBQUFCZ0FsVk50LXhKWmdCTy1fS0RrUjlyQmNVZlFIU0pWUDdUSmpHOVdR|5351a5161585796dfbc8a2fbae5732b8232e9200ad55dbd62f65ad49ddc377ff",
}

market = MarketSpider(headers)
# market.getMarketHtml(url)
print(market.getFontData())
