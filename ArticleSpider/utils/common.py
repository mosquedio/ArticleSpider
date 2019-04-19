# -*- coding: utf-8 -*-
# @Time    : 19-1-9 上午11:52
# @Author  : turing_lee
# @Email   : 13500502420@163.com
# @File    : common.py
import hashlib

def get_md5(url):
    if isinstance(url,str):             #判断url是不是str类型,如果是,先进行转码
        url = url.encode("utf-8")       #先将unicode编码转化成utf-8编码
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()          #抽取摘要

if __name__=="__main__":
    print(get_md5("http://jobbole.com"))    #python3中所有的字符都是unicode