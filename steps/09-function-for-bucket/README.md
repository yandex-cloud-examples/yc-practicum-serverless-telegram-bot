# Создание функции для выгрузки данных в Object Storage

До этого момента наш бот брал данные из YDB, 
но мы можем использовать Object Storage для хранения подготовленных данных.
Создадим небольшую функцию с помощью которой переложим данные из базы данных в Object Storage.

Для этого мы будем использовать ключ, секрет и название бакета, созданные на ранних этапах:

    echo $AWS_ACCESS_KEY_ID
    echo $AWS_SECRET_ACCESS_KEY
    echo $BUCKET_NAME

Находясь в директории с исходными файлами нашей функции, упакуем нужные нам файлы в zip-архив:

    cd ../09-function-for-bucket/    
    zip src.zip index.py requirements.txt

В переменные окружения функции необходимо добавить пять переменных: 
`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, 
`BUCKET_NAME`, `YDB_ENDPOINT` и `YDB_DATABASE`.
Все переменные у нас уже лежат в секрете с именем `bot-secrets` 
и ключи наших секретов идентичны ключам переменных.
Посмотрим конфигурацию секрета `bot-secrets`:

    yc lockbox secret get --name bot-secrets

Важно, чтобы передать в конфигурации функции параметры наших переменных нужно взять `id` секрета `bot-secrets`,
пусть для примера он будет равен `e6qbrqvn8jv0gtfhkr5q`. Взять `version-id` это `id` от `current_version`,
пусть для примера он будет равен `e6qej8pukfhq94petq0t`. 

Важно, если вы обновляли секрет то текущая версия **будет отличаться** от ранее использованной!

Создайте функцию с именем `function-for-bucket`:

    yc serverless function create --name function-for-bucket

При создании функции вы получите URL по которому можно будет сделать вызов функции `http_invoke_url`. 
По умолчанию функция будет не публичной.

Находясь в директории с файлом `src.zip` вызовите следующую команду, 
это позволит вам загрузите код функции в облако и создать ее версию.
Не забывайте подставить свои значения `id` и `version-id`:

    yc serverless function version create \
    --function-name function-for-bucket \
    --memory 128m \
    --execution-timeout 5s \
    --runtime python311 \
    --entrypoint index.handler \
    --service-account-id $SERVICE_ACCOUNT_DEPLOY_ID \
    --secret environment-variable=AWS_ACCESS_KEY_ID,id=e6qbrqvn8jv0gtfhkr5q,version-id=e6qdp3lmb1up5pu0ntnq,key=AWS_ACCESS_KEY_ID \
    --secret environment-variable=AWS_SECRET_ACCESS_KEY,id=e6qbrqvn8jv0gtfhkr5q,version-id=e6qdp3lmb1up5pu0ntnq,key=AWS_SECRET_ACCESS_KEY \
    --secret environment-variable=BUCKET_NAME,id=e6qbrqvn8jv0gtfhkr5q,version-id=e6qdp3lmb1up5pu0ntnq,key=BUCKET_NAME \
    --secret environment-variable=YDB_ENDPOINT,id=e6qbrqvn8jv0gtfhkr5q,version-id=e6qdp3lmb1up5pu0ntnq,key=YDB_ENDPOINT \
    --secret environment-variable=YDB_DATABASE,id=e6qbrqvn8jv0gtfhkr5q,version-id=e6qdp3lmb1up5pu0ntnq,key=YDB_DATABASE \
    --source-path src.zip

Успешный деплой функции проверим через публичный вызов.

## Вызов функции

Получите список функций и получите информацию о функции `function-for-bucket`:

    yc serverless function list
    yc serverless function version list --function-name function-for-bucket

В результате вызова последней команды в столбце `FUNCTION ID` 
вы узнаете идентификатор функции и сможете сделать вызов функции с помощью следующей команды:

    yc serverless function invoke <идентификатор функции>

По умолчанию функция создается не публичной. Чтобы сделать функцию `first-bot-function` публичной, 
вызовете следующую команду:

    yc serverless function allow-unauthenticated-invoke function-for-bucket

После этого вы можете сделать ее вызов в браузере. 
Получите параметр `http_invoke_url` для функции `first-bot-function`

    yc serverless function get function-for-bucket

Введите значение параметра `http_invoke_url` в браузере и проверьте что стало с бакетом.

## Видео

https://youtu.be/P2aGe7r0BVo

# [Следующий этап >>>](../10-update-first-bot-function/README.md)