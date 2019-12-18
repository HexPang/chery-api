# chery-api 奇瑞 智云互联 API

# 使用方法

```python
from chery import chery_api

c_api = chery_api("DEVICE_ID")

c_api.login("USER_NAME", "PASS_WORD",
                        "TOKEN")

c_api.refresh_global_id("UNION_ID") # UNION_ID 可能配合抓包工具进行抓取

c_api.vehicle_list() # 获取车辆列表

c_api.vehicle_info("VIN") # 获取车辆详细数据
```
