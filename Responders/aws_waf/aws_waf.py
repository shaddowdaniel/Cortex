#!/usr/bin/env python3
# encoding: utf-8
# Author: Daniel Müller

from cortexutils.responder import Responder
import requests
import json
import boto3
import ipaddress

class AWSWafv2(Responder):
    def __init__(self):
        Responder.__init__(self)
        self.arn = self.get_param("config.arn", "ARN")
        self.client_id = self.get_param("config.client_id", "client_id", None)
        self.client_secret = self.get_param("config.client_secret", "client_secret", None)
        self.region = self.get_param("config.region", "region", None)
        self.service = self.get_param("config.service", None)
        self.data = self.get_param("data.data")
    def run(self):
        Responder.run(self)
        client = boto3.client("sts",aws_access_key_id=self.client_id,aws_secret_access_key=self.client_secret,region_name=self.region)
        acct_b = client.assume_role(RoleArn=self.arn, RoleSessionName='rol_splunk')
        ACCESS_KEY = acct_b['Credentials']['AccessKeyId']
        SECRET_KEY = acct_b['Credentials']['SecretAccessKey']
        SESSION_TOKEN = acct_b['Credentials']['SessionToken']
        client = boto3.client('wafv2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, aws_session_token=SESSION_TOKEN, region_name=self.region)
        new_data = self.get_param("data.data")
        #response = client.list_ip_sets(Scope="CLOUDFRONT")
        response = client.get_ip_set(Id="60ec8e7b-5b86-42e8-8e12-27cd98a5791e", Scope="CLOUDFRONT", Name="ipset-blocklist-ips")
        data = str(ipaddress.IPv4Network(new_data))
        datatype = self.get_param("data.dataType")
        if data not in response['IPSet']['Addresses'] and self.service == "lock" and datatype == "ip":
            response['IPSet']['Addresses'].append(data)
            blocked_ips = response['IPSet']['Addresses']
            response = client.update_ip_set(Id='60ec8e7b-5b86-42e8-8e12-27cd98a5791e', Scope="CLOUDFRONT", Name="ipset-blocklist-ips", Addresses=blocked_ips, LockToken=response['LockToken'])
            self.report(response)
        elif data in response['IPSet']['Addresses'] and self.service == "unlock" and datatype == "ip":
            response['IPSet']['Addresses'].remove(data)
            blocked_ips = response['IPSet']['Addresses']
            response = client.update_ip_set(Id='60ec8e7b-5b86-42e8-8e12-27cd98a5791e', Scope="CLOUDFRONT", Name="ipset-blocklist-ips", Addresses=blocked_ips, LockToken=response['LockToken'])
            self.report(response)
        else:
            self.error("Datatype: "+datatype+": "+new_data+" already "+self.service)

if __name__ == '__main__':
    AWSWafv2().run()
