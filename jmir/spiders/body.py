# -*- coding: utf-8 -*-
import scrapy
import re


class BodySpider(scrapy.Spider):
    name = 'body'
    allowed_domains = ['www.jmir.org']
    start_urls = ['http://www.jmir.org/2018/6/e215/']

    def parse(self, response: scrapy.http.Response):
        url = response.url
        abstract = response.css("article.abstract")
        num_abstract_sections = len(abstract.css("p span::text"))
        out = dict([(abstract.css("p span::text")[i].extract()[:-2].lower(),
                     abstract.css("p::text")[i].extract())
             for i in range(num_abstract_sections)])

        out.update(url=url)

        main_article = response.css("article.main-article")
        items = main_article.xpath("./*/text()").extract()
        whole_string = ""
        for i in items:
            whole_string += i
            whole_string += "\n"

        whole_string = re.sub(r"(\[\n(.*?)\])|(\[(.*?)\n\])|(\[\n(.*?)\n\])|(\[(.*?)\])", "", whole_string)
        saved_string = whole_string     # temp
        whole_string = re.sub(r"\n", " ", whole_string) # temp
        out.update(article_text = whole_string)

        references = {}
        reference_text = []
        reference_url = []
        ol = response.xpath('//div[@class="footnotes"]/ol')
        for span in ol.xpath('./li/span'):
            reference_text.append(span.xpath('./text()').extract())
            try:
                reference_url.append(span.xpath('./a[@target="_blank"]/@href').extract())
            except:
                reference_url.append("")

        for index in range(len(reference_text)):
            references[str(reference_text[index])] = str(reference_url[index])
        out.update(references = references)

        self.logger.warning('Out: %s', out)
        yield out