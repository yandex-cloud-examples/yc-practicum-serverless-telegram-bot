# Обновление функции

У нас уже была сделана функция `first-bot-function` обновим ее для работы с Object Storage. 
Находясь в директории с исходными файлами, упакуем все нужные нам файлы в zip-архив:

    cd ../10-update-first-bot-function/
    zip src.zip index.py requirements.txt 

В переменные окружения функции необходимо добавить шесть переменных: 
`TELEGRAM_BOT_TOKEN`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`,
`BUCKET_NAME`, `YDB_ENDPOINT` и `YDB_DATABASE`.
Все переменные у нас уже лежат в секрете с именем `bot-secrets` и ключи наших секретов идентичны ключам переменных.
Посмотрим конфигурацию секрета `bot-secrets`:

    yc lockbox secret get --name bot-secrets

Важно, чтобы передать в конфигурации функции параметры наших переменных нужно взять `id` секрета `bot-secrets`,
пусть для примера он будет равен `e6qbrqvn8jv0gtfhkr5q`. Взять `version-id` это `id` от `current_version`,
пусть для примера он будет равен `e6qej8pukfhq94petq0t`.

Важно, если вы обновляли секрет то текущая версия **будет отличаться** от ранее использованной!

Не забывайте подставить свои значения `id` и `version-id`:

    yc serverless function version create \
    --function-name first-bot-function \
    --memory 128m \
    --execution-timeout 5s \
    --runtime python311 \
    --entrypoint index.handler \
    --service-account-id $SERVICE_ACCOUNT_DEPLOY_ID \
    --secret environment-variable=TELEGRAM_BOT_TOKEN,id=e6qbrqvn8jv0gtfhkr5q,version-id=e6qdp3lmb1up5pu0ntnq,key=TELEGRAM_BOT_TOKEN \
    --secret environment-variable=AWS_ACCESS_KEY_ID,id=e6qbrqvn8jv0gtfhkr5q,version-id=e6qdp3lmb1up5pu0ntnq,key=AWS_ACCESS_KEY_ID \
    --secret environment-variable=AWS_SECRET_ACCESS_KEY,id=e6qbrqvn8jv0gtfhkr5q,version-id=e6qdp3lmb1up5pu0ntnq,key=AWS_SECRET_ACCESS_KEY \
    --secret environment-variable=BUCKET_NAME,id=e6qbrqvn8jv0gtfhkr5q,version-id=e6qdp3lmb1up5pu0ntnq,key=BUCKET_NAME \
    --secret environment-variable=YDB_ENDPOINT,id=e6qbrqvn8jv0gtfhkr5q,version-id=e6qdp3lmb1up5pu0ntnq,key=YDB_ENDPOINT \
    --secret environment-variable=YDB_DATABASE,id=e6qbrqvn8jv0gtfhkr5q,version-id=e6qdp3lmb1up5pu0ntnq,key=YDB_DATABASE \
    --source-path src.zip

Успешный деплой функции проверим через отправку сообщений в телеграм.

## Видео

https://youtu.be/D_w9koTV6Yk

# [Следующий этап >>>](../11-deleting-resources/README.md)
