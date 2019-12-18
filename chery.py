# -*- coding: utf-8 -*

import requests
import hashlib
import base64
import json
import uuid
from urllib import parse
import os.path

class chery_api():
    # 奇瑞 智云互联 API
    def __init__(self, device_id = None):
        self.base_url = "https://cloudriveapp.mychery.com:3082/"
        self.user = None
        self.device_id = device_id

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


    def encode_pwd(self, password):
        sha256_pwd = hashlib.sha256(password.encode('utf-8')).hexdigest()
        base64_pwd = base64.b64encode(sha256_pwd.encode('utf-8')).decode('utf-8')
        return base64_pwd


    def login(self, username, password, token):
        cache = self.read_cache("user")
        if cache is not None:
            self.user = cache
            return self.user
        data = {
            "data": {
                "appType": "1",
                "userAccount": username,
                "userPasswd":  self.encode_pwd(password),
                "token": token
            }
        }
        self.user = self.request(100, 101, data)
        self.write_cache("user", self.user)
        return self.user


    def refresh_global_id(self, union_id, app_type = "1"):
        res = self.request(100, 102, {"data": {"token": self.user["data"]["token"], "unionid": union_id, "appType": app_type}})
        self.user = res
        return self.user


    def vehicle_list(self):
        return self.request(100, 900)


    def vehicle_config(self, vin):
        return self.request(100, 969, {"data": {vin: vin}})


    def vehicle_info(self, vin):
        data = {
            "data": {
                "vin": vin
            }
        }
        res = self.request(100, 910, data)
        return res


    def load_user(self):
        return self.request(100, 112)


    def upload_device(self):
        return self.request(100, 1004, {"data": {"deviceId": self.device_id }})

    
    def menu(self, vin):
        return self.request(100, 969, {"data": {"vin": vin, "isBluetoothAuth": 0}})


    def vehicle_pass(self, vin, password):
        return self.request(100, 125, {"data": {"vin": vin, "openGesturePass": "0", "vehiclePass": self.encode_pwd(password)}})


    def vehicle_command(self, vin, password, data, passwordType = "0", instruction = "1105"):
        conf_data = {"vin": vin, "safePasswd": self.encode_pwd(password), "passwordType": "0", "instruction": instruction}
        merge_data = {**data, **conf_data}
        return self.request(100, 970, {"data": merge_data})
