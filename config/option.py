# 此文件用来获取命令行参数的信息或者菜单选项的信息
import sys
import logging
class option:
    def __init__(self):
        self.type = ""

    def menu(self) -> None:
        logging.info("1. Question 链接")
        logging.info("2. Market   链接")
        logging.info("3.          退出")
    
    # 获取命令行参数
    def getCommand(self) -> str:
        # 返回命令行参数
        if len(sys.argv) == 2:
            return sys.argv[1]
        # 如果命令行参数大于2, 则提示错误
        if (len(sys.argv) > 2):
            logging.info("正确的命令行参数为: python3 main.py [链接]")
            return "None"
    
    # 获取选项
    def getOption(self) -> None:
        while(1):
            self.type = input("请输入选项: ")
            if(self.type == "1" or self.type == "2" or self.type == "3"):
                break
            else:
                logging.info("输入错误, 请重新输入")

    def main(self) -> str:
        # 如果命令行参数为None, 则返回None
        if self.getCommand() == "None":
            return None
        
        # 如果命令行参数不为None, 则返回命令行参数
        if self.getCommand() != None:
            self.type = self.getCommand()
        
        # 如果命令行参数为None, 则返回菜单选项
        if self.getCommand() == None:
            self.menu()
            self.getOption()
        return self.type
