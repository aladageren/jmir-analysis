import scrapy
import xml.etree.ElementTree as ET
import datetime
from collections import OrderedDict

class XmlSpider(scrapy.Spider):
    name = 'xmlspider'
    allowed_domains = ['www.jmir.org']
    start_urls = ['http://www.jmir.org/2018/6/e215/xml',
                  'http://www.jmir.org/2018/8/e245/xml',
                  'http://www.jmir.org/2018/8/e246/xml',
                  'http://www.jmir.org/2018/8/e10231/xml',
                  'http://www.jmir.org/2018/8/e244/xml'
                  ]

    def text_to_int(text):
        try:
            return int(text)
        except:
            return 1

    def parse(self, response: scrapy.http.Response):
        # Root of the XML body
        root = ET.fromstring(response.body)

        # Article's title
        article_title = root.find("front/article-meta/title-group/article-title").text

        # Editor, reviewer and author list
        editor_list = []
        reviewer_list = []
        author_list = []
        contrip_group_editor = root.findall("front/article-meta/contrib-group")[0]
        contrip_group_reviewer = root.findall("front/article-meta/contrib-group")[1]
        contrib_group_authors = root.findall("front/article-meta/contrib-group")[2]

        for contrib in contrip_group_editor.iter("contrib"):
            given_names = contrib.find("name/given-names").text
            surname = contrib.find("name/surname").text
            editor_list.append("{0} {1}".format(given_names, surname))

        for contrib in contrip_group_reviewer.iter("contrib"):
            given_names = contrib.find("name/given-names").text
            surname = contrib.find("name/surname").text
            reviewer_list.append("{0} {1}".format(given_names, surname))

        for contrib in contrib_group_authors.iter("contrib"):
            given_names = contrib.find("name/given-names").text
            surname = contrib.find("name/surname").text
            author_list.append("{0} {1}".format(given_names, surname))

        # Received, Rev-Request, Rev-Received, Accepted dates
        history = OrderedDict()
        for date in root.findall("front/article-meta/history/date"):
            date_tuple = tuple(
                map(int,
                    (date.find("year").text,
                     date.find("month").text,
                     date.find("day").text)))
            dt = datetime.date(*date_tuple)
            history[date.attrib.get("date-type").title()] = dt
            #print(date.attrib.get("date-type").title(), dt)

        # Subject of the article (e.g original research, letter to the editor ...)
        subject = root.find("front/article-meta/article-categories/subj-group[1]/subject").text

        # Keywords
        keywords = []
        kwd_group = root.find("front/article-meta/kwd-group")
        for keyword in kwd_group:
            keywords.append(keyword.text)

        # Metadata / "publisher-id", "pmid", "doi" in the form of dictionary
        metadata_id = OrderedDict()
        for article_id in root.findall("front/article-meta/article-id"):
            metadata_id[article_id.attrib.get("pub-id-type")] = article_id.text

        # Metadata / Volume
        volume = root.find("front/article-meta/volume").text

        # Metadata / Issue
        issue = root.find("front/article-meta/issue").text

        # Metadata / Elocation ID
        elocation_id = root.find("front/article-meta/elocation-id").text

        # Metadata / URL
        xlink_href = "{http://www.w3.org/1999/xlink}href"
        url = root.find("front/article-meta/self-uri").attrib.get(xlink_href)

        # Publish data
        publish_data = {}
        for pub_temp in root.findall("front/article-meta/pub-date"):
            try:
                year = int(pub_temp.find("year").text)
                month = int(pub_temp.find("month").text)
                day = int(pub_temp.find("day").text)
            except:
                day = 1
            publish_data[pub_temp.get("pub-type")] = datetime.datetime(year,month,day)

        """
        out = OrderedDict()
        out.update(article_title = article_title)
        out.update(editor_list = editor_list)
        out.update(reviewer_list = reviewer_list)
        out.update(author_list = author_list)
        out.update(history = history)
        out.update(subject = subject)
        out.update(keywords = keywords)
        out.update(metadata_id = metadata_id)
        out.update(volume = volume)
        out.update(issue = issue)
        out.update(elocation_id = elocation_id)
        out.update(url = url)
        """

        out = {"article_title":article_title,
               "editor_list":editor_list,
               "reviewer_list":reviewer_list,
               "author_list":author_list,
               "history":history,
               "subject":subject,
               "keywords":keywords,
               "metadata_id":metadata_id,
               "volume":volume,
               "issue":issue,
               "elocation_id":elocation_id,
               "url":url,
               "publish_data":publish_data
               }

        yield out










