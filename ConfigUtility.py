#!/usr/bin/python3
# -*- coding:UTF-8 -*-
from configparser import ConfigParser
from Config import logger


class Config(object):
	def __init__(self, config_path):
		# 配置文件参数
		self.config_path = config_path
		self.config_section = None
		self.config_option = None
		self.config_value = None
		# 加载配置文件
		try:
			self.config = ConfigParser()
			self.config.read(config_path, encoding='utf-8')
		except FileNotFoundError as f:
			logger.error(f)
		except Exception as e:
			logger.error(e)

	def read(self, config_section, config_option):
		try:
			self.config_section = config_section
			self.config_option = config_option
			self.config_value = self.config.get(section=self.config_section, option=self.config_option)
			return self.config_value
		except Exception as e:
			logger.error(e)

	def save(self, config_section, config_option, config_value):
		try:
			self.config_section = config_section
			self.config_option = config_option
			self.config_value = config_value
			self.config.set(section=self.config_section, option=self.config_option, value=self.config_value)
			with open(self.config_path, 'w') as config_file:
				self.config.write(config_file)
		except FileNotFoundError as f:
			logger.error(f)
		except Exception as e:
			logger.error(e)

