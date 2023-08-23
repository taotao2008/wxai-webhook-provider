import requests
import json
str = r'设计头像，色彩缤纷，浪漫的软焦点和空灵的光线'
#type = "photorealistic"
model = "midjourney"
mj_model = "V5"
url = "https://app.aizen.chat/autumn/attachments/t2CGvlepUnU87Hoym161lcFogOfvkQtwUV8aRrqjTS/image.png"

payload = { "prompt": str,
            #"type": type,
            "model": model,
            "mj_model": mj_model,
            "url": url
        }

#url = "http://localhost:6001/api/get_mj_images_async"
url = "http://bot.aizen.chat:6001/api/get_mj_images_async"

response = requests.post(url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
print(response.json())