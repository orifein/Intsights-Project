import requests
import arrow
from lxml import etree
from io import StringIO
from intsights_model import IntsightsModel
from base_logger import BaseLogger
import os


LOG_FORMAT = '[%(asctime)s %(levelname)s]: %(message)s'
FILE_DIRECTORY = os.path.dirname(__file__)
LOGS_FOLDER = os.path.join(FILE_DIRECTORY, 'logs')


class IntsightsCrawler():
    AUTHOR_NAMES_CONST = ['Guest', 'Unknown', 'Anonymous']
    BASE_URL = 'http://nzxj65x32vh2fkhk.onion/all'
    ALL_ROWS_ELEMENTS = '//section[@id="list"]//div[@class="col-sm-12"]'
    WINDOWS_URL = 'file:///C:/Users/orif/Desktop/StrongholdPaste.htm'
    TITLE_ELEMENT_IN_ROWS = './/h4'
    TEXT_CONTENT_IN_ROWS = './/div[contains(@class,"well-sm")]'
    AUTHOR_AND_DATE_IN_ROWS = './/div[contains(@class,"pre-footer")]'

    def __init__(self):
        log_file_path = os.path.join(LOGS_FOLDER, 'logger.log')
        self.logger = BaseLogger().create_logger('crawler_logger', log_file_path, LOG_FORMAT)
    
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
        element_text = element.xpath(self.AUTHOR_AND_DATE_IN_ROWS)[0]
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
        all_rows = html_root.xpath(self.ALL_ROWS_ELEMENTS)
        self.logger.debug('Found {} rows , now will fetch info of every row'.format(len(all_rows)-1))
        for element in all_rows:
            
            response = IntsightsModel()
            got_title = element.xpath(self.TITLE_ELEMENT_IN_ROWS)
            txt_cont = element.xpath(self.TEXT_CONTENT_IN_ROWS)
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
        self.logger.debug('Finished Getting all rows - now sorting them by date')
        list_of_models.sort(key=lambda model: model.date, reverse=True)
        for paste_model in list_of_models:
            paste_model.date = str(paste_model.date)
        self.logger.debug('Finished all evaluation - return response')
        return list_of_models

    def _get_proxy_for_onion_sites(self):
        session = requests.session()
        session.proxies = {'http':  'socks5h://localhost:9050',
                           'https': 'socks5h://localhost:9050'}
        return session

    def crawl(self):
        self.logger.debug('Getting proxy for onion sites')
        session = self._get_proxy_for_onion_sites()
        self.logger.debug('Dont getting proxy for onion sites')
        self.logger.debug('Getting onion site by request method')
        response = session.get(self.BASE_URL)
        self.logger.debug('Done getting onion site')
        if response.status_code != 200:
            self.logger.error('Problem with site - got status code != 200  - exiting')
            raise Exception('Problem Fetching site - got error code : {} - raising exception'.format(response.status_code))
        content = response.text
    
        tree = self._parse_html_content(content)
        self.logger.debug('Getting elements from tree')
        response = self._get_elements_from_tree(tree)
        return response


class Testers:
    @staticmethod
    def test_crawl():
        try:
            print('################### TESTING CRAWL  --- ##################')
            i = IntsightsCrawler()
            response=i.crawl()
            print(response)
        except Exception:
            raise Exception('Problem while crawling site')
        
def main():
    Testers.test_crawl()

if __name__ == '__main__':
    main()
