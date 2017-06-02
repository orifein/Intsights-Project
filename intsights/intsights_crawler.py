import lxml 
import requests
import arrow
import json
import tinydb
from lxml import etree
from io import StringIO, BytesIO
from intsights_model import IntsightsModel
print (lxml.__file__)

class IntsightsCrawler():
    AUTHOR_NAMES_CONST =['Guest', 'Unknown', 'Anonymous']
    
    
    BASE_URL = 'file:///Users/orifein/Downloads/StrongholdPaste.html'
    ALL_ROWS_ELEMENTS = '#list .col-sm-12'


    def _get_content_from_html(self):
        http_parse = requests.get(self.BASE_URL)
        content_string = http_parse.text
        
        return content_string

    def _parse_html_content(self,content):
        parser = etree.HTMLParser();
        tree =  etree.parse(StringIO(content),parser)
        return tree
    def _fetch_date_and_author_from_element(self,element):
        print('lala')
    
        element_text = element.cssselect('.pre-footer')[0]
        
        fetched_text = ''.join([x.replace('\n','').replace('\t','') for x in element_text.itertext()])
        fetched_text_splitted = fetched_text.replace(',','').split(' ')
    
        author = fetched_text_splitted[2]
        
        if author in self.AUTHOR_NAMES_CONST:
            author = 'Anonymous'
        
        date = arrow.get(fetched_text_splitted[6]+'-'+fetched_text_splitted[5]+'-'+fetched_text_splitted[4]+' '+fetched_text_splitted[7],'YYYY-MMM-DD HH:mm:ss')
    
        return author,date
    
    def _get_elements_from_tree(self,tree):
        list_of_models = []
        
        
        
        html_root = tree.getroot()
        
        all_rows = html_root.cssselect(self.ALL_ROWS_ELEMENTS)
        
        for element in all_rows:
            
            response = IntsightsModel()
            got_title = element.cssselect('h4')
            content_text = element.cssselect('.well-sm')
            if not got_title:
                continue
            
            
            response.title = got_title[0].text.replace('\n','').replace('\t','')
            response.content = ''.join([txt.replace('\n','').replace('\t','') for txt in content_text[0].itertext()])
            response.author,response.date = self._fetch_date_and_author_from_element(element)
            
            list_of_models.append(response)
            
  
        list_of_models.sort(key=lambda model: model.date,reverse=True) ##sorting all by dates
        for paste_model in list_of_models:
            
            paste_model.date = str(paste_model.date)
        
        return list_of_models
    
    
    
    def crawl(self):
        
#         content = self._get_content_from_html()
        enc='utf-8'
        content = open('/Users/orifein/Downloads/StrongholdPaste.html',encoding=enc).read()
        
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