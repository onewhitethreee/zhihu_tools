import logging
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import config
import marketSpider
import fakeUserAgent
import time
class zhihuSpider:
    def __init__(self) -> None:
        self.__config = config.Config().getEnviroments()
        self.__option = None # 选项 暂时为空
        self.__header = {}
        self.__header["Cookie"] = self.__config["Cookie"]  # 设置cookie
        self.__header["User-Agent"] = self.__config["User-Agent"] + " "+ str(fakeUserAgent.fakeUserAgent().getRandomUserAgent())  # 设置User-Agent
    
    def getOptionChoise(self) -> str:

        if self.__option == "1":
            # return self.parseLink(self.optionChoise1())
            return self.optionChoise1()
        if self.__option == "2":
            # return self.parseLink(self.optionChoise2())
            return self.optionChoise2()

        if self.__option == "3":
            # return self.parseLink(self.optionChoise3())
            return self.optionChoise3()

        if self.__option == "4":
            # return self.parseLink(self.optionChoise4())
            return self.optionChoise4()
        # 如果是从命令行参数传入的
        if self.__option != None:
            return self.parseLink(self.commandChoise())

    # 爬取严选的单个问题
    def optionChoise1(self) -> str:
        logging.info("暂时不想开发。点个start鼓励鼓励作者让他开发吧！")
        logging.info("https://github.com/onewhitethreee/zhihu_tools")
        exit(0)

    # 爬取书的单个章节
    def optionChoise2(self) -> str:
        logging.info("请输入你要解析的链接: ")
        link = input()
        market = marketSpider.MarketSpider(self.__header)
        market.spider(link)
        return link

    # 爬取整本书
    def optionChoise3(self) -> str:
        logging.info("暂时不想开发。点个start鼓励鼓励作者让他开发吧！")
        logging.info("https://github.com/onewhitethreee/zhihu_tools")
        exit(0)

    # 搜索关键词爬取
    def optionChoise4(self) -> str:
        logging.info("暂时不想开发。点个start鼓励鼓励作者让他开发吧！")
        logging.info("https://github.com/onewhitethreee/zhihu_tools")
        exit(0)
    # 获取命令行参数
    def commandChoise(self) -> str:
        return self.__option


if __name__ == "__main__":
    spider = zhihuSpider()

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logging.info("=====================================")
    logging.info("程序启动")
    time.sleep(1)
    logging.info("=====================================")

    while 1:
        logging.info("请输入你的选项: ")
        logging.info("1. 爬取严选的单个问题")
        logging.info("2. 爬取书的单个章节")
        logging.info("3. 爬取整本书")
        logging.info("4. 关键词爬取")
        logging.info("0. 退出")
        spider._zhihuSpider__option = input()
        if spider._zhihuSpider__option == "0":
            break
        spider.getOptionChoise()
    logging.info("=====================================")
    logging.info("程序退出")
