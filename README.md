# chery-api 奇瑞 智云互联 API

# 此项目有个卵子用?

> 没啥卵用, 我是将这个功能和家里的HASS连到一起了,用于统计车的行驶数据及油费计算.

![Screenshot](https://github.com/HexPang/chery-api/blob/master/Screenshot.png?raw=true)

# 其他说明

车控方面暂时先不做

# 使用方法

```python
from chery import chery_api

# 此处需要一个设备ID,具体用途未做测试
c_api = chery_api("DEVICE_ID")

# 登陆并获取新的TOKEN,旧TOKEN可能也需要通过抓包工具进行获取
c_api.login("USER_NAME", "PASS_WORD", "TOKEN")

# 刷新 globalId ,不然会提示已从其他地方登陆.(UNION_ID 可能配合抓包工具进行抓取)
c_api.refresh_global_id("UNION_ID") 

# 获取车辆列表
c_api.vehicle_list() 

# 获取车辆详细数据
c_api.vehicle_info("VIN") 
```
