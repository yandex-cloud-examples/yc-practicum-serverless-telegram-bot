import requests

TELEGRAM_BOT_TOKEN = "Ваш TELEGRAM_BOT_TOKEN"
TELEGRAM_BOT_URL = "https://<ID API Gateway>.apigw.yandexcloud.net/forwebhook"

url = "https://api.telegram.org/bot{token}/{method}".format(
    token = TELEGRAM_BOT_TOKEN,
    method = "setWebhook"
    #method="getWebhookinfo"
    #method = "deleteWebhook"
)

data = {"url": TELEGRAM_BOT_URL}

def main():
    r = requests.post(url, data=data)
    print(r.json())

if __name__ == "__main__":
    main()