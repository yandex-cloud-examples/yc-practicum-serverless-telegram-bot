# Обновление функции

До этого момента мы использовали рантайм `python311`, и у нас была очень простая функция. 
Если вы подключаете сторонние библиотеки необходимо их указывать явно. 
Для этого их нужно поместить в файл `requirements.txt` есть удобная python библиотека `pipreqs` которая вам может помочь. 
Для генерации `requirements.txt` с помощью `pipreqs` достаточно указать рабочий каталог. 

В большинстве интерпритаторов linux для указания текущего каталога есть переменная `$PWD`. 
Если файл `requirements.txt` уже есть и его нужно актуализировать то используется флаг `--force`, например:

    pip install pipreqs
    pipreqs $PWD --print
    pipreqs $PWD --force

В нашем случае уже имеется нужный файл с нужными библиотеками.
Теперь функция состоит из двух файлов. 
Находясь в директории с исходными файлами, упакуем все нужные нам файлы в zip-архив:

    cd ..
    cd 06-update-function/
    zip src.zip index.py requirements.txt 

В переменные окружения функции необходимо добавить три переменные: 
`TELEGRAM_BOT_TOKEN`, `YDB_ENDPOINT` и `YDB_DATABASE`.
Все переменные у нас уже лежат в секрете с именем `bot-secrets` и ключи наших секретов идентичны ключам переменных. 
Посмотрим конфигурацию секрета `bot-secrets`:

    yc lockbox secret get --name bot-secrets

Важно, чтобы передать в конфигурации функции параметры наших переменных нужно взять `id` секрета `bot-secrets`, 
пусть для примера он будет равен `e6qbrqvn8jv0gtfhkr5q`. Взять `version-id` это `id` от `current_version`, 
пусть для примера он будет равен `e6qej8pukfhq94petq0t`. 

Чтобы передеплоить функцию с новыми параметрами, находясь в директории с архивом, вызовем следующую команду, 
не забыв подставить свои значения `id` и `version-id`: 

    yc serverless function version create \
    --function-name first-bot-function \
    --memory 128m \
    --execution-timeout 5s \
    --runtime python311 \
    --entrypoint index.handler \
    --service-account-id $SERVICE_ACCOUNT_DEPLOY_ID \
    --secret environment-variable=TELEGRAM_BOT_TOKEN,id=e6qbrqvn8jv0gtfhkr5q,version-id=e6qej8pukfhq94petq0t,key=TELEGRAM_BOT_TOKEN \
    --secret environment-variable=YDB_ENDPOINT,id=e6qbrqvn8jv0gtfhkr5q,version-id=e6qej8pukfhq94petq0t,key=YDB_ENDPOINT \
    --secret environment-variable=YDB_DATABASE,id=e6qbrqvn8jv0gtfhkr5q,version-id=e6qej8pukfhq94petq0t,key=YDB_DATABASE \
    --source-path src.zip

Успешный деплой функции проверим через отправку сообщений в телеграм.

## Видео

https://youtu.be/LF1SvzI2y2w

# [Следующий этап >>>](../07-create-key/README.md)
