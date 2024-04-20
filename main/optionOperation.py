import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fakeUserAgent.fakeUserAgent import fakeUserAgent
from marketSpider.MarketSpider import MarketSpider  # 导入marketSpider类


class operation:
    # 此函数和菜单选项1绑定。暂时不想开发
    def _answerSpider(self) -> str:
        pass

    # 此函数和菜单选项2绑定
    def _markeSpider(self) -> str:
        market = MarketSpider(self.__header.header, self.__config)
        market.getMarket()

    # 此函数用来解析命令行参数中的链接是什么类型的
    def _commandSpider(self) -> str:
        pass
