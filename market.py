from lxml import etree
from lxml.html import fromstring, tostring
import requests
import re
import os
import time
import argparse

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'cookie':''
}
parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('-u', type=str, default=None)
args = parser.parse_args()
print(args.u)#传入命令行的网站
html = requests.request('get',args.u, headers=headers)#请求
text_html = html.text#源码
text_encode = text_html.encode('utf-8')#解码
html_xpath = etree.HTML(text_encode)#解码为xpath
title = html_xpath.xpath('/html/body/main/div/h1/text()')[0]
section = html_xpath.xpath('string(/html/body/main/div/div[2]/div)')
now = time.strftime("%Y-%m-%d",time.localtime(time.time()))
first_texts = html_xpath.xpath('/html/body/main/div/div[2]/div/p[1]/text()')[0]
print(title)
print(first_texts) 
with open(r'./1.md','w+',encoding='utf-8') as f:
    f.write(section)#这个文件里面有源码
    firstline = f.readline().rstrip()
    with open(r'/www/bloghu/_posts/{}-{}.md'.format(now,title),'w+',encoding='utf-8') as fx:
            fx.seek(0)#在最开始写入
            fx.write('---\n')#写入————
            fx.write('title: '+title+'\n')#写入标题
            fx.write('layour: ' + 'post'+'\n')#写入layour
            fx.write('tags: ' + '杂志\n')#写入标签
            fx.write('categories: ' 'zhihu\n')#写入分类
            try:
                fx.write('excerpt: ' +first_texts+ '\n')#写入卡片显示内容
            except:
                fx.write('excerpt: ' + '\n')
            fx.write('---\n')#写入————
            replae = section.replace('\n','\r\r')#在text中查找换行符并直接替换为回车符
            fx.write(replae)