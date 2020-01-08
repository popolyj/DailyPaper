#!/usr/bin/python3
# -*- coding:UTF-8 -*-

import os
from datetime import datetime

import pyperclip
import requests
import yagmail as email
from PIL import Image, ImageFont, ImageDraw
import ConfigUtility

config = ConfigUtility.Config(config_path=r'D:\WorkSpace\Project\python\DailyPaper\Config\Config.ini')
user = config.read(config_section='Email', config_option='user')
password = config.read(config_section='Email', config_option='password')
host = config.read(config_section='Email', config_option='host')
port = config.read(config_section='Email', config_option='port')
mail_ls = list(filter(None, str(config.read(config_section='Email', config_option='mail_ls')).split('|')))
key_ls = list(filter(None, str(config.read(config_section='Key', config_option='key_ls')).split('|')))
city_name = config.read(config_section='Weather', config_option='city_name')


# 剪贴板操作
def addToClipBoard(text):
	pyperclip.copy(text)


# 时间戳操作
def get_timestamp():
	return datetime.now().strftime("%Y%m%d")


# 发送邮件
def sendMail(to=None, subject=None, contents=None, attachments=None, cc=None, bcc=None, preview_only=False, headers=None, newline_to_break=True):
	try:
		with email.SMTP(user=user, password=password, host=host, port=port) as m:
			m.send(to=to, subject=subject, contents=contents, attachments=attachments, cc=cc, bcc=bcc, preview_only=preview_only, headers=headers, newline_to_break=newline_to_break)
			print(f'邮件发送成功！to：{to}')
	except Exception as ex:
		print(ex)


# 获取天气，渠道：天行api 72
def get_weather():
	for key in key_ls:
		res = requests.get(url=f'http://api.tianapi.com/txapi/tianqi/index?key={key}&city={city_name}').json()
		if res['code'] == 200 and res['msg'] == 'success':
			return res['newslist'][0]
		else:
			print(res)
	print(f'无可用的key！')
	return None


# 获取新闻，渠道：天行api 117
def get_news():
	for key in key_ls:
		res = requests.get(url=f'http://api.tianapi.com/bulletin/index?key={key}').json()
		if res['code'] == 200 and res['msg'] == 'success':
			return res['newslist']
		else:
			print(res)
	print(f'无可用的key！')
	return None


# 获取名人名言，渠道：天行api 26
def get_word_of_famous_people():
	for key in key_ls:
		res = requests.get(url=f'http://api.tianapi.com/txapi/dictum/index?key={key}&num=1').json()
		if res['code'] == 200 and res['msg'] == 'success':
			return res['newslist'][0]
		else:
			print(res)
	print(f'无可用的key！')
	return None


# 获取日报
# show_digest: bool = False, 是否显示简介，默认为否
# show_url: bool = False, 是否显示超链接，默认为否
# show_image: bool = False, 是否显示图片，默认为否
# send_to_clidBoard: bool = False, 是否复制到剪贴板，默认为否
# send_mail: bool = True，是否发送邮件，默认为是
# 返回daily_lines
def get_daily(show_digest: bool = False, show_url: bool = False, show_image: bool = False, send_to_clidBoard: bool = False, send_mail: bool = True):
	daily_lines = list()
	# 获取天气预报
	res = get_weather()
	if res:
		daily_lines.append(f'******************************')
		daily_lines.append(f"天气预报：[ 城市：{city_name} ]")
		daily_lines.append(f'******************************')
		daily_lines.append(f"日期：{res['date']}")
		daily_lines.append(f"星期：{res['week']}")
		daily_lines.append(f"天气：{res['weather']}")
		daily_lines.append(f"当前温度：{res['real']}")
		daily_lines.append(f"最低温度：{res['lowest']}")
		daily_lines.append(f"最高温度：{res['highest']}")
		daily_lines.append(f"风向：{res['wind']}")
		daily_lines.append(f"风速：{res['windspeed']}")
		daily_lines.append(f"湿度：{res['humidity']}")
		daily_lines.append(f"空气质量指数：{res['air']}")
		daily_lines.append(f"空气质量等级：{res['air_level']}")
		daily_lines.append(f"天气状况提示：{res['tips']}")

	# 今日热点
	res = get_news()
	if res:
		daily_lines.append(f'******************************')
		daily_lines.append(f'今日热点：')
		daily_lines.append(f'******************************')
		for idx, news in enumerate(res, 1):
			daily_lines.append(f"{idx}、{news['title']}")
			if show_digest and news['digest']:
				daily_lines.append(f"--> {news['digest']}")
			if show_url and news['url']:
				daily_lines.append(f"--> {news['url']}")
			if show_image and news['imgsrc']:
				daily_lines.append(f"<img src='{news['imgsrc']}' alt='{news['title']}'>")

	# 每日一句
	res = get_word_of_famous_people()
	if res:
		daily_lines.append(f'******************************')
		daily_lines.append(f'每日一句：')
		daily_lines.append(f'******************************')
		daily_lines.append(f"{res['content']} —— {res['mrname']}")
	if len(daily_lines) > 0:
		content = '\n'.join(daily_lines)
		if send_to_clidBoard:
			addToClipBoard(content)
		if send_mail:
			# 发送邮件
			sendMail(to=mail_ls, subject=f'{get_timestamp()}日报', contents=content)
		return daily_lines


# 文本转图片
def get_img(lines: list):
	if not lines:
		print(f"文本不能为空！")
		return
	font = ImageFont.truetype(os.path.join("fonts", "simkai.ttf"), 18)
	line_dict = dict()
	line_dict['image_height'] = 0
	line_dict['image_width'] = 0
	line_dict['lines'] = list()
	for line in lines:
		font_size = font.getsize(line)
		line_dict['image_height'] += font_size[1] + 5
		if font_size[0] > line_dict['image_width']:
			line_dict['image_width'] = font_size[0] + 20
		ldic = dict()
		ldic['line'] = line
		ldic['line_height'] = font_size[1] + 5
		ldic['line_width'] = line_dict['image_width']
		line_dict['lines'].append(ldic)
	line_dict['image_height'] += 30
	print(f"image_height = {line_dict['image_height']}, image_width = {line_dict['image_width']}")
	im = Image.new("RGB", (line_dict['image_width'], line_dict['image_height']), (255, 255, 255))
	dr = ImageDraw.Draw(im)
	x, y = 10, 10
	for line in line_dict['lines']:
		dr.text((x, y), line['line'], font=font, fill="#000000")
		y += line['line_height']
		print(line)
	im.save(f"Export\\{get_timestamp()}.png")


if __name__ == '__main__':
	# 请在配置顶部参数后，根据实际情况修改传入的参数
	# show_digest: bool = False, 是否显示简介，默认为否
	# show_url: bool = False, 是否显示超链接，默认为否
	# send_to_clidBoard: bool = False, 是否复制到剪贴板，默认为否
	# send_mail: bool = True，是否发送邮件，默认为是
	# 默认返回daily到控制台
	daily = get_daily(show_digest=False, show_url=False, show_image=False, send_to_clidBoard=True, send_mail=False)
	print('\n'.join(daily))
	get_img(daily)
	pass
