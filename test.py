#!/usr/bin/python
# -*-encoding:utf8 -*-

import queue
import threading
import time
import argparse,sys,os
import re,requests
from urllib import parse
from socket import *


url = 'https://www.andseclab.com/wp-admi'
# sock = socket(AF_INET, SOCK_STREAM)
# sock.settimeout(5)
# result = sock.connect_ex((url,80))
# print(result)

bad_msg = ['404', '页面不存在', '不可访问','can\'t be found']  # 用于检测页面自定义报错的信息
headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
res = requests.post(url, headers=headers,timeout=10)

print(res.status_code)




