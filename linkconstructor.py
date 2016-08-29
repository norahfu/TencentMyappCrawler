#-*- coding: UTF-8 -*-
__author__ = 'Norah'
import argparse
import seedsmanager
from lxml import html
from Utils import Utils

import sys
import errno
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

class linkconstructor():
    def __init__(self):
        params ={}
        params['server'] = 'localhost'
        params['port'] = '27017'
        params['database'] = 'Myappseedsurl'
        params['username'] = 'test'
        params['password'] = 'test'
        params['seed_collection'] = 'Myapps_QueuedApps_2016_08_26'
        params['auth_database'] = 'Myappseedsurl'
        params['write_concern'] = True
        self._params = params

    def scroll(self,driver):
        driver.execute_script("""
            (function () {
                var y = document.body.scrollTop;
                var step = 100;
                window.scroll(0, y);


                function f() {
                    if (y < document.body.scrollHeight) {
                        y += step;
                        window.scroll(0, y);
                        setTimeout(f, 50);
                    }
                    else {
                        window.scroll(0, y);
                        document.title += "scroll-done";
                    }
                }

                setTimeout(f, 1000);
            })();
            """)
    def get_arguments_parser(self):
        parser = argparse.ArgumentParser(description='Linkconstructor phase of \
                                                     the Myapp \
                                                     Store Crawler')
        parser.add_argument('seeds',
                            type=file,
                            help='Path to the xml containing the seeds\
                                   terms that should be loaded')

    def assemble_post_url(self, keyword):
        """ Format Search Url based on the keyword received """

        return 'http://sj.qq.com/myapp/search.htm?kw={0}'.format(keyword)

    def assemble_app_category_url(self,category):
        return 'http://sj.qq.com/myapp/category.htm?orgame=1&categoryId={0}'.format(category)

    def assemble_game_category_url(self,category):
        return 'http://sj.qq.com/myapp/category.htm?orgame=2&categoryId={0}'.format(category)


    def fix_url(self, url):
        """ Fix relative Urls by appending the prefix to them """

        url_prefix = 'http://sj.qq.com/myapp/'
        return "{0}{1}".format(url_prefix, url)

    def parse_app_urls(self, page_text, xpath):
        """
        Extracts urls out of a HTML search page result,
        taking care of duplicates
        """
        # Set tree for html formatting
        tree = html.fromstring(page_text)

        # Xpath parsing

        urls = tree.xpath(xpath)

        # Sanity check
        if urls is None or len(urls) == 0:
            yield None

        # Go on each node looking for urls
        url_prefix = 'http://sj.qq.com/myapp/'
        for node in urls:
            if "href" in node.attrib and "detail.htm?apkName=" in node.attrib["href"]:
                url = node.attrib["href"]
                '''
                if (url.index('myapp')):
                    url = url[9:]
                '''
                yield "{0}{1}".format(url_prefix, url)
    '''
    scroll the page to load whole page until find keyword"没有更多了"
    '''
    def load_whole_page(self,url):

        service_args = [
            '--load-images=no'
        ]
        browser = webdriver.PhantomJS(service_args=service_args)

        #browser = webdriver.Chrome()
        browser.set_page_load_timeout(30)
        try:
            browser.get(url)
            print ("crawling %s ......" %url)
        except Exception as e:
            print "oops something wrong"+e
            #if errors detected. rest for 10minutes
            time.sleep(600)

       #scroll the page to load more
        maxtime = 30
        timecount = 0
        while True:
            try:
                self.scroll(browser)
                time.sleep(1)

                timecount += 1
                ec = EC.text_to_be_present_in_element((By.CLASS_NAME, 'load-more-btn'), u'没有更多了')
                if ec.__call__(browser):
                    break
                else:
                    if timecount > maxtime:

                        break
                    else:
                        pass
            except Exception as e:
                print e
                break
        whole_page = browser.page_source

        browser.close()


        return whole_page


    def construct_by_search(self,keyword):

        parsed_url = self.assemble_post_url(keyword)
        whole_page = self.load_whole_page(parsed_url)

        xpath ="//div[@class='icon-margin']/a[@class='icon' and \
                @target='_blank']"
        for url in self.parse_app_urls(whole_page, xpath):
            if url in parsed_urls:
                return

            self._mongo_wrapper.insert_on_queue(url)
            parsed_urls.add(url)


    def start_construct(self):
        seeds = seedsmanager.seedsmanager()
        seeds.initialize_seed_class()

        if not Utils.configure_mongodb(self,**self._params):

            sys.exit(errno.ECONNREFUSED)

        for keyword in seeds.get_words():

            self.construct_by_search(keyword)


if __name__ == "__main__":
    parsed_urls = set()
    linkconstructor = linkconstructor()
    linkconstructor.start_construct()
