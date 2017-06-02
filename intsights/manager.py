import arrow
from base_logger import BaseLogger
from tinydb import TinyDB, Query
from repeated_timer import RepeatedTimer


db = TinyDB('db3.json')

class CrawlerManager(object):


    def __init__(self,):
        self.launch_time = arrow.utcnow()
        self.action = ''
        self.running_crawler = None
        self.timer = None
        self.logger = BaseLogger().create_logger('intsights')
        print('lala')
        
        
        
        
    
    def do_work(self):
        try:
            self.action = 'crawl_site'
            self._execute(self.action)
            
            
            


        except:
            self.logger.debug('CrawlerManager Error')
        
        
    def start(self):
        if self.timer is not None:
            self.logger.info('Manager is still running')
        else:
            self.logger.info('First time work - startinf')

            self.timer = RepeatedTimer(10,CrawlerManager.do_work,self)
            
            
            
    def _get_crawler(self):
        package = 'intsights_crawler'
        class_name = 'IntsightsCrawler'
        module_handle = __import__(package)
        class_handle = getattr(module_handle,class_name)
    
        class_obj = class_handle()
        self.running_crawler = class_obj
        return self.running_crawler
    
    def crawl_site(self):
        User = Query()
        crawler = self._get_crawler()
        
        
        try:
            response = crawler.crawl()
            updated_item = 0
            for item in response:
                item_dict = item.__dict__
                if db.search(User.date == item_dict['date']):
                    continue
                updated_item+=1
                db.insert(item_dict)
                
            self.logger.debug('Finished Updating DB, updated rows number: {}'.format(updated_item))   
            print('lala')
            
        except Exception as e:
            
            self.logger.exception('Problem with crawling - getting out')
    
    
    def _execute(self,action):
        if hasattr(self,action):
            getattr(self,action)()
            
        else:
            raise Exception('No action named like this - going out')
        
    
   