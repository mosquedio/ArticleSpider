# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
import re
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from scrapy.loader import ItemLoader

class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def add_jobbole(value):
    return value+"-jobbole"


def trim_and_replace(value):
    return value.replace("·","").strip()


def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date

#用正则表达式提取数字
def get_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums

#去掉tags中的评论二字
def remove_comment_tags(value):
    if "评论" in value:
        return ""
    else:
        return value


def retrun_value(value):
    return value


#自定义ItemLoader
class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()                #默认取list中的第一个元素


class JobboleArticleItem(scrapy.Item):
    #指明类型,scrapy中只有Field这一种类型
    title = scrapy.Field(
        input_processor=MapCompose(add_jobbole)           #input_processor=MapCompose(add_jobbole,lambda x: x+"-lee")  #(匿名函数lambda用法)
    )
    create_date = scrapy.Field(
        input_processor=MapCompose(trim_and_replace, date_convert)
        # out_processor=TakeFirst()
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_img_url = scrapy.Field(
        output_processor=MapCompose(retrun_value)
    )
    front_img_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor= MapCompose(get_nums)
    )
    fav_nums = scrapy.Field(
        input_processor= MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor= MapCompose(get_nums)
    )
    content = scrapy.Field()
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor=Join(",")
    )