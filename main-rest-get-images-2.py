import requests
import json
str = r'一个帅气的男孩，MD服装，新潮的服装，蓬松的头发，精致的五光十色，耐克鞋，耳机，银色项链，充气背包，Orange系列，干净的背景，正面视图，电影灯光，明暗对比'
#type = "photorealistic"
model = "midjourney"
mj_model = "V5"
url = ""

payload = { "prompt": str,
            #"type": type,
            "model": model,
            "mj_model": mj_model,
            "url": url
        }

url = "http://localhost:6001/api/get_mj_images_async"

response = requests.post(url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
print(response)