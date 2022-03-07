#!/usr/bin/env python3
# encoding: utf-8
# Author: Daniel Müller

from cortexutils.responder import Responder
import requests
import json
import base64


class okta(Responder):
    def __init__(self):
        self.file = "okta.json"
        Responder.__init__(self)
        self.host = self.get_param("config.url", "localhost")
        self.user = self.get_param("config.user", "user", None)
        self.pwd = self.get_param("config.pass", "pwd", None)
        self.api_key = self.get_param("config.api_key", "api_key", None)

    def run(self):
        Responder.run(self)
        url = "https://"+self.host+"/api/v1/users?q="+username+"&limit=1"
        payload={}
        
        headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'SSWS '+self.api_key
        }
        
        find_userid = requests.request("GET", url, headers=headers, data=payload)
        
        if find_userid.status_code == 200:
            self.report(find_userid.text)
        else:
            self.error(find_userid.status_code)

if __name__ == '__main__':
    okta().run()
