import os
import random
import json
import logging

class fakeUserAgent:
    def __init__(self):
        self.user_agents = []

    # 从json文件中读取user-agent
    def loadUserAgent(self):
        with open("fakeUserAgent/user_agents.json", "r") as f:
            user_agents = json.load(f)
            logging.info("加载user-agent成功")
            logging.info("--------------------------")
            # 获取所有key
            for key in user_agents.keys():
                self.user_agents.append(user_agents[key])

    # 随机获取一个user-agent
    def getRandomPlatform(self) -> str:
        return random.randint(0, len(self.user_agents) - 1)

    # 获取随机的user-agent
    def getRandomUserAgent(self) -> str:

        self.loadUserAgent()
        return self.user_agents[self.getRandomPlatform()][
            random.randint(0, len(self.user_agents[self.getRandomPlatform()]) - 1)
        ]

