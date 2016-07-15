# -*- coding:utf-8 -*-
__author__ = 'jclin'
import logging
import ctypes
import platform
from handler import CLoggerHandler


class CMyLog(object):
    '''
    自定义log类
    '''
    _objs = {}
    _logger = None
    _fileHandler = None
    _consoleHandler = None

    class Meta():
        FOREGROUND_WHITE = 0x0007
        FOREGROUND_BLUE = 0x01 # text color contains blue.
        FOREGROUND_GREEN= 0x02 # text color contains green.
        FOREGROUND_RED  = 0x04 # text color contains red.
        FOREGROUND_YELLOW = FOREGROUND_RED | FOREGROUND_GREEN

    def __new__(cls, *args, **kwargs):
        if cls in cls._objs:
            return cls._objs[cls]
        else:
            cls._objs[cls] = object.__new__(cls)
            return cls._objs[cls]

    def __init__(self):
        self.init()

    @classmethod
    def init(cls):
        print 'log init .... '
        cls._logger = logging.getLogger()
        cls._logger.setLevel(logging.INFO)
        formatter = logging.Formatter('<%(asctime)s> %(levelname)s/%(module)s/%(funcName)s, Line:%(lineno)d: %(message)s')
        #写文件handler
        cls._fileHandler = CLoggerHandler()
        cls._fileHandler.setFormatter(formatter)
        #控制台handler
        cls._consoleHandler = logging.StreamHandler()
        cls._consoleHandler.setFormatter(formatter)
        cls._logger.addHandler(cls._fileHandler)
        cls._logger.addHandler(cls._consoleHandler)
        print 'log init success'

    @classmethod
    def getLogger(cls):
        if not cls._objs:
            print ('CmyLog instance start....')
            CMyLog()
        return cls._logger

    @classmethod
    def setColor(cls,color, platform):
        if platform == "Linux":
            formatter = None
            if color == cls.Meta.FOREGROUND_RED:
                formatter = logging.Formatter('\033[1;31;40m <%(asctime)s> %(levelname)s/%(module)s/%(funcName)s, Line:%(lineno)d: %(message)s \033[0m')
            elif color == cls.Meta.FOREGROUND_WHITE:
                formatter = logging.Formatter('\033[1;37;40m <%(asctime)s> %(levelname)s/%(module)s/%(funcName)s, Line:%(lineno)d: %(message)s \033[0m')
            elif color == cls.Meta.FOREGROUND_YELLOW:
                formatter = logging.Formatter('\033[1;33;40m <%(asctime)s> %(levelname)s/%(module)s/%(funcName)s, Line:%(lineno)d: %(message)s \033[0m')
            elif color == cls.Meta.FOREGROUND_GREEN:
                formatter = logging.Formatter('\033[1;32;40m <%(asctime)s> %(levelname)s/%(module)s/%(funcName)s, Line:%(lineno)d: %(message)s \033[0m')
            elif color == cls.Meta.FOREGROUND_BLUE:
                formatter = logging.Formatter('\033[1;31;40m <%(asctime)s> %(levelname)s/%(module)s/%(funcName)s, Line:%(lineno)d: %(message)s \033[0m')
            else:
                formatter = logging.Formatter('<%(asctime)s> %(levelname)s/%(module)s/%(funcName)s, Line:%(lineno)d: %(message)s')
            cls._fileHandler.setFormatter(formatter)
            cls._consoleHandler.setFormatter(formatter)
            return True