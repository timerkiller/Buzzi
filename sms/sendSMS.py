# -*- coding: utf8 -*-
# 文件名称：sendSMS.py
# 
#Return Code										Description
#success:msgid								提交成功，发送状态请见4.1
#error:msgid								提交失败
#error:Missing username						用户名为空
#error:Missing password						密码为空
#error:Missing apikey						APIKEY为空
#error:Missing recipient					手机号码为空
#error:Missing message content				短信内容为空
#error:Account is blocked					帐号被禁用
#error:Unrecognized encoding				编码未能识别
#error:APIKEY or password error				APIKEY 或密码错误
#error:Unauthorized IP address				未授权 IP 地址
#error:Account balance is insufficient		余额不足
#error:Black keywords is:党中央				屏蔽词
import httplib, urllib
httpClient = None

#用户名
username = 'qinghuadaxue'
#密码
password = 'ml160321'
#APIKEY,请向销售或技术人员索取
apikey = '94b7f93d13a4666accc666224120b176'

def sendSMS(phoneNum,code):
	try:
		content = "您的验证码是："+code
		msg = content.decode('utf-8','ignore').encode('gbk','ignore')
		print msg
		params = urllib.urlencode({'username': username, 'password': password, 'apikey': apikey, 'mobile': phoneNum, 'content': msg})
		headers = {"Content-type": "application/x-www-form-urlencoded"
						, "Accept": "text/plain"}

		httpClient = httplib.HTTPConnection("m.5c.com.cn", 80, timeout=30)
		httpClient.request("POST", "/api/send/index.php", params, headers)
		response = httpClient.getresponse()	
		print response
	except Exception, e:
		print e
	finally:
		if httpClient:
			httpClient.close()

#sendSMS('13750821660','12354')