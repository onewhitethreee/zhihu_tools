
from lxml import etree
import requests
import re
import os
import time
import random
import argparse

def generate_code(code_len=2):

    all_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    last_pos = len(all_chars) - 1
    code = ''
    #获取数字
    for _ in range(code_len):
        index = random.randint(0, last_pos)#61
        code += all_chars[index]#获取位于61位的字母或数字
        #print(all_chars)
    return code

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'cookie':''}
parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('-u', type=str, default=None)
args = parser.parse_args()
print(args.u)#传入命令行的网站
html = requests.request('get',args.u, headers=headers)#请求
text_html = html.text#源码
text_encode = text_html.encode('utf-8')#解码
html_xpath = etree.HTML(text_encode)#解码为xpath
answer = re.findall('<title data-rh="true">(.*?)? - 知乎</title>',text_html)[0]#正则获取问题
answer_without_interrogation = answer.split('?')[0]#切割问好
texts = html_xpath.xpath('string(/html/body/div[1]/div/main/div/div/div[3]/div[1]/div/div[2]/div/div/div/div[3]/span[1]/div/span)')#获取文本
try:
    first_texts = html_xpath.xpath('string(/html/body/div[1]/div/main/div/div/div[3]/div[1]/div/div[2]/div/div/div/div[3]/span[1]/div/span/p[1])')
except:
    print('第一行获取失败')
#print(first_texts)
now = time.strftime("%Y-%m-%d",time.localtime(time.time()))
nows = time.strftime("%Y-%m-%d %H:%M",time.localtime(time.time())) 
with open(r'./1.md','w+',encoding='utf-8') as f:
    f.write(texts)#这个文件里面有源码
    firstline = f.readline().rstrip()
    with open(r'/www/bloghu/_posts/{}-{}-{}.md'.format(now,answer_without_interrogation,generate_code()),'w+',encoding='utf-8') as fx:
        fx.seek(0)#在最开始写入
        fx.write('---\n')#写入————
        fx.write('title: '+answer_without_interrogation+'\n')#写入标题
        fx.write('layour: ' + 'post'+'\n')#写入layour
        fx.write('tags: ' + '回答\n')#写入标签
        fx.write('categories: ' 'zhihu\n')#写入分类
        try:
            fx.write('excerpt: ' +first_texts+ '\n')#写入卡片显示内容
        except:
            fx.write('excerpt: ' + '\n')
        fx.write('---\n')#写入————
        replae = texts.replace('\n','\r\r')#在text中查找换行符并直接替换为回车符
        fx.write(replae)
print('excerpt是：'+first_texts)
print('时间为：' + nows)
print('已成功保存在post文件夹下')
os.remove(r'./1.md')
#os.remove(r'./{}.html'.format(answer_without_interrogation))
