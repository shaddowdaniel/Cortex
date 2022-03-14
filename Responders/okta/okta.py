#!/usr/bin/env python3
# encoding: utf-8
# Author: Daniel Müller

from cortexutils.responder import Responder
import requests
import json
import base64
import ipaddress 

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
        datatype = self.get_param("data.dataType")

    def run(self):
        Responder.run(self)
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'SSWS '+self.api_key
            }
        
        datatype = self.get_param("data.dataType")

        if datatype == "mail":
            data = self.get_param("data.data")
            data = str(data)
            url = "https://docktech.okta.com/api/v1/users?q="+data+"&limit=1"
            payload={}
            find_userid = requests.get(url, headers=headers, json=payload).json()
            #find_userid = json.loads(find_userid)
            #if find_userid["status_code"] == 200:
            userid = str(find_userid[0]['id'])
            status = str(find_userid[0]['status'])
            #datatype = self.get_param("data.dataType")
            if self.service == "lock" and status == "ACTIVE" and datatype == "mail":
                url = "https://docktech.okta.com/api/v1/users/"+userid+"/lifecycle/suspend"
                lock = requests.post(url, headers=headers, json=payload)
                self.report({'status_code': str(lock.status_code),
                    'message': 'User '+data+' success '+self.service+' Datatype '+datatype})

            elif self.service == "unlock" and status == "SUSPENDED" and datatype == "mail":
                url = "https://docktech.okta.com/api/v1/users/"+userid+"/lifecycle/unsuspend"
                unlock = requests.post(url, headers=headers, json=payload)
                self.report({'status_code': str(unlock.status_code),
                    'message': 'User '+data+' success '+self.service+' Datatype '+datatype})
            else:
                self.error(self.service+" Error User:"+data+' Status '+status+' Datatype '+datatype)

        elif self.service == "lock" and  datatype == "ip":
            data = self.get_param("data.data")
            url = "https://docktech.okta.com/api/v1/zones/nzo15k4zjyg4hrQMx357"
            payload = {}
            response = requests.request("GET", url, headers=headers, data=payload).json()
            payload = {
                    "type": "IP",
                    "id": "nzo15k4zjyg4hrQMx357",
                    "name": "BlockedIpZone",
                    "status": "ACTIVE",
                    "usage": "BLOCKLIST",
                    "gateways": response["gateways"]
                    }
            data = str(ipaddress.IPv4Network(data))
            for i in payload['gateways']:
                if i['value'] == data:
                    exists = True
                    self.error("Address/Network: "+data+" Already "+self.service)
                    break
                else:
                    exists = False

            if "/" in data and exists == False:
                new_data = {"type": "CIDR", "value": data}
                dataFormat = "IPv4 Network"
                payload['gateways'].append(new_data)
                lock = requests.request("PUT", url, headers=headers, json=payload)
                self.report({'status_code': str(lock.status_code),
                    'message': dataFormat+' '+data+' Success '+self.service+'. Datatype: '+datatype})
            elif "/" not in data and exists == False:
                data = data+"/32"
                new_data = {"type": "CIDR", "value": data}
                dataFormat = "IPv4 Address"
                payload['gateways'].append(new_data)
                lock = requests.request("PUT", url, headers=headers, json=payload)
                self.report({'status_code': str(lock.status_code),
                    'message': dataFormat+' '+data+' Success '+self.service+'. Datatype: '+datatype})
            else:
                dataFormat = "Null"
                self.error(self.service+" Error "+dataFormat+" :"+data+' Status '+status+' Datatype '+datatype)

        elif self.service == "unlock" and  datatype == "ip":
            data = self.get_param("data.data")
            url = "https://docktech.okta.com/api/v1/zones/nzo15k4zjyg4hrQMx357"
            payload = {}
            response = requests.request("GET", url, headers=headers, data=payload).json()
            payload = {
                    "type": "IP",
                    "id": "nzo15k4zjyg4hrQMx357",
                    "name": "BlockedIpZone",
                    "status": "ACTIVE",
                    "usage": "BLOCKLIST",
                    "gateways": response["gateways"]
                    }
            data =  str(ipaddress.IPv4Network(data))
            for i in payload['gateways']:
                if i['value'] == data:
                    exists = True
                    break
                else:
                    exists = False


            if exists == True:
                new_data = {"type": "CIDR", "value": data}
                dataFormat = "IPv4 Network"
                payload['gateways'].remove(new_data)
                lock = requests.request("PUT", url, headers=headers, json=payload)
                self.report({'status_code': str(lock.status_code),
                    'message': dataFormat+' '+data+' Success '+self.service+'. Datatype: '+datatype})
            else:
                dataFormat = "Null"
                self.error("Error to "+self.service+" Address/Network: "+data+". Is not Locked")
if __name__ == '__main__':
    okta().run()
