import configparser


class Config:
    def __init__(self) -> None:
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")

    # 获取config.ini配置文件
    def get(self, section, key) -> str:
        return self.config.get(section, key)

    # 获取config.ini环境变量
    def getEnviroments(self) -> dict:

        envoromentDict = {}
        envoromentDict["Cookie"] = self.get("DEFAULT", "Cookie")
        envoromentDict["User-Agent"] = self.get("DEFAULT", "User-Agent")
        envoromentDict["Host"] = self.get("DEFAULT", "Host")
        return envoromentDict
