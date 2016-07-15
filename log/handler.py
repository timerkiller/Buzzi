# -*- coding:utf-8 -*-
__author__ = 'jclin'
import logging
import os,os.path
import datetime

class CLoggerHandler(logging.Handler):
    '''
    自定义logger handler 模块
    '''
    def __init__(self,filefmt = None):
        if filefmt == None:
            self.filefmt = os.path.join("logs","%Y-%m-%d","%H.log")
        else:
            self.filefmt = filefmt
        logging.Handler.__init__(self)

    def emit(self, record):
        '''
        log 写文件接口
        该接口可以文件可以改成定期flush，跟换文件的时候再关闭上一次的文件，提供接口效率
        '''
        msg = self.format(record)
        _filePath=datetime.datetime.now().strftime(self.filefmt)
        _dir=os.path.dirname(_filePath)
        try:
            if os.path.exists(_dir) is False:
                os.makedirs(_dir)
        except Exception,e:
            print 'can not make dirs',e
            print 'filepath is ' + _filePath
            return
        try:
            log=open(_filePath,'a')
            log.write(msg)
            log.write("\n")
            log.flush()
            log.close()
        except Exception ,e:
            print "can not write to file",e
            print "filepath is "+_filePath
            pass

