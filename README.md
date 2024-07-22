# zhihu_tools
---
##### 学业繁忙，目前计划在每个星期至少提交一次更新
##### 等到真正能使用后还需要提交至少三次更新。目前还无法使用。
---
## 2024-04-20 代码重构

### 目录树 🤷‍♂️

```
├─answerSpider 用来获取到知乎盐选文件带有question的链接
│  └─__pycache__
├─config 默认配置文件。内中含有读取配置信息的内容
│  └─__pycache__
├─fakeUserAgent 请求头内容。进行爬取的时候需要有手机请求头，不然无法请求成功
│  └─__pycache__
├─fontParse 用来解决知乎字体反扒的问题。具体准备实现的方式为OCR
├─main
│  └─__pycache__
└─marketSpider 用来获取到知乎带有market链接的文章内容
    └─__pycache__

```

### 开发计划 😘

- [X] fake请求头随机获取 👌
- [ ] OCR解决字体错乱
- [ ] 单一question链接爬取
- [ ] 单一market链接爬取
- [ ] 整合一本书爬取
- [ ] 图形页面开发

### 如何使用？ 😶‍🌫️

    - python3环境
    - 正常的脑子 🧠
    - 至少小学的语文水平 📚

#### 下载此项目文件到本地

    1. 打开cmd
    2. cd到项目文件目录
    3. 输入 python/python3 main.py
    4. 进入到程序。

#### 报错？🤡

##### 1. module not found

- pip install 那个没有的模块
  后期会提供一个requirements.txt

##### 2. 无法爬取？🤡🤡

- 这是一个盐选文件获取的项目。不是无中生有破解知乎
- 首先要有的就是一个盐选账号。
  - 获取到账号的cookie复制到config.ini文件夹中有cookie的值后
- 知乎提示需升级版本
  - User-Agent 不是手机或者是无用的User-Agent
  - 如何获取一个User-Agent？
    1. 手机抓包。打开知乎然后随意一条请求复制其中的内容到config.ini文件中含有User-Agent的值后
    2. 运气。项目提供上百个User-Agent。如果一次运行失败建议再运行一次

3. 未知错误
   - 提ISSUE.
   - [怎么提问?](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way)

#### 这个项目有什么用？🤷‍♂️

- 获取盐选文章到本地观看. 除此之外没有任何用

---

**所看皆可爬**
