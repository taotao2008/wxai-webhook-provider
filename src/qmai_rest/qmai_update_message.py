import requests
import json
import time
from config.ConfigVars import X_AUTH_TOKEN, X_USER_ID, QMAI_CHAT_UPDATE_APP_URL, QMAI_URL_BASE
from utils.audio_util import get_filename_from_url


def update_message(roomId, msgId, audio_url, prompt):
    filenameStart = str(audio_url).rindex('/')
    filename = str(audio_url)[filenameStart + 1:]
    current_dateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    audio_url_download = QMAI_URL_BASE + audio_url

    text = f"""
**文本转语音已完成！**   [音频下载]({audio_url_download}) 
**Prompt预览**：{prompt[:180]}...
  """
    payload = json.dumps({
        "roomId": roomId,
        "msgId": msgId,
        "text": text,
        "attachments": [
            {
                "title": filename,
                "title_link": audio_url,
                "title_link_download": True,
                "audio_url": audio_url,
                "audio_type": "audio/mp3",
                "type": "file",
                "description": text,
                "descriptionMd": [
                    {
                        "type": "PARAGRAPH",
                        "value": [
                            {
                                "type": "PLAIN_TEXT",
                                "value": ""
                            }
                        ]
                    }
                ]
            }

        ]
    })
    headers = {
        'X-Auth-Token': X_AUTH_TOKEN,
        'X-User-Id': X_USER_ID,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", QMAI_CHAT_UPDATE_APP_URL, headers=headers, data=payload)

    # print(response.text)
    response_json = json.loads(response.text)
    if (response_json['success']):
        return "SUCCESS"
    else:
        return "ERROR"


def update_message_speech2txt_file(roomId, msgId, txt_url, content_txt, audio_url, sumarize_content):
    filenameStart = str(txt_url).rindex('/')
    filename = str(txt_url)[filenameStart + 1:]
    filename_audio = get_filename_from_url(audio_url)

    current_dateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    text = ''
    if (len(sumarize_content) > 0):
        text = f"""
    **语音转会议纪要已完成**
    **会议纪要总结**：\n {sumarize_content}\n 
    **译文预览**：\n {content_txt[:180]}...
      """
    else:
        text = f"""
    **语音转文本已完成**
    **译文预览**：\n {content_txt[:180]}...
      """

    #   text = f"""
    # **语音转文本已完成**
    # **译文预览**：\n {content_txt[:180]}...
    #   """
    payload = json.dumps({
        "roomId": roomId,
        "msgId": msgId,
        "text": text,
        "attachments": [
            {
                "title": '完整译文.txt',
                "title_link": txt_url,
                "title_link_download": True,
                "type": "file",
                "description": text,
                "descriptionMd": [
                    {
                        "type": "PARAGRAPH",
                        "value": [
                            {
                                "type": "PLAIN_TEXT",
                                "value": ""
                            }
                        ]
                    }
                ]
            },
            {
                "title": filename_audio,
                "title_link": audio_url,
                "title_link_download": True,
                "audio_url": audio_url,
                "type": "file",
                "description": text,
                "descriptionMd": [
                    {
                        "type": "PARAGRAPH",
                        "value": [
                            {
                                "type": "PLAIN_TEXT",
                                "value": ""
                            }
                        ]
                    }
                ]
            }

        ]
    })
    headers = {
        'X-Auth-Token': X_AUTH_TOKEN,
        'X-User-Id': X_USER_ID,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", QMAI_CHAT_UPDATE_APP_URL, headers=headers, data=payload)

    # print(response.text)
    response_json = json.loads(response.text)
    if (response_json['success']):
        return "SUCCESS"
    else:
        return "ERROR"


def update_message_ai_remove_noise_finished(roomId, msgId, file_name, audio_url, file_name_before, audio_url_before):
    current_dateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    audio_url_download = QMAI_URL_BASE + audio_url

    audio_url_before_download = QMAI_URL_BASE + audio_url_before

    text = f"""
      ** AI降噪任务已完成！**  [降噪后音频下载]({audio_url_download}) | [降噪前音频下载]({audio_url_before_download}) 
        """

    payload = json.dumps({
        "roomId": roomId,
        "msgId": msgId,
        "text": "",
        "attachments": [
            {
                "title": file_name,
                "title_link": audio_url,
                "title_link_download": True,
                "audio_url": audio_url,
                "audio_type": "audio/mp3",
                "type": "file",
                "description": text + "\n降噪后",
                "descriptionMd": [
                    {
                        "type": "PARAGRAPH",
                        "value": [
                            {
                                "type": "PLAIN_TEXT",
                                "value": "降噪后"
                            }
                        ]
                    }
                ]
            },
            {
                "title": file_name_before,
                "title_link": audio_url_before,
                "title_link_download": True,
                "audio_url": audio_url_before,
                "audio_type": "audio/mp3",
                "type": "file",
                "description": "降噪前",
                "descriptionMd": [
                    {
                        "type": "PARAGRAPH",
                        "value": [
                            {
                                "type": "PLAIN_TEXT",
                                "value": "降噪前"
                            }
                        ]
                    }
                ]
            }

        ]
    })
    headers = {
        'X-Auth-Token': X_AUTH_TOKEN,
        'X-User-Id': X_USER_ID,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", QMAI_CHAT_UPDATE_APP_URL, headers=headers, data=payload)

    # print(response.text)
    response_json = json.loads(response.text)
    if (response_json['success']):
        return "SUCCESS"
    else:
        return "ERROR"


def update_message_ai_remove_noise_other_type(roomId, msgId, other_type, message_str):
    current_dateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    if (other_type == 'failed'):
        text = f"""
          AI降噪任务执行失败，失败原因：{message_str} 
            """
    elif (other_type == 'in_progress'):
        text = f"""
              AI降噪正在处理中，当前进度：{message_str} 
                """
    elif (other_type == 'queued'):
        text = f"""
              AI降噪任务正在排队中，前面还有：{message_str} 
                """
    elif (other_type == 'downloading'):
        text = f"""
              AI降噪任务正在下载：{message_str} 
                """

    payload = json.dumps({
        "roomId": roomId,
        "msgId": msgId,
        "text": "",
        "attachments": [
            {
                "color": "#ff0000",
                "text": text
            }

        ]
    })
    headers = {
        'X-Auth-Token': X_AUTH_TOKEN,
        'X-User-Id': X_USER_ID,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", QMAI_CHAT_UPDATE_APP_URL, headers=headers, data=payload)

    # print(response.text)
    response_json = json.loads(response.text)
    if (response_json['success']):
        return "SUCCESS"
    else:
        return "ERROR"
