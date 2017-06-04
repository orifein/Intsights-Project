import arrow
from base_logger import BaseLogger
from tinydb import TinyDB, Query
from repeated_timer import RepeatedTimer
import os
db = TinyDB('db.json')
INTERVAL = 14400  # 14400 Seconds is 4Hours, Yep


FMT = '[%(asctime)s %(levelname)s]: %(message)s'
FILE_DIRECTORY = os.path.dirname(__file__)
LOGS_FOLDER = os.path.join(FILE_DIRECTORY, 'logs')


class CrawlerManager(object):
    def __init__(self,):
        self.launch_time = arrow.utcnow()
        self.action = ''
        self.running_crawler = None
        self.timer = None
        path = os.path.join(LOGS_FOLDER, 'logger.log')
        self.logger = BaseLogger().create_logger('manager_logger', path, FMT)

    def do_work(self):
        try:
            self.action = 'crawl_site'
            self._execute(self.action)
        except Exception:
                raise

    def start(self):
        if self.timer is not None:
            self.logger.info('Manager is still running')
        else:
            self.logger.info('First time work - starting')
            self.do_work()
            self.logger.debug('Finished first work- now wait for interval')
            self.timer = RepeatedTimer(INTERVAL, CrawlerManager.do_work, self)

    def stop(self):
        if self.timer is not None and self.timer.is_alive():
            self.timer.stop_timer()
            self.timer = None

    def _get_crawler(self):
        package = 'intsights_crawler'
        class_name = 'IntsightsCrawler'
        module_handle = __import__(package)
        class_handle = getattr(module_handle, class_name)
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
                    self.logger.debug('No Updates- wait for next interval')
                    break
                updated_item += 1
                db.insert(item_dict)
            if updated_item > 0:
                self.logger.debug('Updated rows {}'.format(updated_item))
        except Exception:
            raise

    def _execute(self, action):
        if hasattr(self, action):
            getattr(self, action)()
        else:
            raise Exception('No action named like this - going out')
