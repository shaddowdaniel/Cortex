#!/usr/bin/env python3
# encoding: utf-8
# Author: Daniel Müller
from cortexutils.responder import Responder
import requests
import json
import base64
import os


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
        if self.service == "lock":
            ruleObject = "173"
            action = url+"ruleobject/"+ruleObject
            listRuleObject = requests.get(action, headers=headers, data=payload, verify=False).json()
            resp = json.dumps(listRuleObject)

            payload = {
            'RuleObjDef': {
            'visibleToChild': True, 
            'description': listRuleObject['RuleObjDef']['description'], 
            'ruleobjId': ruleObject, 
            'name': listRuleObject['RuleObjDef']['name'], 
            'ruleobjType': 'NETWORK_IPV_4',
            'Network_IPV_4': listRuleObject['RuleObjDef']['Network_IPV_4']
            }
            }
            payload['RuleObjDef']['Network_IPV_4']['networkIPV4List'].append(self.data)
            payload = json.dumps(payload)
            insertRuleObject = requests.put(action, headers=headers, data=payload, verify=False).json()
            self.report(insertRuleObject) 

        elif self.service == "unlock":
            ruleObject = "173"
            action = url+"ruleobject/"+ruleObject
            listRuleObject = requests.get(action, headers=headers, data=payload, verify=False).json()
            payload = {
            'RuleObjDef': {
            'visibleToChild': True,
            'description': listRuleObject['RuleObjDef']['description'], 
            'ruleobjId': ruleObject, 
            'name': listRuleObject['RuleObjDef']['name'], 
            'ruleobjType': 'NETWORK_IPV_4',
            'Network_IPV_4': listRuleObject['RuleObjDef']['Network_IPV_4']
            }
            }
            payload['RuleObjDef']['Network_IPV_4']['networkIPV4List'].remove(self.data)
            payload = json.dumps(payload)

            removeRuleObject = requests.put(action, headers=headers, data=payload, verify=False).json()
            self.report(removeRuleObject)

if __name__ == '__main__':
    McafeeNSP().run()
