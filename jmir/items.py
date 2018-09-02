# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleHTMLItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    background = scrapy.Field()
    objective = scrapy.Field()
    methods = scrapy.Field()
    result = scrapy.Field()
    conclusions = scrapy.Field()
    article_text = scrapy.Field()
    references = scrapy.Field()

class ArticleXMLItem(scrapy.Item):
    article_title = scrapy.Field()
    editor_list = scrapy.Field()
    reviewer_list = scrapy.Field()
    author_list = scrapy.Field()
    history = scrapy.Field()
    subject = scrapy.Field()
    keywords = scrapy.Field()
    metadata_id = scrapy.Field()
    volume = scrapy.Field()
    issue = scrapy.Field()
    elocation_id = scrapy.Field()
    url = scrapy.Field()
    publish_data = scrapy.Field()
