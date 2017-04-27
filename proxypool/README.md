# proxypool

基于 django 制作的 IP 池，本项目使用 requests+bs4 爬取数据，依托 django 数据库系统保存，通过网络请求从数据库内获取 IP，运行中有疑问可以在 Issues 下
提交。

##运行环境

python 3+

##运行依赖包

- requests
- bs4
- lxml
- selenium
- PhantomJS

##下载使用

###下载配置
pass

###运行
####1、windows 下计划任务
将 sche_spider.py 加入计划任务


####2、linux - django-cron

pass
####2、手动运行
进入 http://127.0.0.1:8000/proxy/work/
手动点击 crwal 按钮运行


##项目说明

###爬取 IP

####爬取流程

请求网站 --> 获得代理 --> 初次验证代理  --> 存入数据库

####文件说明

爬虫文件在 spider 文件夹下
爬虫控制文件为 fetch.py

####目前支持的网站

- IP181
- 快代理
- 66 代理
- 西刺代理

####扩展网站

- 爬虫脚本编写参考爬虫文件
- 脚本编写好之后，在 fetch.py 中导入该文件主函数，加入线程池即可

###验证 IP

####文件说明

验证 IP 文件为 VerifyProxy.py

####验证流程

请求 baidu --> 返回 200 --> 验证成功


###整理 IP

####文件说明

整理数据库内 IP 的文件为 SortDt.py

####整理流程

清除重复的 IP
清除连续验证失败次数超过 5 次的 IP

###API 提取 IP 接口

#### API 提取 url
app: yourproject/proxy/get
project: http://127.0.0.1:8000/proxy/get/

####参数

| name      | type | Description | Must | example | Remarks |
| :-------- | --------:| :------: | :------: | :------: | :------: |
| num    |   int |  IP数量  |   必须 |  10  |每次最多100  |
| v    |   bool |  是否验证  |   可选 |  true/false  |大小写不敏感,True也是可以的，其他值一律视为 false  |
| v_num    |   int |  验证通过次数  |   可选 |  5  |原则上通过次数，越多IP越稳定，次数越大IP数量越少 |
| type    |   str |  ip类型,G-'高匿',T-'透明',O-'其他'  |   可选 |  O  |  |
| head    |   str |  http 或者 https,默认为 http  |   可选 |  https  |  |
| loc    |   str |  地区  |   可选 |  上海  |尽量以省市一级的地名查询  |

示例: http://127.0.0.1:8000/proxy/get/?num=50&v_num=5&head=https&loc=上海
说明: 提取100个ip , 通过验证次数大于等于 5，https 类型，ip坐标上海

###查看数据库情况

####django自带的admin

pass


####可视化图表

结合 echarts 做了可视化图表
请求地址:http://127.0.0.1:8000/proxy/chart/
效果图:
pass
