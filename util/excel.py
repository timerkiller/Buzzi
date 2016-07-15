#coding=utf-8
from django.template import loader,Context
from django.http import HttpResponse
import xlwt
import xlrd
from cStringIO import StringIO
import os
import time
from django.db.models import Q

class CExeclOperationBase(object):

    m_objectModel = None

    class Meta:
        m_normalData = 0
        m_invalidData = 1

    def __init__(self,model):
        print 'in CExeclOperationBase'
        self.m_objectModel = model

    def importExcelData(self, file):
        try:
            path = "media/xls" + time.strftime('/%Y-%m-%d %H.%M.%S/')
            if not os.path.exists(path):
                os.makedirs(path)
                file_name = path + file.name
                destination = open(file_name, 'wb+')
                for chunk in file.chunks():
                    destination.write(chunk)
                destination.close()
                result = self.excelDataToDataBase(file_name)
                return result
        except Exception, e:
            return e
        return "success"

    def exportExcelData(self, file):
        pass

    def excelDataToDataBase(self, path):
        try:
            data = xlrd.open_workbook(path)
        except:
            return "openFailed"
        table = data.sheets()[0]
        nrows = table.nrows #行数
        targetModelObjList =[]
        for rowNumber in range(0,nrows):
            row = table.row_values(rowNumber)
            if rowNumber == 0:
                result = self.checkDataIsValid(row)
                if result == self.Meta.m_invalidData:
                    return "failed"
                elif result == self.Meta.m_normalData:
                    continue
            if row:
                targetModelObj = self.operateTargetModel(row)
                if targetModelObj != None:
                    targetModelObjList.append(targetModelObj)
        self.m_objectModel.objects.bulk_create(targetModelObjList)
        return "success"

    def databaseToExcelData(self):
        pass

    def checkDataIsValid(self,firstRow):
        pass

    #需要被重载
    def operateTargetModel(cls, row):
        pass

from mainApp.models.C4SModels import C4SShopModel,CRegistationCodeModel


class CExcelOperationForResisterCodeModel(CExeclOperationBase):
    '''
    注册码表格导入导出类
    '''
    m_shop4sName = None
    m_shopObj = None
    def __init__(self,shop):
        print 'in CExcelOperationForResisterCodeModel init'
        self.m_shop4sName = shop
        try:
            self.m_shopObj = C4SShopModel.objects.get(title=shop)
        except Exception,e:
            print "CExcelOperationForResisterCodeMode:",e

        super(CExcelOperationForResisterCodeModel, self).__init__(model=CRegistationCodeModel)

    def operateTargetModel(self,row):
        print row
        try:
            code = self.m_objectModel.objects.get(shop = self.m_shopObj,code=row[0])
            print ('code has exist now')
            return None
        except:
            registerCodeObj = self.m_objectModel()
            registerCodeObj.code = row[0]
            if row[1].encode('utf-8') == "no":
                registerCodeObj.isUsed = False
            else:
                registerCodeObj.isUsed = True

            registerCodeObj.shop = self.m_shopObj
            return registerCodeObj

    def checkDataIsValid(self,firstRow):
        print "----------->",firstRow[0]
        if firstRow[0].encode('utf-8') == "RegisterCode":
            return self.Meta.m_normalData
        else:
            return  self.Meta.m_invalidData