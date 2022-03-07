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
        self.service = self.get_param("config.service", None)
        data = self.get_param("data.data")

    def run(self):
        Responder.run(self)
        data = self.get_param("data.data")
        data = str(data)
        url = "https://docktech.okta.com/api/v1/users?q="+data+"&limit=1"
        payload={}

        headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'SSWS '+self.api_key
        }

        find_userid = requests.get(url, headers=headers, json=payload).json()
        #find_userid = json.loads(find_userid)
        #if find_userid["status_code"] == 200:
        userid = str(find_userid[0]['id'])
        status = str(find_userid[0]['status'])

        if self.service == "lock" and status == "ACTIVE":
             url = "https://docktech.okta.com/api/v1/users/"+userid+"/lifecycle/suspend"
             lock = requests.post(url, headers=headers, json=payload)

             self.report({'status_code': str(lock.status_code),
                 'message': 'User '+data+' success '+self.service})

        elif self.service == "unlock" and status == "SUSPENDED":
             url = "https://docktech.okta.com/api/v1/users/"+userid+"/lifecycle/unsuspend"
             unlock = requests.post(url, headers=headers, json=payload)
             self.report({'status_code': str(unlock.status_code),
                 'message': 'User '+data+' success '+self.service})
        else:
            self.error(self.service+" Error User:"+data+' Status '+status)

if __name__ == '__main__':
    okta().run()
