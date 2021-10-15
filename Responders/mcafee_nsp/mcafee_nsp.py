#!/usr/bin/env python3
# encoding: utf-8
# Author: Daniel Müller
from cortexutils.responder import Responder
import requests
import json
import base64

class McafeeNSP(Responder):
    def __init__(self):
        Responder.__init__(self)
        self.user = self.get_param("config.user", "")
	self.pass = self.get_param("config.pass", "")
        self.host = self.get_param("config.url", "")

    def run(self):
	McafeeNSP.run(self)
	
	self.basic =  base64.b64decode(self.user+":"+self.pass)
	url = "https://"+self.host+"/sdkapi/session"
	payload={}
	
	headers = {
  	'Content-Type': 'application/json',
  	'Accept': 'application/vnd.nsm.v1.0+json',
  	'NSM-SDK-API': self.basic
	}
	
	login = requests.request("GET", url, headers=headers, data=payload)
	
	if login.status_code == 200:
            self.report(login.text)
        else:
            self.error(login.status_code)

if __name__ == '__main__':
    McafeeNSP().run()
