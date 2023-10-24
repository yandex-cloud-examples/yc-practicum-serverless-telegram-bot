# Создадим бота с помощью BotFather
В телеграме найдите BotFather, вызовите команду `/newbot`, задайте имя новому боту.
Имя бота должно быть уникальным, используйте для этого номер своего аккаунта. 
Например, включайте `sls350` в название. 

В моем случае это — `ServerlessQuoteTelegram_bot`, 
также задайте username — `ServerlessQuoteTelegram_bot`. 
В результате вы получите `token`, сохраним его, он потребуется на следующих этапах.

    echo "export TELEGRAM_BOT_TOKEN=<YOUR_TELEGRAM_BOT_TOKEN>" >> ~/.bashrc && . ~/.bashrc
    echo $TELEGRAM_BOT_TOKEN

С помощью команды `/setuserpic` установите иконку для вашего бота `sayhello.png`

## Видео

https://youtu.be/ctgm7w1siYY

# [Следующий этап >>>](../02-create-service-account/README.md)
