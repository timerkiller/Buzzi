# -*- coding:utf-8 -*-
__author__ = 'jclin'
import logging
import ctypes
import platform
from handler import CLoggerHandler

STD_OUTPUT_HANDLE= -11
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

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
    def setColor(cls,color, platform,handle=std_out_handle):
        if platform == "Windows":
            try:
                bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
                return bool
            except:
                pass


