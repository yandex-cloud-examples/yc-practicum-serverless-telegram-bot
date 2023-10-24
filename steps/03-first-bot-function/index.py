import os
import requests
import json

# Telegram Bot Token
# token = "TELEGRAM_BOT_TOKEN"
token = os.getenv('TELEGRAM_BOT_TOKEN')


# send message function
def send_message(chat_id, text):
    #url = 'https://api.telegram.org/bot' + token + '/' + 'sendMessage'
    url = "https://api.telegram.org/bot%s/sendMessage" % (token)
    data = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, data=data)
    return r


def handler(event, context):
    try:
        body = json.loads(event['body'])
        chat_id = body['message']['from']['id']
        text_from_user = body['message']['text']

        print(body)
        print(text_from_user)

        send_message(chat_id, text_from_user)
        r = {'statusCode': 200, 'body': 'Message sent'}

    except Exception as e:
        r = {'statusCode': 404, 'body': 'Same error'}

    return r
