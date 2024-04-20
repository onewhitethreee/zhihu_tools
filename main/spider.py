import logging
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import __config__

import main.getHeader as getHeader

class zhihuSpider:
    def __init__(self) -> None:
        self.__config = __config__.Config().getEnviroments()
        self.__option = __config__.Config().getOption()
        self.__header = None

    def getOptionChoise(self) -> str:

        if self.__option == "1":
            # return self.parseLink(self.optionChoise1())
            return self.parseLink(self.optionChoise1())
        if self.__option == "2":
            return self.parseLink(self.optionChoise2())

        if self.__option == "3":
            # return self.parseLink(self.optionChoise3())
            return self.optionChoise3()

        # 如果是从命令行参数传入的
        if self.__option != None:
            return self.parseLink(self.commandChoise())

    # 第一个选项的选择
    def optionChoise1(self) -> str:
        logging.info("暂时不想开发")
        return "None"

    # 第二个选项的选择
    def optionChoise2(self) -> str:
        logging.info("请输入你要解析的链接: ")
        link = input()
        return link

    # 第三个选项的选择
    def optionChoise3(self) -> str:
        logging.info("退出程序")
        return "None"

    # 获取命令行参数
    def commandChoise(self) -> str:
        return self.__option

    # 解析链接
    def parseLink(self, link):
        header = getHeader.getHeader(self.__config, link)

        if(header.check_soia_url()):
            logging.info("暂时不支持soia短链接")

        self.__header = header
    
    

if __name__ == "__main__":
    spider = zhihuSpider()

    logging.basicConfig(level=logging.INFO)
    spider.getOptionChoise()
    print("=====================================")
    logging.info("程序退出")
