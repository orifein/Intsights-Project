'''
Created on 2 Jun 2017

@author: orifein
'''
from manager import CrawlerManager


def run():
    manager = CrawlerManager()
    try:
        manager.start()
    except KeyboardInterrupt:
        manager.stop()


if __name__ == '__main__':
    run()
