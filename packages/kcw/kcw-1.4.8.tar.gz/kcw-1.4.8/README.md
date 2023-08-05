#### 安装框架
pip install kcw

#### 创建应用
python
from kcw.create import create
create = create()
create.appname='apptest' #应用名

create.name="web" #模块名
create.webapp() #创建web应用  (创建网站)

create.name="cli" #模块名
create.cliapp() #创建cli应用  (创建cli程序)

### linux启动web
gunicorn守护启动：进去目录cd app/linuxweb/start    执行：gunicorn -w 2 -b 0.0.0.0:39010 -D --access-logfile ./logs/log server:kcwapp
