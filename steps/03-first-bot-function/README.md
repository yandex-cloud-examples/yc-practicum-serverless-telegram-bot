# Создание первой функции для бота
## Создание функции

Создайте свою первую функцию с именем `first-bot-function`:

    cd steps/03-first-bot-function/
    yc serverless function create --name first-bot-function

При создании функции вы получите URL по которому можно будет сделать вызов функции `http_invoke_url`. По умолчанию функция будет не публичной.

## Загрузка кода

Находясь в директории с файлом `index.py` вызовите следующую команду, это позволит вам загрузите код функции в облако и создать ее версию:

    echo $SERVICE_ACCOUNT_DEPLOY_ID

    yc serverless function version create \
    --function-name first-bot-function \
    --memory 128m \
    --execution-timeout 5s \
    --runtime python311 \
    --entrypoint index.handler \
    --service-account-id $SERVICE_ACCOUNT_DEPLOY_ID \
    --environment TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN \
    --source-path index.py

Успешное выполнение команды приведет к созданию версии функции.

## Вызов функции

Получите список функций и получите информацию о функции `first-bot-function`:

    yc serverless function list
    yc serverless function version list --function-name first-bot-function

В результате вызова последней команды в столбце `FUNCTION ID` вы узнаете идентификатор функции и сможете сделать вызов функции с помощью следующей команды:

    yc serverless function invoke <идентификатор функции>

По умолчанию функция создается не публичной. Чтобы сделать функцию `first-bot-function` публичной, вызовете следующую команду:

    yc serverless function allow-unauthenticated-invoke first-bot-function

Принципиально бот можно настроить и с прямым вызовом функции. 
После предыдущей команды вы можете сделать вызов функции хоть в браузере. 
Для этого нужно получить параметр `http_invoke_url` для функции `first-bot-function`

    yc serverless function get first-bot-function

Можно ввести значение параметра `http_invoke_url` в браузере и насладиться вызовом вашей функции.
Но мы не будем так делать и скроем ее за экземпляром Yandex API Gateway. 

## Модификация спецификации и создание экземпляра Yandex API Gateway

В директории лежит файл `first-bot-apigw.yaml` в него необходимо внести ранее полученные данные. 
Вместо `<идентификатор функции>` вставить `FUNCTION ID` для ранее созданной функции `first-bot-function`. 
Вместо `<ID сервисного аккаунта>` вставить значение переменной `SERVICE_ACCOUNT_DEPLOY_ID`. 

После внесения изменений в спецификацию `first-bot-apigw.yaml`, используем ее для инициализации:

    yc serverless api-gateway create \
    --name first-bot-apigw \
    --spec=first-bot-apigw.yml \
    --description "first-bot-apigw"

В результате успешного создания API-шлюза получим `domain`:

    yc serverless api-gateway list
    yc serverless api-gateway get --name first-bot-apigw

Служебный домен нужен нам для того, чтобы соединить нашу функцию и телеграм, 
Согласно нашей спецификации, функция будет доступна по адресу если в конце `domain` дописать `/forwebhook`. 
Должно получиться следующее:

    https://<ID API Gateway>.apigw.yandexcloud.net/forwebhook

Сохраним полученный URL в переменную `TELEGRAM_BOT_URL`.

    echo "export TELEGRAM_BOT_URL=https://<ID API Gateway>.apigw.yandexcloud.net/forwebhook" >> ~/.bashrc && . ~/.bashrc
    echo $TELEGRAM_BOT_URL

## Регистрация вебхука

В директории есть небольшой простой скрипт `webhook-utils.py` для работы c webhook telegram. 
Для корректной работы необходимо в скрипте в переменные `TELEGRAM_BOT_TOKEN` и `TELEGRAM_BOT_URL` 
внести ваши значения.

Находясь в директории со скриптом `webhook-utils.py`, вызовите его. 
Возможно перед запуском скрипта вам потребуется установить библиотеку `requests` 
и возможно, перед этим потребуется вызвать команду `sudo apt update`:
 
    pip install requests 
    python3 webhook-utils.py

Если все удачно прошло, то вы получите ответ от API Telegram:

    {'ok': True, 'result': True, 'description': 'Webhook was set'}

## Видео

https://youtu.be/A5DGogHIUuc и финал https://youtu.be/MEpYJs2TXVI

# [Следующий этап >>>](../04-create-database/README.md)