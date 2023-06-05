from flask import Flask, request, jsonify
from chatGPTMidJourneyPrompt.mjPrompt import PromptGenerator
import requests
import json
import os
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import re
# DOCS https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor
# 创建线程池执行器
executor = ThreadPoolExecutor(10)

# 创建 Flask 应用
app = Flask(__name__)



#URL_MJ_PROMPT = "http://127.0.0.1:6001/api/send_and_receive_async"

URL_MJ_PROMPT = os.environ['URL_MJ_PROMPT']
OPENAI_KEY = os.environ['OPENAI_KEY']

# supported authorization methods: via email and password, via token, via api key
config = {
  "email": "your_email",
  "password": "your_password",
  # or
  "session_token": "your_session_token",
  # or
  #"api_key": "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",
  "api_key": OPENAI_KEY,
}

promptGenerator = PromptGenerator(config)


# 创建一个 API 路由，接受 POST 请求，用户输入图片描述和风格，生成MJ适用的prompt
@app.route('/api/get_mj_prompt_async', methods=['POST'])
def get_mj_prompt_async():
    # 从请求中获取关键词参数
    data = request.get_json()
    prompt = data.get('prompt')
    # type = data.get('type')
    mj_model = data.get('mj_model')
    model = data.get('model')
    url = data.get('url')
    # 交由线程去执行耗时任务
    ret_mj = None
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_result = executor.submit(get_mj_prompt, prompt, mj_model, model, url)
        ret_mj = future_result.result()
        print(ret_mj)

    return jsonify(ret_mj)


def get_mj_prompt(prompt, mj_model, model, url):
    global params
    global promptGenerator

    promptConfig = {
        "model": model,
        #"type": type,
        # "renderer": "octane",
        # "content": "landscape",
        # "aspect_ratio": "9:16",
        # "color": "red",
        "url": url,
    }
    prompt_mj = None
    if mj_model == "V5":
        prompt_mj = promptGenerator.V5(prompt, config=promptConfig, words=80)
    elif mj_model == "V4":
        prompt_mj = promptGenerator.V4(prompt, config=promptConfig, words=80)
    elif mj_model == "niji":
        prompt_mj = promptGenerator.niji(prompt, config=promptConfig, words=80)

    # 将最新图片的URL作为响应返回
    return str(prompt_mj)

# 创建一个 API 路由，接受 POST 请求，用户输入图片描述和风格，输出midjourney图片，异步方式
@app.route('/api/get_mj_images_async', methods=['POST'])
def get_mj_images_async():
    # 从请求中获取关键词参数
    data = request.get_json()
    prompt = data.get('prompt')
    mj_model = data.get('mj_model')
    model = data.get('model')
    url = data.get('url')
    # 交由线程去执行耗时任务
    ret_mj = None
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_result = executor.submit(get_mj_images, prompt, mj_model, model,url)
        ret_mj = future_result.result()
        print(ret_mj)

    return jsonify(ret_mj)


# 创建一个 API 路由，接受 POST 请求，用户输入图片描述和风格，输出midjourney图片，同步方式，用于调试
@app.route('/api/get_mj_images_sync', methods=['POST'])
def get_mj_images_sync():
    # 从请求中获取关键词参数
    data = request.get_json()
    prompt = data.get('prompt')
    mj_model = data.get('mj_model')
    model = data.get('model')
    url = data.get('url')
    # 交由线程去执行耗时任务
    # 交由线程去执行耗时任务
    ret_mj = None
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_result = executor.submit(get_mj_images, prompt, mj_model, model, url)
        ret_mj = future_result.result()
        print(ret_mj)

    return jsonify(json.dumps(ret_mj))


def get_mj_images(prompt,mj_model,model,url):
    global url_mkj_prompt

    prompt_1 = ""

    if is_chinese_char(prompt):
        prompt_mj = get_mj_prompt(prompt, mj_model, model, url)
        prompt_all = prompt_mj
        prompt_1_start = prompt_all.index("imagine prompt:") + 15
        prompt_1_tmp = prompt_all[prompt_1_start:]
        prompt_1_end = prompt_1_tmp.index("imagine prompt:") - 13
        prompt_1 = prompt_1_tmp[:prompt_1_end]
        if prompt_1[len(prompt_1) - 1] == '.':
            prompt_1 = prompt_1[:-1]
    else:
        prompt_1 = prompt


    if url != "":
        prompt_1 = url + " " + prompt_1



    #调用MJ discord接口
    payload_mj = {"prompt": prompt_1}

    response_mj = requests.post(URL_MJ_PROMPT, data=json.dumps(payload_mj), headers={'Content-Type': 'application/json'})
    ret_mj = response_mj.json()
    if response_mj.status_code == 200:
        return ret_mj
        # return {'result': "200",
        #         'image_url': ret_mj['latest_image_url'],
        #         'message_id': ret_mj['latest_image_id']}
    else:
        return {'result': "500"}


#检查是否包含中文
def is_chinese_char(content_str):
    ret = False
    # 定义正则表达式模式
    pattern = re.compile(u'[\u4e00-\u9fa5]+')
    # 定义测试字符串
    # 使用search函数查找字符串中是否包含中文字符
    result = re.search(pattern, content_str)
    if result:
        ret = True
    else:
        ret = False
    return ret


if __name__ == "__main__":
    # 启动 Flask 应用
    app.run(debug=True, port=6001, host='0.0.0.0')
