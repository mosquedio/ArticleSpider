# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import JobboleArticleItem,ArticleItemLoader
from ArticleSpider.utils.common import get_md5
from scrapy.loader import ItemLoader

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1.获取文章列表页中的文章url并交给scrapy下载后并进行解析
        2.获取下一页的url并交给scrapy进行下载，下载完成后交给parse
        :param response:
        :return:
        """

        #解析列表页中的所有文章url并交给scrapy下载后并进行解析
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
                                                                #用meta的方式可以向response中传入想要的值
            yield Request(url=parse.urljoin(response.url,post_url),meta={"front_img":image_url},callback=self.parse_detail)

        #提取下一页并交给scrapy下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            #parse.urljoin()函数在url没有域名的时候会自动的把response中的根域名加上去
            yield Request(url=parse.urljoin(response.url,next_url),callback=self.parse)


    def parse_detail(self,response):
        article_item = JobboleArticleItem()

        # 通过xpath提取字段
        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]
        # create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].replace("·","").strip()
        # praise_num = response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()").extract()[0]
        # fav_nums = response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract()[0]
        # match_re = re.match(".*?(\d+).*",fav_nums)
        # if match_re:
        #     fav_nums = int(match_re.group(1))
        # else:
        #     fav_nums = 0
        # comment_nums = response.xpath("//a[@href='#article-comment']/span").extract()[0]
        # match_re = re.match(".*?(\d+).*", comment_nums)
        # if match_re:
        #     comment_nums = int(match_re.group(1))
        # else:
        #     comment_nums = 0
        # content = response.xpath("//div[@class='entry']").extract()[0]
        # tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        # tags = ','.join(tag_list)

        #通过css选择器提取字段
        # front_img_url = response.meta.get("front_img", "")   #文章封面图(meta是字典,可以用[]直接提取,但是用get方法可以避免抛异常)
        # title = response.css(".entry-header h1::text").extract_first("")
        # create_date = response.css("p.entry-meta-hide-on-mobile::text").extract()[0].replace("·","").strip()
        # praise_nums = response.css(".vote-post-up h10::text").extract()[0]
        # fav_nums = response.css(".bookmark-btn::text").extract()[0]
        # match_re = re.match(".*?(\d+).*", fav_nums)
        # if match_re:
        #     fav_nums = int(match_re.group(1))
        # else:
        #     fav_nums = 0
        # comment_nums = response.css("a[href='#article-comment'] span::text").extract()[0]
        # match_re = re.match(".*?(\d+).*", comment_nums)
        # if match_re:
        #     comment_nums = int(match_re.group(1))
        # else:
        #     comment_nums = 0
        # content = response.css("div.entry").extract()[0]
        # tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        # tags = ','.join(tag_list)
        #
        # article_item["title"] = title
        # try:
        #     create_date = datetime.datetime.strptime(create_date,"%Y/%m/%d").date()
        # except Exception as e:
        #     create_date = datetime.datetime.now().date()
        #
        # article_item["create_date"] = create_date
        # article_item["url"] = response.url
        # article_item["url_object_id"] = get_md5(response.url)   #因为文章的url长度长短不一，所以进行MD5转码长度一致，方便保存
        # article_item["front_img_url"] = [front_img_url]         #这里把它变成数组是因为在settings中配置image_url时，会默认的从数组中取值
        # article_item["praise_nums"] = praise_nums
        # article_item["fav_nums"] = fav_nums
        # article_item["comment_nums"] = comment_nums
        # article_item["content"] = content
        # article_item["tags"] = tags


        #通过Item Loder加载item    (可将这些css格式写到文件或数据库中,达到可配置化的目的)
        front_img_url = response.meta.get("front_img", "")  # 文章封面图(meta是字典,可以用[]直接提取,但是用get方法可以避免抛异常)
        item_loader = ArticleItemLoader(item=JobboleArticleItem(), response=response)
        item_loader.add_css("title", ".entry-header h1::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        item_loader.add_value("front_img_url", [front_img_url])
        item_loader.add_css("praise_nums", ".vote-post-up h10::text")
        item_loader.add_css("fav_nums", ".bookmark-btn::text")
        item_loader.add_css("comment_nums", "a[href='#article-comment'] span::text")
        item_loader.add_css("content", "div.entry")
        item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")

        article_item = item_loader.load_item()

        yield article_item      #yield之后,将article_item传递到pipeline中去

        pass
