#!/usr/bin/env python
# -*- coding=utf-8 -*-
# dnspod 动态更新IP的客户端

import json,sys,urllib2,urllib,os,time

def POST(url,data):
    formdata=urllib.urlencode(data)
    req = urllib2.Request(url,headers={'User-Agent' : "Magic Browser"}) 
    f = urllib2.urlopen(req,formdata,timeout=10)
    content = f.read()
    return content

def GetIP():
		return urllib2.urlopen("http://lab.hitoy.org/api/gettheip").read()


class dnspod:
		def __init__(self,username,password,token):
				self.username=username
				self.password=password
				self.token=token

		def get_domain_list(self):
				dlist = POST("https://dnsapi.cn/Domain.List",{"login_email":self.username,"login_password":self.password,"format":"json"})
				ddict = json.loads(dlist)
				self.domains=ddict['domains']

		def get_record_list(self,domain):
				domain_id=0
				for d in self.domains:
						if d['punycode']  == domain:
								domain_id=d['id']
				if domain_id == 0:return
				rlist = POST("https://dnsapi.cn/Record.List",{"login_email":self.username,"login_password":self.password,"format":"json","domain_id":domain_id})
				return json.loads(rlist)

		def update_record(self,sub_domain,value,retype="A",reline="默认",ttl=600,mx=10):
				self.get_domain_list()
				record = self.get_record_list("hitoy.org")
				domain_id=record['domain']['id']
				for i in record['records']:
						if i['name'] == sub_domain:
								record_id = i['id']

				do = POST("https://dnsapi.cn/Record.Modify",{"login_email":self.username,"login_password":self.password,"format":"json","domain_id":domain_id,"record_id":record_id,"sub_domain":sub_domain,"value":value,"record_type":retype,"record_line":reline,"ttl":ttl})
				resulte = json.loads(do)
				return resulte['status']['message']


ip = "1.1.1.1"
uname = "example@hitoy.org"
password = "example"
sub_domain = "www"

dns = dnspod(uname,password,"")
while True:
		try:
				newip = GetIP()
				if newip != ip:
						ip = newip
						re  = dns.update_record(sub_domain,ip)
						sys.stdout.write("%s\r"%re)
		except Exception,e:
				sys.stdout.write("%s\n"%e)
		time.sleep(20)
