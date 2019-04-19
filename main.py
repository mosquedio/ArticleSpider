# -*- coding: utf-8 -*-
# @Time    : 19-1-7 下午2:24
# @Author  : turing_lee
# @Email   : 13500502420@163.com
# @File    : main.py

from scrapy.cmdline import execute
import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(["scrapy","crawl","jobbole"])
execute(["sdcrapy","crawl","zhihu"])