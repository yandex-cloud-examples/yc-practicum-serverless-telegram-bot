# Cоздание YDB
## Создание экземпляра YDB для хранения данных игры

Создадим базу данных YDB с именем `bot-data` и типом serverless используя для этого флаг `--serverless`:

    cd ..
    cd 04-create-database/
    yc ydb database create bot-data --serverless --folder-id $YC_FOLDER_ID
    yc ydb database list

Сразу получим и сохраним значение `endpoint` и `database` в значение переменной `YDB_ENDPOINT` и `YDB_DATABASE`
они нужны будут для подключения наших функций.

В выводе следующей команды есть значение `endpoint` оно обычно состоит из необходимых нам `YDB_ENDPOINT` и `YDB_DATABASE`.
Например, в строке `grpcs://ydb.serverless.yandexcloud.net:2135/?database=/ru-central1/b1gvr958gmn7ibs9vfib/etnovd16d79gc946q6ph`
первая часть `grpcs://ydb.serverless.yandexcloud.net:2135` это `YDB_ENDPOINT`,
а вторая `/ru-central1/b1gvr958gmn7ibs9vfib/etnovd16d79gc946q6ph` это `YDB_DATABASE`.

    yc ydb database get --name bot-data

    echo "export YDB_ENDPOINT=<YDB_ENDPOINT>" >> ~/.bashrc && . ~/.bashrc
    echo $YDB_ENDPOINT

    echo "export YDB_DATABASE=<YDB_DATABASE>" >> ~/.bashrc && . ~/.bashrc
    echo $YDB_DATABASE

## Генерируем ключ для сервисного аккаунта

Команды на этом шаге нужно выполнять в каталоге шага, или в каталоге куда вы поместите необходимые файлы.
Для дальнейшей работы воспользуемся утилитой `ydb`, мы ее устанавливали на этапе настройки окружения:

    curl https://storage.yandexcloud.net/yandexcloud-ydb/install.sh | bash

С помощью CLI Yandex Cloud создадим авторизованный ключ сервисного аккаунта `sls-deploy`:

    yc iam key create \
    --service-account-name <имя_сервисного_аккаунта> \
    --output <имя_файла>

В нашем случае команда будет выглядеть так:

    yc iam key create \
    --service-account-name sls-deploy \
    --output sls-deploy.sa

    echo "export SA_KEY_FILE=$PWD/sls-deploy.sa" >> ~/.bashrc && . ~/.bashrc  
    echo $SA_KEY_FILE

Проверим работоспособность с помощью команды:

    ydb \
    --endpoint <эндпоинт> \
    --database <база данных> \
    --sa-key-file <путь к файлу с ключом>\
    discovery whoami \
    --groups

В нашем случае команда будет выглядеть так:

    ydb \
    --endpoint $YDB_ENDPOINT \
    --database $YDB_DATABASE \
    --sa-key-file $SA_KEY_FILE \
    discovery whoami \
    --groups

## Создадим таблицы в YDB

В каталоге имеется файл `db-example.sql` и выполнив следующую команду мы создадим
нужные для работы приложения таблицы на сервере:

    ydb \
    --endpoint $YDB_ENDPOINT \
    --database $YDB_DATABASE \
    --sa-key-file $SA_KEY_FILE \
    scripting yql --file db-example.sql

Если с помощью файл `db-example.sql` была создана структура БД, 
то далее мы добавим записи — «стартовую конфигурацию»:

    ydb \
    --endpoint $YDB_ENDPOINT \
    --database $YDB_DATABASE \
    --sa-key-file $SA_KEY_FILE \
    scripting yql --file db-update.sql

Можем проверить результат выполнения:

    ydb \
    --endpoint $YDB_ENDPOINT \
    --database $YDB_DATABASE \
    --sa-key-file $SA_KEY_FILE \
    scheme describe Quotes

## Видео

https://youtu.be/snIgoc7xbqQ

# [Следующий этап >>>](../05-create-lockbox/README.md)