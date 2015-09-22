# PyPageMonitor
## 介绍
  * 一个可以定时监控网页任何数据的monitor
  * 当你所监控的Dom发生变化就会发邮件给你指定的邮箱地址。

## 使用
  首先，你要在```watchweb.ini```加入你要监控网页的配置数据。需要配置以下几个数据：
* ```url```   监控网页的url地址
* ```query```   Dom选择器
* ```mail_receiver```   收件人邮箱地址
* ```interval_seconds```  监控间隔时间（单位：秒）

## 环境
* python版本 2.7.9
 
## 依赖库
* openSSL
 * [openssl安装说明](http://elliott-shi.iteye.com/blog/1955408) 
* APScheduler
* gevent
 * 安装APScheduler和gevent
 ```
 easy_install APScheduler
 easy_install gevent
 ```

#部署运行
可以把它部署在亚马逊aws上运行，运行命令：```python monitor.py```

* 学习自用
* 最后感谢PyWebMonitor
