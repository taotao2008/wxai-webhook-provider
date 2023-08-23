import requests
import json

from config.ConfigVars import QMAI_DELETE_MESSAGE_APP_URL, X_AUTH_TOKEN, X_USER_ID


def delete_message(roomId, msgId):
  payload = json.dumps({
    "roomId": roomId,
    "msgId": msgId,
    "asUser": False
  })
  headers = {
    'X-Auth-Token': X_AUTH_TOKEN,
    'X-User-Id': X_USER_ID,
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", QMAI_DELETE_MESSAGE_APP_URL, headers=headers, data=payload)

  print(response.text)
  # print(response.text)
  response_json = json.loads(response.text)
  if (response_json['success']):
    return "SUCCESS"
  else:
    return "ERROR"
