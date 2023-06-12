from flask import Flask, request, jsonify
import json
import os
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import re
# DOCS https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor
# 创建线程池执行器
from rocketchat_api.RocketChatAPIResponse import createImRoomAll
from rocketchat_api.RocketChatAPIResponse import setPreferencesAll

executor = ThreadPoolExecutor(10)

# 创建 Flask 应用
app = Flask(__name__)


# 创建一个 API 路由，接受 POST 请求，用户输入图片描述和风格，生成MJ适用的prompt
@app.route('/api/user_created_webhook', methods=['POST'])
def send_message_webhook():
    # 从请求中获取关键词参数
    data = request.get_json()
    print(data)
    user_name = data.get('user_name')
    user_id = data.get('user_id')

    # 交由线程去执行耗时任务
    ret = None
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_result = executor.submit(userCreatedWebhookFun, user_name, user_id)
        ret = future_result.result()

    return jsonify(ret)


def userCreatedWebhookFun(user_name, user_id):
    # 响应返回
    ret = createImRoomAll(user_name)
    ret2 = setPreferencesAll(user_id)
    return ret


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
    app.run(debug=True, port=6005, host='0.0.0.0')
