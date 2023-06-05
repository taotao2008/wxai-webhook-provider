import requests
import json
str = r'早晨，一位美女坐在河边钓鱼，周围环境是绿水青山'
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

url = "http://localhost:5001/api/get_mj_prompt"

response = requests.post(url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
ret = ""
if response.status_code == 200 :
    ret_json = json.loads(response.text)
    prompt_all = ret_json.get('prompt')
    prompt_1_start = prompt_all.index("imagine prompt:") + 15
    print(prompt_1_start)
    prompt_1_tmp = prompt_all[prompt_1_start:]
    prompt_1_end = prompt_1_tmp.index("imagine prompt:") - 12
    print(prompt_1_end)
    prompt_1 = prompt_1_tmp[:prompt_1_end]
    print(prompt_1)
    ret = json.loads({"prompt": prompt_1})

else:
    ret = json.loads({"prompt": "ERROR"})

print(ret)