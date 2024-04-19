import requests
import sys
import os
proyectDit = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(proyectDit)

from fakeUserAgent.fakeUserAgent import fakeUserAgent

class ShortLinkToLargeLink:
    def __init__(self, short_link):
        self.short_link = short_link

    # 检查是否是soia短链接
    def check_soia_url(self) -> bool:
        if "soia" in self.short_link:
            return True
        return False

    def get_large_link(self) -> str:
        fua = fakeUserAgent()
        headers = {"User-Agent": fua.getRandomUserAgent()}
        print(headers)

    def moreFunction(self):
        pass

    def main(self):
        if(self.check_soia_url()):
            return "暂不支持soia短链接"

s = ShortLinkToLargeLink("https://www.soia.vip/1")
s.get_large_link()
