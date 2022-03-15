#!/usr/bin/env python3
# encoding: utf-8
# Author: Daniel Müller

from cortexutils.responder import Responder
import requests
import json

class cloudflare(Responder):
    def __init__(self):
        Responder.__init__(self)
        self.account_identifier = self.get_param("config.account_identifier", "localhost")
        self.api_key = self.get_param("config.api_key", "api_key", None)
        self.mail = self.get_param("config.mail", "mail", None)
        self.service = self.get_param("config.service", None)

    def run(self):
        Responder.run(self)
        data = self.get_param("data.data")
        url = "https://api.cloudflare.com/client/v4/accounts/"+self.account_identifier+"/rules/lists/f881069d33aa4626bf44f8fd13ae09e2/items"
        datatype = self.get_param("data.dataType")
        caseTitle = self.get_param("data.case.title")
        caseId = str(self.get_param("data.case.caseId"))
        comment = "Thehive Case: \""+caseTitle+"\" ID: "+caseId
        headers = {"X-Auth-Email": self.mail, "X-Auth-Key": self.api_key, "Content-Type": "application/json"}
        if datatype == "ip" and self.service == "lock":
            getlistitems = requests.get(url, headers=headers).json()
            for i in getlistitems['result']:
                if i['ip'] == data:
                    id = i['id']
                    exists = True
                    break
                else:
                    exists = False
            if exists == False:
                payload = [{"ip": data,"comment": comment}]
                response = requests.post(url, json=payload, headers=headers).json()
                self.report(response)
            else:
                self.error("Error to "+self.service+" Address/Network: "+data+". Already Is Locked")

        elif datatype == "ip" and self.service == "unlock":
            getlistitems = requests.get(url, headers=headers).json()
            for i in getlistitems['result']:
                if i['ip'] == data:
                    id = i['id']
                    exists = True
                    break
                else:
                    exists = False
            if exists == True:
                payload = {"items":[{"id": id}]}
                deletelistitem = requests.delete(url, headers=headers, json=payload).json()
                self.report(deletelistitem)
            else:
                dataFormat = "Null"
                self.error("Error to "+self.service+" Address/Network: "+data+". Is not Locked")
if __name__ == '__main__':
    cloudflare().run()
