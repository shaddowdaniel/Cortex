#!/usr/bin/env python3
# encoding: utf-8
# Author: Daniel Müller
from cortexutils.responder import Responder
import requests
import json
import base64
import os
import ipaddress

class McafeeNSP(Responder):
    def __init__(self):
        Responder.__init__(self)
        self.host = self.get_param("config.host", "localhost")
        self.user = self.get_param("config.user", "user", None)
        self.pwd = self.get_param("config.pass", "pwd", None)
        self.service = self.get_param("config.service", None)
        self.data = self.get_param("data.data")
    def run(self):
        Responder.run(self)
        token = self.user+":"+self.pwd
        token = token.encode('ascii')
        self.basic =  base64.b64encode(token)
        url = "https://"+self.host+"/sdkapi/"
        payload={}
        headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.nsm.v1.0+json',
        'NSM-SDK-API': self.basic
        }
        action = url+"session"
        login = requests.get(action, headers=headers, data=payload, verify=False).json()
        
        
        login_str = json.dumps(login)
        token = json.loads(login_str)['session']+":"+json.loads(login_str)['userId']
        token = token.encode('ascii')
        self.basic =  base64.b64encode(token)
        headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.nsm.v1.0+json',
        'NSM-SDK-API': self.basic
        }
        data = str(ipaddress.IPv4Address(self.data))
        if self.service == "lock":
            action = url+"sensor/1006/action/quarantinehost"
            #listQuarantine = requests.get(action, headers=headers, data=payload, verify=False).json()
            #resp = json.dumps(listQuarantine)
            payload = {
                    "IPAddress": data,
                    "Duration": "UNTIL_EXPLICITLY_RELEASED"
                    }
            quarantine = requests.post(action, headers=headers, json=payload, verify=False)
            if quarantine.status_code == 200:
                self.report(quarantine.json())
            else:
                self.error(quarantine.text)

        if self.service == "unlock":
            action = url+"sensor/1006/action/quarantinehost/"+data
            quarantine = requests.delete(action, headers=headers, verify=False)
            if quarantine.status_code == 200:
                self.report(quarantine.json())
            else:
                self.error(quarantine.text)

if __name__ == '__main__':
    McafeeNSP().run()
