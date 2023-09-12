import random

import requests
import os
import json

from config.ConfigVars import QMAI_URL_BASE
from qmai_rest.qmai_upload import uploadImagine
from utils.audio_util import download_file, get_filename_from_url

global sender_params
current_directory = os.path.dirname(os.path.abspath(__file__))
params = os.path.join(current_directory, 'sender_params.json')
with open(params, 'r') as f:
    sender_params = json.load(f)


def postCreateImRoom(wxai_url, wxai_token, wxai_user_id, user_name, bot_name):
    url = wxai_url + "/api/v1/im.create.auto"
    headers = {
        'X-Auth-Token': wxai_token,  # access_token 是你的访问令牌
        'X-User-Id': wxai_user_id
    }

    playload = {
        "usernames": user_name + "," + bot_name,
        "excludeSelf": True,
        "x_user_id": wxai_user_id
    }

    response = requests.post(url, json=playload, headers=headers)
    return response.json()


def postOpenImRoom(wxai_url, wxai_token, wxai_user_id, room_id):
    url = wxai_url + "/api/v1/im.open"
    headers = {
        'X-Auth-Token': wxai_token,  # access_token 是你的访问令牌
        'X-User-Id': wxai_user_id
    }

    playload = {
        "roomId": room_id
    }

    response = requests.post(url, json=playload, headers=headers)
    return response.json()


def createImRoomAll(user_name):
    global sender_params
    for server in sender_params.get('servers'):
        url = server.get('url')
        token = server.get('token')
        user_id = server.get('user_id')
        bots = server.get('bots')
        for bot_name in bots:
            ret_room = postCreateImRoom(url, token, user_id, user_name, bot_name)
            print(ret_room)
            if ret_room.get('success'):
                room_id = ret_room.get('room').get('rid')
                ret_open_room = postOpenImRoom(url, token, user_id, room_id)

    return {'status': 'success'}


def postPreferences(wxai_url, wxai_token, wxai_user_id, user_id):
    url = wxai_url + "/api/v1/users.setPreferences"
    headers = {
        'X-Auth-Token': wxai_token,  # access_token 是你的访问令牌
        'X-User-Id': wxai_user_id
    }


    playload = {
        "userId": user_id,
        "data": {
            #"language": "zh",
            "sidebarGroupByType": True,
            "sidebarShowFavorites":True
        }
    }

    response = requests.post(url, json=playload, headers=headers)
    return response.json()


def setPreferencesAll(setting_user_id):
    global sender_params
    for server in sender_params.get('servers'):
        url = server.get('url')
        token = server.get('token')
        user_id = server.get('user_id')

        ret_set_preferences = postPreferences(url, token, user_id, setting_user_id)

    return {'status': 'success'}

def setAvatar(wxai_url, wxai_token, wxai_user_id, user_id, avatarUrl):

    url = wxai_url + "/api/v1/users.setAvatar"

    payload = json.dumps({
        "avatarUrl": avatarUrl,
        "userId": user_id
    })
    headers = {
        'X-Auth-Token': wxai_token,
        'X-User-Id': wxai_user_id,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return response.json()



def setAvatarAll(setting_user_id):
    global sender_params
    random_id = random.randint(1, 2000)
    filename_or_dir = "./images/"
    url = "https://shop.jind.cloud/avatars/avatar" + str(random_id) + ".jpg"
    # 下载文件
    file_path = download_file(url, filename_or_dir)
    # print(file_path)

    # 上传到room
    file_name = get_filename_from_url(url)
    image_url = uploadImagine(file_path, file_name)
    # 成功则发送im messaging
    if (image_url != 'ERROR'):
        for server in sender_params.get('servers'):
            wxai_url = server.get('url')
            wxai_token = server.get('token')
            wxai_user_id = server.get('user_id')

            avatarUrl = QMAI_URL_BASE + image_url
            #avatarUrl = 'https://chat.qmai.chat/file-upload/YMd8HtsahJRY7xGpr/avatar13.jpg?download'
            setAvatar(wxai_url, wxai_token, wxai_user_id, setting_user_id, avatarUrl)

    return {'status': 'success'}



if __name__ == '__main__':
    user_name = 'a2030'
    print(createImRoomAll(user_name))

    #user_id = 'ZbZXTAhY8KEX4ZkHG'
    #print(setAvatarAll(user_id))

    #user_id = 'XiP8jfr7Muf2x2vKW'
    #print(setPreferencesAll(user_id))
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # loop.run_until_complete(getInstance())
