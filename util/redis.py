#coding=utf-8
__author__ = 'jclin'
SIMULATE_REDIS_DEBUG = True

import json
import time
import threading

if not SIMULATE_REDIS_DEBUG:
    from django.core.cache import cache

class thread_class(object):
    def __init__(self,func,args,name=''):
        self.func=func
        self.name=name
        self.args=args

    def __call__(self):
        apply(self.func,self.args)

def threadBody(obj):
    '''
    移除超时的key 数据
    '''
    
    while not obj.STOP_REDIS:
        time.sleep(obj.REDIS_LOOP_DURATION)
        obj.objs_locker.acquire()
        for key in obj.SIMULATE_REDIS.keys():
            currentTime = time.time()
            setTime = obj.SIMULATE_REDIS[key]["setTime"]
            expire = obj.SIMULATE_REDIS[key]['expire']
            if currentTime - setTime > expire:
                obj.SIMULATE_REDIS.pop(key)
        obj.objs_locker.release()

class CSimulateRedis(object):

    objs = {}
    objs_locker = threading.Lock()
    SIMULATE_REDIS = {}
    STOP_REDIS = False
    REDIS_LOOP_DURATION = 60
    REDIS_START = False

    def __new__(cls, *args, **kwargs):
        if cls in cls.objs:
            return cls.objs[cls]
        else:
            cls.objs[cls] = object.__new__(cls)
            return cls.objs[cls]

    def __init__(self):
        try:
            thread = threading.Thread(target=thread_class(threadBody,(self,),"SimulateRedisThread"))
            thread.start()
            print "threading SimulateRedisTread start success"
        except:
            print 'threading SimulateRedisThread start error'

    @classmethod
    def simulateRedisCheckStart(cls):
        if not cls.REDIS_START:
            CSimulateRedis()
            cls.REDIS_START = True


    @classmethod
    def simulateRedisGet(cls,key):
        '''
        redis模拟器 获取值
        '''
        cls.simulateRedisCheckStart()
        cls.objs_locker.acquire()
        if key in cls.SIMULATE_REDIS.keys():
            currentTime = time.time()
            setTime = cls.SIMULATE_REDIS[key]["setTime"]
            expire = cls.SIMULATE_REDIS[key]['expire']
            if currentTime - setTime > expire:
                cls.SIMULATE_REDIS.pop(key)
                cls.objs_locker.release()
                return None
            else:
                value = cls.SIMULATE_REDIS[key]['value']
                cls.objs_locker.release()
                return value
        else:
            cls.objs_locker.release()
            return None

    @classmethod
    def simulateRedisSet(cls,key,value,expire_timeout):
        '''
        redis模拟器设置值
        '''
        cls.simulateRedisCheckStart()
        currentTime = time.time()
        data = {"value":value,"setTime":currentTime,"expire":expire_timeout}
        cls.objs_locker.acquire()
        cls.SIMULATE_REDIS.update({key:data})
        cls.objs_locker.release()

    @classmethod
    def simulateRedisUpdate(cls,key):
        '''
        redis模拟器更新数据
        '''
        cls.simulateRedisCheckStart()
        cls.objs_locker.acquire()
        if key in cls.SIMULATE_REDIS.keys():
            currentTime = time.time()
            setTime = cls.SIMULATE_REDIS[key]['setTime']
            expire = cls.SIMULATE_REDIS[key]['expire']
            if currentTime - setTime > expire:
                cls.SIMULATE_REDIS.pop(key)
                cls.objs_locker.release()
                print 'expire timeout'
                return False
            else:
                cls.SIMULATE_REDIS[key]['expire'] = currentTime
                cls.objs_locker.release()
                print 'update success'
                return True
        else:
            cls.objs_locker.release()
            print 'key not found'
            return False

    @classmethod
    def simulateRedisDelete(cls,key):
        '''
        删除dedis数据
        '''
        cls.simulateRedisCheckStart()
        cls.objs_locker.acquire()
        if key in  cls.SIMULATE_REDIS.keys():
            cls.SIMULATE_REDIS.pop(key)
            cls.objs_locker.release()
            return True
        else:
            cls.objs_locker.release()
            return False





def readFromCache(key):
    '''
    从redis读取数据
    对外接口
    '''
    if SIMULATE_REDIS_DEBUG:
        return CSimulateRedis.simulateRedisGet(key)
    else:
        print 'readfrom cache'
        value = cache.get(key)
        if value == None:
            data = None
        else:
            data = value
        print 'readfrom success'
        return data

def writeToCache(key,data,expire):
    '''
    写入redis
    对外接口
    '''
    # CSimulateRedis()# 实例化simulateRedis 对象
    if SIMULATE_REDIS_DEBUG:
        return CSimulateRedis.simulateRedisSet(key,data,expire)
    else:
        cache.set(key,data,expire)

def updateToCache(key,expire):
    print 'update......'
    if SIMULATE_REDIS_DEBUG:
        return CSimulateRedis.simulateRedisUpdate(key)
    else:
        data = cache.get(key)
        cache.set(key,data,expire)


def deleteCache(key):
    if SIMULATE_REDIS_DEBUG:
        return CSimulateRedis.simulateRedisDelete(key)
    else:
        print "del  cache cache"
        cache.delete(key)
        print "del cache end"
        value = cache.get(key)
        print "get cache end"
        if value == None:
            return True
        else:
            return False



