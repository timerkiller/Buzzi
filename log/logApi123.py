__author__ = 'jclin'
# from .core import CMyLog
#from .coreLinux import CMyLogLinux

import platform

if 'Windows' in platform.system():
    from log_lib import core as log_core
    SYS_LOG = log_core.CMyLog.getLogger()
    currentPlatform = "Windows"
if 'Linux' in platform.system():
    from log_lib import coreLinux as log_core
    SYS_LOG = log_core.CMyLog.getLogger()
    currentPlatform = "Linux"

FOREGROUND_WHITE = 0x0007
FOREGROUND_BLUE = 0x01 # text color contains blue.
FOREGROUND_GREEN= 0x02 # text color contains green.
FOREGROUND_RED  = 0x04 # text color contains red.
FOREGROUND_YELLOW = FOREGROUND_RED | FOREGROUND_GREEN


class CPlatformLogger(object):
    @classmethod
    def isWindowsSystem(cls):
        if 'Windows' in platform.system():
            return True
        else:
            return False

    @classmethod
    def isLinuxSystem(cls):
        if 'Linux' in platform.system():
            return True
        else:
            return False

    @classmethod
    def getPlatform(cls):
        return log_core.CMyLog.getLogger(), currentPlatform,log_core.CMyLog

class CLog(object):
    SYS_LOG,_platform,_Log = CPlatformLogger.getPlatform()

    @classmethod
    def debug(cls):
        cls._Log.setColor(FOREGROUND_GREEN,cls._platform)
        return cls.SYS_LOG#.debug(message,*args, **kwargs)

    @classmethod
    def info(cls):
        cls._Log.setColor(FOREGROUND_WHITE,cls._platform)
        return cls.SYS_LOG#cls.SYS_LOG.info(message,*args, **kwargs)

    @classmethod
    def warn(cls):
        cls._Log.setColor(FOREGROUND_YELLOW,cls._platform)
        return cls.SYS_LOG#.warn(message,*args, **kwargs)

    @classmethod
    def error(cls):
        print  ">>>>>>>>>>>>>in error"
        cls._Log.setColor(FOREGROUND_RED,cls._platform)
        return cls.SYS_LOG #cls.SYS_LOG.error(message,*args, **kwargs)

    @classmethod
    def critical(cls):
        cls._Log.setColor(FOREGROUND_BLUE,cls._platform)
        return cls.SYS_LOG #.critical(message,*args, **kwargs)

def test():
    CSysLog.info("123")


def setColor(type):
    def setErrorColor(func):
        def wrapper(*arg,**kargs):
            log_core.CMyLog.setColor(FOREGROUND_RED,currentPlatform)
            func(*arg,**kargs)
        return wrapper

    def setWarnColor(func):
        def wrapper(*arg,**kargs):
            log_core.CMyLog.setColor(FOREGROUND_YELLOW,currentPlatform)
            func(*arg,**kargs)
        return wrapper

    return {'error':setErrorColor,'warn':setWarnColor}[type]

class CSysLog(object):

    
    info= CLog.info().info

    critical= CLog.critical().critical

    warn= CLog.warn().warn

    debug= CLog.debug().debug