#!/usr/bin/python3
# -*- coding:UTF-8 -*-
from datetime import datetime
from io import BytesIO
from urllib.request import urlretrieve

import pyperclip
import requests
import yagmail as email
from PIL import Image

import ConfigUtility
from Config import logger

config = ConfigUtility.Config(config_path=r'./Config/Config_Use.ini')
MailToList = list(filter(None, str(config.read(config_section='Email', config_option='MailToList')).split('|')))
Key = config.read(config_section='Key', config_option='Key')
DefaultWidth = int(config.read(config_section='DailyPaper', config_option='DefaultWidth'))
DefaultHeight = int(config.read(config_section='DailyPaper', config_option='DefaultHeight'))
city_name = config.read(config_section='DailyPaper', config_option='city_name')
max_retry = int(config.read(config_section='DailyPaper', config_option='max_retry'))


# 核心数据请求
def get():
	try:
		api_list = {'weather': f'http://api.tianapi.com/txapi/tianqi/index?key={Key}&city={city_name}',
		            'bulletin': f'http://api.tianapi.com/bulletin/index?key={Key}',
		            'journalism': f'http://api.tianapi.com/generalnews/index?key={Key}&num=10',
		            'it_news': f'http://api.tianapi.com/it/index?key={Key}&num=10',
		            'sentence': f'http://api.tianapi.com/txapi/dictum/index?key={Key}&num=1'
		            }
		res_list = {
			'weather': None,
			'bulletin': None,
			'journalism': None,
			'it_news': None,
			'sentence': None
		}
		for api in api_list.items():
			module, url = api
			res = request(url)
			retry = 1
			while not res:
				if retry <= max_retry:
					logger.error(msg=f"请求 {module} [ {url} ] 出现网络出现波动，请在重试第 {retry} 次！")
					res = request(url)
					retry += 1
				else:
					logger.critical(msg=f"网络访问异常！")
					break
			if res:
				res = res.json()
				if res['code'] == 200 and res['msg'] == 'success':
					res_list[module] = res['newslist']
				else:
					logger.error(msg=f'请求失败\n{res}')
		return res_list
	except Exception as e:
		logger.error(e)


# Http请求
def request(url):
	try:
		res = requests.get(url)
		if res:
			return res
		else:
			return None
	except Exception as e:
		logger.error(msg=e)
		return None


# 剪贴板操作
def SetClipBoard(text):
	try:
		pyperclip.copy(text)
	except Exception as e:
		logger.error(e)


# 时间戳操作
def Today(strftime="%Y%m%d"):
	return datetime.now().strftime(strftime)


# 获取日期和星期几
def DayOfWeek():
	weekday = {0: "星期天", 1: "星期一", 2: "星期二", 3: "星期三", 4: "星期四", 5: "星期五", 6: "星期六"}
	today = datetime.today()
	week = weekday.get(today.weekday())
	date = today.strftime("%Y-%m-%d")
	return date, week


# 加载图片
def LoadImage(image_url: str):
	res = request(image_url)
	retry = 1
	while not res:
		logger.error(msg=f"请求 [ {image_url} ] 出现网络出现波动，请在重试第 {retry} 次！")
		if retry <= max_retry:
			res = request(image_url)
			retry += 1
		else:
			logger.critical(msg=f"网络访问异常！")
			return res
	image = Image.open(BytesIO(res.content))
	return image


# 下载图片
def DownloadImage(immage_url: str, image_name: str):
	try:
		path, message = urlretrieve(immage_url, f'./Export/{image_name}.png')
		return path
	except Exception as e:
		logger.error(e)


# 发送邮件
def sendMail(to=MailToList, subject=None, contents=None, attachments=None, cc=None, bcc=None, preview_only=False, headers=None, newline_to_break=True):
	user = config.read(config_section='Email', config_option='user')
	password = config.read(config_section='Email', config_option='password')
	host = config.read(config_section='Email', config_option='host')
	port = config.read(config_section='Email', config_option='port')
	try:
		with email.SMTP(user=user, password=password, host=host, port=port) as m:
			m.send(to=to, subject=subject, contents=contents, attachments=attachments, cc=cc, bcc=bcc, preview_only=preview_only, headers=headers, newline_to_break=newline_to_break)
			logger.info(f'邮件发送成功！to：{to}')
	except Exception as e:
		logger.error(e)

