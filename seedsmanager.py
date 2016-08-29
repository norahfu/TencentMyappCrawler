#-*- coding: UTF-8 -*-
__author__ = 'Norah'

import string
import urllib
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class seedsmanager():
    def __init__(self):
        self._english_characters = []
        self._chinese_characters = []

    def initialize_seed_class(self):
        self._init_english_characters()
        self._init_chinese_characters()

    def _init_english_characters(self):
        """Initializes a list of all the characters from 'a' to 'z'"""

        [self._english_characters.append(x) for x in string.ascii_lowercase]

    def _init_chinese_characters(self):
        f = open('./ChineseCharacters','r')
        for line in f.readlines():
            for c in line.split():
                #注意汉字的编码问题,
                self._chinese_characters.append(urllib.quote(c.decode('gbk').encode('utf-8')))
                #self._chinese_characters.append(c.decode('gbk').encode('utf-8'))
        f.close()

    def get_words(self):
        #words = self._characters
        words = []
        #words.extend(self._english_characters)
        words.extend(self._chinese_characters)

        for word in words:
            yield  word