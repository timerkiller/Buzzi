#coding=utf-8
__author__ = 'jclin'
#分页类
class CPage(object):
    def __init__(self,obj,perPage):
        self.obj = obj
        self.perPage = int(perPage)
        self.counts = len(obj)

    def getPageCounts(self):
        if self.counts % self.perPage > 0:
            pageAll = self.counts / self.perPage +1
        else:
            pageAll = self.counts / self.perPage
        return  pageAll

    def getPageDate(self,page):
        start = self.perPage * (int(page) - 1)
        end = start + self.perPage
        if start > self.counts:
            items = []
        elif end > self.counts:
            items = self.obj[start:self.counts+1]
        else:
            items = self.obj[start:end]
        return items

