import scrapy
import urllib.request
import json

class IssueListSpider(scrapy.Spider):
    name = 'issuelist'
    allowed_domains = ['www.jmir.org']
    start_urls = ['http://www.jmir.org/issue/archive']

    def parse(self, response: scrapy.http.Response):
        issue_list = []
        for li_item in response.css("section.authors-list ol li"):
            issue_list += li_item.css("a::attr(href)").extract()
        issue_list = [x for x in issue_list if not "suppl" in x]


        article_list = []
        for url in issue_list:
            json_url = str(url) + "/JSON"
            res = urllib.request.urlopen(json_url)
            res_body = res.read()
            d = json.loads(res_body.decode("utf-8"))
            collection_index = []
            for key in d.keys():
                try:
                    collection_index.append(int(key))
                except:
                    pass
            collection_index = sorted(collection_index)
            article_count = []
            for count in collection_index:
                article_count.append(len(d[str(count)]['articles']))
            index = 0
            for x in collection_index:
                for y in range(article_count[index]):
                    article_list.append(d[str(x)]['articles'][y]['articleUrl'])
                index += 1

        file = open("article_list.txt", "w")
        file.write("\n".join(article_list))
        file.close()