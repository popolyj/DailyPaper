#!/usr/bin/python3
# -*- coding:UTF-8 -*-

from PILUtility import Image, ImageFont, ImageOpt
from Utils import DefaultWidth, DefaultHeight, city_name, get, DayOfWeek, LoadImage, Today, sendMail, SetClipBoard

data_list = get()
weather_ls, bulletin_ls, journalism_ls, it_news_ls, sentence_ls = data_list.values()
date, week = DayOfWeek()


# 图片日报
def ImageDailyPaper():
	canvas = Image.new("RGBA", (DefaultWidth, DefaultHeight), (255, 255, 255))
	image_opt = ImageOpt(Canvas=canvas)
	cur_x, cur_y = 10, 10
	# 早报
	cur_x, cur_y = image_opt.drawText(text=f"{date} [ {week} ] 日报", x=cur_x, y=cur_y + 5, font=ImageFont.truetype("./Resource/Fonts/simkai.ttf", 24))
	# 天气预报
	if weather_ls:
		image_opt.drawImage(image=image_opt.resizeImage(image=LoadImage(image_url=f"http://res.tianapi.com/weather/{weather_ls[0]['weatherimg']}")), x=460, y=60, show_mask=True)
		image_opt.drawText(text=f"{city_name} {weather_ls[0]['weather']}", x=460, y=165, fill="#666666", maxWidth=10)
		cur_x, cur_y = image_opt.drawImage(image=Image.open(f'./Resource/Skins/Default/bg-0-weather.png'), x=cur_x, y=cur_y)
		cur_x, cur_y = image_opt.drawText(text=f"当前温度：{weather_ls[0]['real']}, 最低温度：{weather_ls[0]['lowest']}, 最高温度：{weather_ls[0]['highest']}", x=cur_x, y=cur_y + 5)
		cur_x, cur_y = image_opt.drawText(text=f"风向：{weather_ls[0]['wind']}, 风速：{weather_ls[0]['windspeed']}, 湿度：{weather_ls[0]['humidity']}", x=cur_x, y=cur_y + 5)
		cur_x, cur_y = image_opt.drawText(text=f"空气质量指数：{weather_ls[0]['air']}, 空气质量等级：{weather_ls[0]['air_level']}", x=cur_x, y=cur_y + 5)
		cur_x, cur_y = image_opt.drawText(text=f"天气状况提示：", x=cur_x, y=cur_y + 5)
		cur_x, cur_y = image_opt.drawText(text=f"{weather_ls[0]['tips']}", x=cur_x, y=cur_y + 5, fill='#FF0000', maxWidth=32)
	# 简报
	if bulletin_ls:
		cur_x, cur_y = image_opt.drawImage(image=Image.open(f'./Resource/Skins/Default/bg-0-bulletin.png'), x=cur_x, y=cur_y + 10)
		for idx, bulletin in enumerate(bulletin_ls, start=1):
			cur_x, cur_y = image_opt.drawText(text=f"{idx}、{bulletin['title']}", x=cur_x, y=cur_y + 5, fill='#006666', maxWidth=33, iswarp=False)
			if bulletin['imgsrc']:
				cur_x, cur_y = image_opt.drawImageText(text=f"    {bulletin['digest']}({bulletin['source']})",
				                                       image=image_opt.resizeImage(image=LoadImage(image_url=f"{bulletin['imgsrc']}"), width=150),
				                                       x=cur_x, y=cur_y + 5, maxWidth=23)
			else:
				cur_x, cur_y = image_opt.drawText(text=f"    {bulletin['digest']}({bulletin['source']})", x=cur_x, y=cur_y + 5, maxWidth=33)
	# 综合新闻
	if journalism_ls:
		cur_x, cur_y = image_opt.drawImage(image=Image.open(f'./Resource/Skins/Default/bg-0-journalism.png'), x=cur_x, y=cur_y + 10)
		for idx, journalism in enumerate(journalism_ls, start=1):
			cur_x, cur_y = image_opt.drawText(text=f"{idx}、{journalism['description']}:{journalism['title']}", x=cur_x, y=cur_y + 5, maxWidth=33)
	# IT资讯
	if it_news_ls:
		cur_x, cur_y = image_opt.drawImage(image=Image.open(f'./Resource/Skins/Default/bg-0-itnews.png'), x=cur_x, y=cur_y + 10)
		for idx, it_news in enumerate(it_news_ls, start=1):
			cur_x, cur_y = image_opt.drawText(text=f"{idx}、{it_news['title']}", x=cur_x, y=cur_y + 5, maxWidth=33)
	# 心语
	if sentence_ls:
		cur_x, cur_y = image_opt.drawImage(image=Image.open(f'./Resource/Skins/Default/bg-0-sentence.png'), x=cur_x, y=cur_y + 10)
		for idx, sentence in enumerate(sentence_ls, start=1):
			cur_x, cur_y = image_opt.drawText(text=f"{sentence['content']} —— {sentence['mrname']}", x=cur_x, y=cur_y + 5, maxWidth=33)
	image_path = f"./Export/DailyPaper_{Today()}.png"
	image_opt.saveImage(image_path=image_path)
	return image_path


# 文字日报
def TextDailyPaper():
	daily_lines = list()
	daily_lines.append(f"{date} [ {week} ] 日报")
	if weather_ls:
		daily_lines.append(f">>>>> 天气预报 <<<<<")
		daily_lines.append(f"{city_name} {weather_ls[0]['weather']}")
		daily_lines.append(f"当前温度：{weather_ls[0]['real']}, 最低温度：{weather_ls[0]['lowest']}, 最高温度：{weather_ls[0]['highest']}")
		daily_lines.append(f"风向：{weather_ls[0]['wind']}, 风速：{weather_ls[0]['windspeed']}, 湿度：{weather_ls[0]['humidity']}")
		daily_lines.append(f"空气质量指数：{weather_ls[0]['air']}, 空气质量等级：{weather_ls[0]['air_level']}")
		daily_lines.append(f"天气状况提示：")
		daily_lines.append(f"{weather_ls[0]['tips']}")
	if bulletin_ls:
		daily_lines.append(f">>>>> 今日简报 <<<<<")
		for idx, bulletin in enumerate(bulletin_ls, start=1):
			daily_lines.append(f"{idx}、{bulletin['title']}")
	if journalism_ls:
		daily_lines.append(f">>>>> 今日新闻 <<<<<")
		for idx, journalism in enumerate(journalism_ls, start=1):
			daily_lines.append(f"{idx}、{journalism['title']}")
	if it_news_ls:
		daily_lines.append(f">>>>> 今日前沿 <<<<<")
		for idx, it_news in enumerate(it_news_ls, start=1):
			daily_lines.append(f"{idx}、{it_news['title']}")
	if sentence_ls:
		daily_lines.append(f">>>>> 今日心语 <<<<<")
		for idx, sentence in enumerate(sentence_ls, start=1):
			daily_lines.append(f"{sentence['content']} —— {sentence['mrname']}")
	daily = '\n'.join(daily_lines)
	return daily


# 邮件日报
def MailDailyPaper():
	sendMail(subject=f"{date} [{week}] 日报", contents=TextDailyPaper(), attachments=ImageDailyPaper())


# 剪贴板日报
def ClipBoardDailyPaper():
	SetClipBoard(TextDailyPaper())


if __name__ == '__main__':
	ImageDailyPaper()

	pass
