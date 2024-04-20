# 此类用来解决字体反爬问题

from fontTools.ttLib import TTFont
import xml.etree.ElementTree as ET
import os


class fontDecripy:
    def __init__(self) -> None:
        self.glyfList = []
        self.glyfName = []

        self.glyfDict = {}

    # 保存为xml文件
    def saveAsXML(self, fontPath="font.ttf", savePath="font.xml"):
        font = TTFont(fontPath)
        font.saveXML(savePath)

    # 读取xml文件中的配套字体映射关系
    def getGlyphOrder(self, xml_file="font.xml") -> list:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        self.glyfList = [glyph.get("name") for glyph in root.iter("GlyphID")]
        return self.glyfList.remove(".notdef")

    # 读取文件中的配套字体映射关系
    def getHmtx(self, xml_file="font.xml") -> list:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        self.glyfName = [names.get("name") for names in root.iter("mtx")]
        return self.glyfName.remove(".notdef")

    # 解析字体
    def parseFont(self) -> dict:
        for i in range(len(self.glyfList)):
            self.glyfDict[self.glyfList[i]] = self.glyfName[i]

    # unicode转中文
    def uniToChar(self, uni_code) -> str:
        return chr(int(uni_code[3:], 16))

    # 获取字体字典数据，使其转换为中文
    def parseToChinese(self):
        dict_translate = {}
        for key, value in self.glyfDict.items():
            key = self.uniToChar(key)
            value = self.uniToChar(value)
            dict_translate[key] = value
            self.glyfDict = dict_translate
        return dict_translate

    # 删除xml文件
    def rmXML(self, xml_file="font.xml"):
        os.remove(xml_file)

    # 删除ttf文件
    def rmTTF(self, ttf_file="font.ttf"):
        os.remove(ttf_file)

    # 返回一个解析后的字典
    def main(self):
        self.saveAsXML()
        self.getGlyphOrder()
        self.getHmtx()
        self.parseFont()
        self.parseToChinese()
        # self.rmXML()
        return self.glyfDict

# 进行实例化然后获取glyfDict即可获取解析后的字典
