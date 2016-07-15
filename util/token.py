#coding=utf-8
__author__ = 'jclin'
import time
import base64
def generateToken(phone):
    '''
    生成系统唯一token
    '''
    currentTime = time.time()
    strTime = str(currentTime)
    key = phone + strTime
    token = base64.encodestring(key)
    return token


