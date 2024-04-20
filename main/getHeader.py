import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fakeUserAgent.fakeUserAgent import fakeUserAgent
import logging  


class getHeader:

    def __init__(self, config, url) -> None:
        self.config = config
        self.header = self.getHeader()
        self.link = url

    # 检查是否是soia短链接
    def check_soia_url(self) -> bool:

        # 还未开发的功能
        if "None" in self.link:
            return True

        # 不支持的链接内容
        if "soia" in self.link:
            return True
        return False

    # 获取请求头
    def getHeader(self):
        fua = fakeUserAgent()
        headers = {"User-Agent": self.config["User-Agent"].replace('"', '') + fua.getRandomUserAgent()}
        return headers

