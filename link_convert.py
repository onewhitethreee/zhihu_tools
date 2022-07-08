import requests
import re
import argparse

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('-u', type=str, default=None)
args = parser.parse_args()
headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
html = requests.request('get',args.u, headers=headers)

text_html = html.text#源码
text_encode = text_html.encode('utf-8')#解码
answer = re.findall('<div class="ContentItem-time"><a target="_blank" href="//(.*?)">',text_html)[0]
print('https://'+answer)