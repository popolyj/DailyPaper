#!/usr/bin/python3
# -*- coding:UTF-8 -*-
import datetime
import logging
import os
from logging.handlers import TimedRotatingFileHandler

log_path = './Logs'


def get_log(logger_name: str):
	# 创建一个logger
	logger = logging.getLogger(logger_name)
	logger.setLevel(logging.DEBUG)
	# 设置所有日志和错误日志的存放路径
	if not os.path.exists(log_path):
		os.mkdir(log_path)
	error_log_path = os.path.join(log_path, 'Error')
	if not os.path.exists(error_log_path):
		os.mkdir(error_log_path)
	# 设置日志文件名
	all_log_name = f'{log_path}/{logger_name}.log'
	error_log_name = f'{error_log_path}/{logger_name}.log'
	# 创建handler
	# 创建一个handler写入所有日志
	all_handle = TimedRotatingFileHandler(filename=all_log_name, when='d', interval=1, backupCount=10, encoding='utf-8', delay=True, atTime=datetime.time(0, 0, 0, 0))
	all_handle.setLevel(logging.INFO)
	# 创建一个handler写入错误日志
	error_handle = TimedRotatingFileHandler(filename=error_log_name, when='d', interval=1, backupCount=0, encoding='utf-8', delay=True, atTime=datetime.time(0, 0, 0, 0))
	error_handle.setLevel(logging.ERROR)
	# 创建一个handler输出到控制台
	console_handle = logging.StreamHandler()
	console_handle.setLevel(logging.INFO)
	# 定义日志输出格式
	# 以时间-日志器名称-日志级别-日志内容的形式展示
	all_log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	# 以时间-日志器名称-日志级别-文件名-函数行号-错误内容
	error_log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s  - %(lineno)s - %(message)s')
	# 以时间-日志器名称-日志级别-文件名-函数行号-错误内容
	console_log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s  - %(lineno)s - %(message)s')
	# 将定义好的输出形式添加到handler
	all_handle.setFormatter(all_log_formatter)
	error_handle.setFormatter(error_log_formatter)
	console_handle.setFormatter(console_log_formatter)
	# 给logger添加handler
	logger.addHandler(all_handle)
	logger.addHandler(error_handle)
	logger.addHandler(console_handle)
	return logger
