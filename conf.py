#!/usr/bin/env python
# encoding: utf-8

import ConfigParser

class Conf(object):
    def __init__(self, config_file):
        self.conf = ConfigParser.ConfigParser()
        self.conf.readfp(open(config_file))
        self.sectionName = 'default'

    def getBaseUrl(self):
        if self.conf.has_section(self.sectionName):
            return self.conf.get(self.sectionName, 'base_url')

    def getKey(self):
        if self.conf.has_section(self.sectionName):
            return self.conf.get(self.sectionName, 'key')

if __name__ == "__main__":
    conf = Conf('config')
    print conf.getBaseUrl()
    print conf.getKey()
