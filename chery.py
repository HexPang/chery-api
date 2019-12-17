# -*- coding: utf-8 -*

import requests
import hashlib
import base64
import json
import uuid
from urllib import parse
import os.path

class chery():
    # 奇瑞 智云互联 API
    def __init__(self):
        self.base_url = "https://cloudriveapp.mychery.com:3082/"
        self.user = None

    def gen_uuid(self):
        uuid_str = str(uuid.uuid4())
        return uuid_str


    def read_cache(self, cache_name):
        cache = None
        if not os.path.isfile(cache_name + '.cache'):
            return None
        with open(cache_name + '.cache', 'r') as f:
            cache = json.loads(f.read())
        return cache


    def write_cache(self, cache_name, data):
        with open(cache_name + '.cache', 'w+') as f:
            f.write(json.dumps(data))
            f.flush()
        return True


    def request_command(self, data):
        headers = {
            "User-Agent": parse.quote("智云互联/1.0.0 CFNetwork/1121.2.2 Darwin/19.2.0"),
            "Content-Type": "application/json; charset=utf-8"
        }
        r = requests.post(
            url=self.base_url + "cheryT15/app/command.do", data=json.dumps(data), headers=headers)
        r.encoding = 'utf-8'
        res = json.loads(r.text)
        if res["resultCode"] != "0200":
            raise Exception(res["resultMsg"])
        return res

    
    def request(self, business_id, service_type, params = None):
        request_data = {
            "businessId": str(business_id),
            "serviceType": str(service_type),
            "version": "0100"
        }
        if self.user != None:
            request_data["globalId"] = self.user["globalId"]
        request_data["requestId"] = self.gen_uuid()
        if params is not None:
            request_data = {**request_data, **params}
        return self.request_command(request_data)


    def login(self, username, password, token):
        cache = self.read_cache("user")
        if cache is not None:
            self.user = cache
            return self.user
        sha256_pwd = hashlib.sha256(password.encode('utf-8')).hexdigest()
        base64_pwd = base64.b64encode(sha256_pwd.encode('utf-8')).decode('utf-8')
        data = {
            "data": {
                "appType": "1",
                "userAccount": username,
                "userPasswd":  base64_pwd,
                "token": token
            }
        }
        self.user = self.request(100, 101, data)
        self.write_cache("user", self.user)
        return self.user


    def load_vehicle_list(self):
        return self.request(100, 900)


    def load_vehicle_config(self, vin):
        return self.request(100, 969, {"data": {vin: vin}})


    def load_vehicle(self):
        data = {
            "data": {
                "vin": self.user["data"]["defaultVin"]
            }
        }
        res = self.request(100, 910, data)
        return res


    def load_user(self):
        return self.request(100, 112)
