# Создание Lockbox

Создадим секрет с именем `bot-secrets` и поместим пару переменных со значениями `YDB_ENDPOINT` и `YDB_DATABASE`

    yc lockbox secret create --name bot-secrets \
    --description "The secrets for the serverless bot" \
    --payload "[{'key': 'YDB_ENDPOINT', 'text_value': $YDB_ENDPOINT},{'key': 'YDB_DATABASE', 'text_value': $YDB_DATABASE}]" \
    --cloud-id $YC_CLOUD_ID \
    --folder-id $YC_FOLDER_ID 

Сохраним ID созданного секрета, и можно подсмотреть и вставить ручками:

    yc lockbox secret list
    echo "export LOCKBOX_SECRET_ID=<ID>" >> ~/.bashrc && . ~/.bashrc

Или автоматизированно:

    echo "export LOCKBOX_SECRET_ID=$(jq -r <<<  \
    "$(yc lockbox secret list --format json | jq '.[]' -c | grep bot-secrets)" .id)"  \
    >> ~/.bashrc && . ~/.bashrc

    echo $LOCKBOX_SECRET_ID

Токен нашего бота тоже лучше положить в секрет, чтобы можно было из функции к нему обращаться.
Проверьте значение своего токена и сохраните его:

    echo $TELEGRAM_BOT_TOKEN

    yc lockbox secret add-version --id $LOCKBOX_SECRET_ID \
    --payload "[{'key': 'TELEGRAM_BOT_TOKEN', 'text_value': '$TELEGRAM_BOT_TOKEN'}]"

## Видео

https://youtu.be/xHWkHiDaY6g

# [Следующий этап >>>](../06-update-function/README.md)