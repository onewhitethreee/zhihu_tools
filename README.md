# zhihu_tools

## 2024-04-20 代码重构

### 目录树

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


### 开发计划

    [x] fake请求头随机获取
