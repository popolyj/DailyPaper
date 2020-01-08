# DailyPaper
日报生成器  
必备环境：  
Python 3.7.3+  
使用前请使用命令安装package  
cd 程序所在目录  
pip install -r requirement.txt  
  
使用注意：  
使用前请务必修改相应的参数  
邮箱类：user、password、host、port、mail_ls  
  
  
接口的key：  
请自行前往https://www.tianapi.com/apiview/26 注册，请替换26为后续数字  
申请后，注册接口ID为 26 72 117  
完成后，在个人中心会得到APIKEY ，将其填入Key的list中  
城市：默认为上海，请修改成你需要的城市  
修改运行参数后，运行  
  
  
效果截图：  
仅复制到剪贴板：  
get_daily(show_digest=False, show_url=False, show_image=False, send_to_clidBoard=True, send_mail=False)  
get_daily(show_digest=True, show_url=False, show_image=False, send_to_clidBoard=True, send_mail=False)  
get_daily(show_digest=True, show_url=True, show_image=True, send_to_clidBoard=True, send_mail=False)  
  
发送邮件（需要提前配置邮件参数）：  
get_daily(show_digest=True, show_url=True, show_image=True, send_to_clidBoard=True, send_mail=True)  
  
