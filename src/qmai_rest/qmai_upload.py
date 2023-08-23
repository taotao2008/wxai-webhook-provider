import json

import requests


from src.config.ConfigVars import X_AUTH_TOKEN, X_USER_ID, QMAI_UPLOAD_URL


def uploadFile(file_dir, file_name):
  payload = {}
  files=[
    ('file',(file_name,open(file_dir + '/' + file_name,'rb'),'audio/mp3'))
  ]
  headers = {
    'X-Auth-Token': X_AUTH_TOKEN,
    'X-User-Id': X_USER_ID
  }

  response = requests.request("POST", QMAI_UPLOAD_URL, headers=headers, data=payload, files=files)

  print(response.text)
  response_json = json.loads(response.text)
  if (response_json['success']) :
    return response_json['message']['attachments'][0]['audio_url']
  else:
    return "ERROR"



def uploadCostomFile(file_path, file_name):
  payload = {}
  files=[
    ('file',(file_name,open(file_path,'rb')))
  ]
  headers = {
    'X-Auth-Token': X_AUTH_TOKEN,
    'X-User-Id': X_USER_ID
  }

  response = requests.request("POST", QMAI_UPLOAD_URL, headers=headers, data=payload, files=files)

  #print(response.text)
  response_json = json.loads(response.text)
  if (response_json['success']) :
    return response_json['message']['attachments'][0]['title_link']
  else:
    return "ERROR"




def uploadImagine(file_path, file_name):
  payload = {}
  files=[
    ('file',(file_name,open(file_path,'rb'),'image/jpeg'))
  ]
  headers = {
    'X-Auth-Token': X_AUTH_TOKEN,
    'X-User-Id': X_USER_ID
  }

  response = requests.request("POST", QMAI_UPLOAD_URL, headers=headers, data=payload, files=files)

  #print(response.text)
  response_json = json.loads(response.text)
  if (response_json['success']) :
    return response_json['message']['attachments'][0]['title_link']
  else:
    return "ERROR"

def uploadFileTxt(file_dir, file_name):
  payload = {}
  files=[
    ('file',(file_name,open(file_dir + '/' + file_name,'rb'), 'text/x-spam'))
  ]
  headers = {
    'X-Auth-Token': X_AUTH_TOKEN,
    'X-User-Id': X_USER_ID
  }

  response = requests.request("POST", QMAI_UPLOAD_URL, headers=headers, data=payload, files=files)

  print(response.text)
  response_json = json.loads(response.text)
  if (response_json['success']) :
    return response_json['message']['attachments'][0]['title_link']
  else:
    return "ERROR"