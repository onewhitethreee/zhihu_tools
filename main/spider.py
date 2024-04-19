import logging
import __config__
import shorLinkToLargeLink


class zhihuSpider:
    def __init__(self) -> None:
        self.__config = __config__.Config().getEnviroments()
        self.__option = __config__.Config().getOption()

    def getOptionChoise(self) -> str:
        if(self.__option == "1"):
            return "Question"
        if(self.__option == "2"):
            return "Market"
        if(self.__option == "3"):
            return "Exit"

        if(self.__option != None):
            self.parseLink(self.__option)
            return "None"

    def parseLink(self, link: str) -> str:
        shortLink = shorLinkToLargeLink.ShortLinkToLargeLink(link)
        return shortLink.get_large_link()


if __name__ == "__main__":
    spider = zhihuSpider()
    logging.basicConfig(level=logging.INFO)
    
    option = spider.getOptionChoise()
    
    
