# DailyPaper
日报生成器  
必备环境：  
Python 3.7.3+  
使用前请使用命令安装package  
cd 程序所在目录  
pip install -r requirement.txt  
  
使用注意：  
使用前请务必修改相应的参数  
邮箱类：user、password、host、port、MailToList  
  
  
接口的key：  
请自行前往https://www.tianapi.com/apiview/26 注册，请替换26为后续数字  
申请后，注册接口ID为 26 72 117  
完成后，在个人中心会得到APIKEY ，将其填入Key的list中  
城市：默认为上海，请修改成你需要的城市  
修改运行参数后，运行  
  
  
使用方法：  
目前提供的方法如下：
ImageDailyPaper()： 生成图片格式的日报，默认返回图片路径  
TextDailyPaper()： 生成文本格式的日报，默认返回日报文本
MailDailyPaper()： 将文本以邮件内容，图片为附件的形式发布邮件  
ClipBoardDailyPaper()： 将文本日报复制到剪贴板  
  
  
效果截图：  
图片日报：  
  
文本日报：  
  
邮件日报：  
  