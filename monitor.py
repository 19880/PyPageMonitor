#coding: utf-8
import watchweb
import os
import smtplib
import re
from email.mime.text import MIMEText
from email.header import Header
import urllib
from apscheduler.schedulers.gevent import GeventScheduler
import logging
#shutdown ssl verify
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import requests
from pyquery import PyQuery as pq
import pickle
import hashlib

# 发送邮件
def send_mail(web,sub,content):
    '''
    to_list:发给谁
    sub:主题
    content:内容
    send_mail("aaa@126.com","sub","content")
    '''
    #要发给谁，这里发给2个人
    mailto_list=web[watchweb.MAIL_RECEIVER]
    #设置服务器，用户名、口令以及邮箱的后缀
    mail_config = watchweb.get_mail_config()
    mail_host=mail_config['mail_smtpserver']
    mail_user=mail_config['mail_user']
    mail_pass=mail_config['mail_password']
    mail_postfix=mail_config['mail_postfix']
    me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content,'html','utf-8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = mailto_list
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me, mailto_list, msg.as_string())
        s.close()
        print "Send success"
        return True
    except Exception, e:
    	print "Send failed"
        print str(e)
        return False

# 对比网页
def check_web(**web):
	user_agent = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding': 'gzip, deflate, sdch',
		'Accept-Language': 'zh-CN,zh;q=0.8',
		'Upgrade-Insecure-Requests': 1,
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
	}
	cookies = dict(__jsluid='f93f2af7849678574390310f47eedabf', __jsl_clearance='1441972658.715|0|YupPuYPVQKTT7URFn1zEZGnBeJg%3D')		#什么值得买cookie
	watch_url = web[watchweb.URL]
	data_file = '.cache/' + text_md5(watch_url) +'.data'
	r = requests.get(watch_url, headers=user_agent, cookies=cookies, timeout=4)
	doc=pq(r.text)
	title = doc('title')
	data=doc(web[watchweb.QUERY])
	for i in data:
		result = pq(i).text()
		fdata = read_data(data_file)

		# from pprint import pprint
		# pprint(result)
		# pprint(fdata)
		if fdata is None:
			record_data(data_file, result)
			fdata = result
		if fdata <> result:
			record_data(data_file, result)
			print 'send mail...'
			sub = u"(◑◑) %s" % title.text()
			content = '<html><p>%s</p><p>Change: <b>%s</b></p><a href="%s">%s</a></html>'% (title.text(),result,watch_url,watch_url)
			send_mail(web, sub, content)
		

# 字符md5
def text_md5(text):
	m = hashlib.md5()
	m.update(text)
	psw = m.hexdigest()
	return psw

# 读取文件数据
def read_data(file):
	try:
		with open(file, 'rb') as f:
			data = pickle.load(f)
	except IOError:
		return None

	return data

# 记录文件数据
def record_data(file, data):
	output = open(file, 'wb')
	pickle.dump(data, output)
	output.close()

# 监控
def watch():
	scheduler = GeventScheduler()
	
	for web in watchweb.get_watch_webs():
		s = int(web[watchweb.INTERVAL_SECONDS])
		scheduler.add_job(check_web, 'interval', seconds=s,kwargs=web)


	g = scheduler.start()  # g is the greenlet that runs the scheduler loop
	print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

	# Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
	try:
		g.join()
	except (KeyboardInterrupt, SystemExit):
		pass

		
if __name__ == '__main__':
	global MAIL_CONFIG
	# logging.basicConfig(filename = 'monitor.log',level=logging.ERROR)
	watch()