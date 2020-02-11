#!/usr/bin/python3
# -*- coding:UTF-8 -*-
import textwrap

from PIL import Image, ImageFont, ImageDraw


class ImageOpt(object):
	def __init__(self, Canvas: Image.Image):
		self.Canvas = Canvas
		self.draw = ImageDraw.Draw(self.Canvas)
		self.CanvasWidth, self.CanvasHeight = self.Canvas.size
		pass

	# 改变图片尺寸
	@staticmethod
	def resizeImage(image: Image.Image, width: int = 100, height: int = 100):
		image = image.resize((width, height), Image.ANTIALIAS)
		return image

	# 保存图片
	def saveImage(self, image_path: str = './Export/testFile.png'):
		self.Canvas.save(image_path)

	# 绘制文本
	def drawText(self, text, x: int = 0, y: int = 0, font: ImageFont.FreeTypeFont = ImageFont.truetype("./Resource/Fonts/simkai.ttf", 18), fill="#000000", maxWidth: int = 30, iswarp:bool = True):
		if iswarp:
			lines = textwrap.wrap(text, width=maxWidth)
		else:
			lines = [textwrap.shorten(text, width=maxWidth, placeholder="...")]
		for line in lines:
			fontWidth, fontHeight = self.draw.textsize(line, font=font)
			self.draw.text((x, y), line, font=font, fill=fill)
			y += fontHeight + 5
		return x, y

	# 绘制图片
	def drawImage(self, image: Image.Image, x: int = 0, y: int = 0, show_mask: bool = False):
		if show_mask:
			mask = Image.new('RGBA', image.size, (255, 255, 255))
			image_width, image_height = image.size
			mask.paste(image, (0, 0, image_width, image_height), image)
			self.Canvas.paste(mask, (x, y, image.size[0] + x, image.size[1] + y))
		else:
			self.Canvas.paste(image, (x, y, image.size[0] + x, image.size[1] + y))
		return x, image.size[1] + y

	# 绘制图片文本(横向)
	def drawImageText(self, text, image: Image.Image, x: int = 0, y: int = 0,
	                  font: ImageFont.FreeTypeFont = ImageFont.truetype("./Resource/Fonts/simkai.ttf", 18),
	                  fill="#000000", maxWidth: int = 30):
		image_width, image_height = image.size
		self.Canvas.paste(image, (x, y, image_width + x, image_height + y))
		cur_x = image.size[0] + x + 15
		cur_y = image.size[1] + y + 5
		lines = textwrap.wrap(text, width=maxWidth)
		for line in lines:
			fontWidth, fontHeight = self.draw.textsize(line, font=font)
			self.draw.text((cur_x, y), line, font=font, fill=fill)
			y += fontHeight + 5
		if y > cur_y:
			cur_y = y
		return x, cur_y
