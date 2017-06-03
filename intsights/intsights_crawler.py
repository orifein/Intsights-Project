import requests
import arrow
from lxml import etree
from io import StringIO
from intsights_model import IntsightsModel


class IntsightsCrawler():
    AUTHOR_NAMES_CONST = ['Guest', 'Unknown', 'Anonymous']
    BASE_URL = 'file:///Users/orifein/Downloads/StrongholdPaste.html'
    ALL_ROWS_ELEMENTS = '#list .col-sm-12'

    def _get_content_from_html(self):
        http_parse = requests.get(self.BASE_URL)
        content_string = http_parse.text
        return content_string

    def _parse_html_content(self, content):
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(content), parser)
        return tree

    def _fetch_date_and_author(self, element):
        fetched_text = ''
        element_text = element.cssselect('.pre-footer')[0]
        for x in element_text.itertext():
            fetched_text += x.replace('\n', '').replace('\t', '')
        fetch_splitted = fetched_text.replace(',', '').split(' ')
        author = fetch_splitted[2]
        if author in self.AUTHOR_NAMES_CONST:
            author = 'Anonymous'
        date_fetched = fetch_splitted[6]+'-'+fetch_splitted[5] + \
            '-'+fetch_splitted[4]+' '+fetch_splitted[7]
        date = arrow.get(date_fetched, 'YYYY-MMM-DD HH:mm:ss')
        return author, date

    def _get_elements_from_tree(self, tree):
        content = ''
        list_of_models = []
        html_root = tree.getroot()
        all_rows = html_root.cssselect(self.ALL_ROWS_ELEMENTS)
        for element in all_rows:
            response = IntsightsModel()
            got_title = element.cssselect('h4')
            txt_cont = element.cssselect('.well-sm')
            if not got_title:
                continue
            title_text = got_title[0].text
            response.title = title_text.replace('\n', '').replace('\t', '')
            for txt in txt_cont[0].itertext():
                content += txt.replace('\n', '').replace('\t', '')
            response.content = content
            author, date = self._fetch_date_and_author(element)
            response.author = author
            response.date = date
            list_of_models.append(response)
        # sorting dates
        list_of_models.sort(key=lambda model: model.date, reverse=True)
        for paste_model in list_of_models:
            paste_model.date = str(paste_model.date)
        return list_of_models

    def _get_proxy_for_onion_sites(self):
        session = requests.session()
        session.proxies = {'http':  'socks5h://localhost:9050',
                           'https': 'socks5h://localhost:9050'}
        return session

    def crawl(self):
        session = self._get_proxy_for_onion_sites()
        #       content = self._get_content_from_html()
        content = session.get('http://nzxj65x32vh2fkhk.onion/all').text
        tree = self._parse_html_content(content)
        response = self._get_elements_from_tree(tree)
        return response


class Testers:
    @staticmethod
    def test_crawl():
        try:
            print('################### TESTING CRAWL  --- ##################')
            i = IntsightsCrawler()
            i.crawl()
        except Exception:
            raise Exception('Problem while crawling site')


def main():
    Testers.test_crawl()


if __name__ == '__main__':
    main()
