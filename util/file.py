#coding=utf-8
import time
import os
from CarLocateManage.settings import MEDIA_ROOT
__author__ = 'jclin'
'''文件上传'''
def handle_uploaded_file(f):
    file_name = ""
    try:
        folder = os.path.join('upload',time.strftime('%Y-%m-%d')).replace('\\','/')
        dirpath = os.path.join(MEDIA_ROOT,folder).replace('\\','/')
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        fileAddress = os.path.join(dirpath,f.name).replace('\\','/')
        filename = f.name
        if os.path.exists(fileAddress):
            tmp = f.name.split('.')
            filename = tmp[0] + time.strftime('-%H-%M-%S') + '.' + tmp[1]
        fileAddress = os.path.join(dirpath,filename).replace('\\','/')
        destination = open(fileAddress, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
        file_name = os.path.join(folder,filename).replace('\\','/')
        print file_name
        print fileAddress
    except Exception, e:
        print e
    return file_name
