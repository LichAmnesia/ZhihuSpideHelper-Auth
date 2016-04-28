# -*- coding: utf-8 -*-

'''
1. 模拟登陆知乎
'''
import sys
import requests
from bs4 import BeautifulSoup
import time
import json
import os

# 全局变量
url = 'http://www.zhihu.com'
loginURL = 'http://www.zhihu.com/login/email'
ospath = 'D:\\Work\\Python\\zhihu_lawspider\\Notused\\'


headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:41.0) Gecko/20100101 Firefox/41.0',
    "Referer": "http://www.zhihu.com/",
    'Host': 'www.zhihu.com',
}

data = {
    'email': 'anyaoaopu425@163.com',
    'password': '****************',
    'rememberme': "true",
}

s = requests.session()

# print os.path.exists(ospath  + 'cookiefile')
if os.path.exists(ospath + 'cookiefile'):
    with open(ospath + 'cookiefile') as f:
        cookie = json.load(f)
    s.cookies.update(cookie)
    req1 = s.get(url, headers=headers)
    # 建立一个zhihu.html文件,用于验证是否登陆成功
    with open(ospath + 'zhihu.html', 'w') as f:
        f.write(req1.content)
else:
    req = s.get(url, headers=headers)
    print req

    soup = BeautifulSoup(req.text, "html.parser")
    xsrf = soup.find('input', {'name': '_xsrf', 'type': 'hidden'}).get('value')

    data['_xsrf'] = xsrf

    timestamp = int(time.time() * 1000)
    captchaURL = 'http://www.zhihu.com/captcha.gif?=' + str(timestamp)
    print captchaURL

    with open('zhihucaptcha.gif', 'wb') as f:
        captchaREQ = s.get(captchaURL)
        f.write(captchaREQ.content)
    loginCaptcha = raw_input('input captcha:\n').strip()
    data['captcha'] = loginCaptcha
    print data
    loginREQ = s.post(loginURL,  headers=headers, data=data)
    if not loginREQ.json()['r']:
        print s.cookies.get_dict()
        with open('cookiefile', 'wb') as f:
            json.dump(s.cookies.get_dict(), f)
    else:
        print 'login fail'
