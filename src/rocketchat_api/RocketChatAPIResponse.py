import requests
import os
import json

global sender_params
current_directory = os.path.dirname(os.path.abspath(__file__))
params = os.path.join(current_directory, 'sender_params.json')
with open(params, 'r') as f:
    sender_params = json.load(f)


def postCreateImRoom(wxai_url, wxai_token, wxai_user_id, user_name, bot_name):
    url = wxai_url + "/api/v1/im.create"
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

                if not ret_open_room.get('success'):
                    return {'status': 'ERROR'}
            else:
                return {'status': 'ERROR'}
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
            "language": "zh",
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
        if not ret_set_preferences.get('success'):
            return {'status': 'ERROR'}

    return {'status': 'success'}



if __name__ == '__main__':
    #user_name = 'taotao2010'
    #print(createImRoomAll(user_name))

    user_id = 'XiP8jfr7Muf2x2vKW'
    print(setPreferencesAll(user_id))
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # loop.run_until_complete(getInstance())
