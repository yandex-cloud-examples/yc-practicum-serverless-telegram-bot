# Настройка окружения для практикума

## Оглавление
1. [Предварительная инсталляция](#Предварительная-инсталляция)
2. [Получение логина и пароля](#Получение-логина-и-пароля)
3. [Подключение к чату практикума](#Подключение-к-чату-практикума)

## Предварительная инсталляция

Для работы вам потребуются:
- IntelliJ IDEA Community Edition (хотя, вы можете попробовать использовать свою любимую IDE) 
- curl
- git
- jq
- zip
- yc (Yandex Cloud CLI)
- aws (Amazon Web Services CLI)
- ydb (YDB CLI)
- python == 3.11.0
- 

Ниже описаны шаги для их установки на различных операционных системах.

### MacOS
#### Установите утилиту brew

Установите [brew](https://brew.sh):

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### IntelliJ IDEA Community Edition

Скачайте и установите дистрибутив IntelliJ IDEA Community Edition, дистрибутив скачать можно [здесь](https://www.jetbrains.com/ru-ru/idea/download/#section=mac).

#### Установите утилиты curl и git

```bash
brew install curl git
```

#### Установите утилиту jq

```bash
brew install jq
```

#### Установите python3

```bash
brew install python3
```

#### Установите terraform

```bash
brew install terraform
```
Обязательно настройте кастомных провайдеров согласно инструкции https://cloud.yandex.ru/docs/tutorials/infrastructure-management/terraform-quickstart#configure-provider

#### Установите утилиту yc CLI

Установите [yc CLI](https://cloud.yandex.ru/docs/cli/operations/install-cli#interactive):

```bash
curl -sSL https://storage.yandexcloud.net/yandexcloud-yc/install.sh | bash
exec -l $SHELL
yc version
```

#### aws CLI

Установите [aws CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-mac.html):

```bash
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
```

Конфигурирование обычно делается по [инструкции](https://cloud.yandex.ru/docs/ydb/quickstart/document-api/aws-setup),
но в этом практикуме, настройку мы будем делать на одном из следующих шагов.

#### ydb CLI

Установите [ydb CLI](https://ydb.tech/ru/docs/reference/ydb-cli/install):
Новым способом
```bash
curl -sSL https://install.ydb.tech/cli | bash
exec -l $SHELL 
ydb version
```

или старым способом
```bash
curl -sSL https://storage.yandexcloud.net/yandexcloud-ydb/install.sh | bash
exec -l $SHELL 
ydb version
```


### Windows

- [Установите WSL](https://docs.microsoft.com/en-us/windows/wsl/install)
- Запустите Ubuntu Linux
- Настройте согласно инструкции для Ubuntu Linux

### Ubuntu Linux

В случае Linux, отличного от Ubuntu, установите те же пакеты, используя пакетный менеджер вашего дистрибутива.

#### IntelliJ IDEA Community Edition

Скачайте и установите дистрибутив IntelliJ IDEA Community Edition, дистрибутив скачать можно [здесь](https://www.jetbrains.com/ru-ru/idea/download/#section=linux).

#### Установите утилиты curl и git

```bash
sudo apt-get install curl git -y
```

#### Установите утилиту jq
Все варианты дистрибутива jq и инструкции можно [посмотреть тут](https://stedolan.github.io/jq/download/).

```bash
sudo apt-get install jq
```

#### Установите python3
Скорее всего python3 у вас уже установлен, но можно это легко проверить: 
где он установлен, какая у него версия, и при необходимости обновить:
```bash
which python3
python3 --version
sudo apt-get upgrade python3
```

#### Установите утилиту yc CLI

Установите [yc CLI](https://cloud.yandex.ru/docs/cli/operations/install-cli#interactive):

```bash
curl https://storage.yandexcloud.net/yandexcloud-yc/install.sh | bash
exec -l $SHELL
yc version
```

#### aws CLI

Установите [aws CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html):

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

Конфигурирование обычно делается по [инструкции](https://cloud.yandex.ru/docs/ydb/quickstart/document-api/aws-setup),
но в этом практикуме, настройку мы будем делать на одном из следующих шагов.

#### ydb CLI

Установите [ydb CLI](https://ydb.tech/ru/docs/reference/ydb-cli/install):
Новым способом
```bash
curl -sSL https://install.ydb.tech/cli | bash
exec -l $SHELL 
ydb version
```

или старым способом
```bash
curl -sSL https://storage.yandexcloud.net/yandexcloud-ydb/install.sh | bash
exec -l $SHELL 
ydb version
```

## Получение логина и пароля
### Подключение к веб-консоли
Для работы в веб-консоли Yandex Cloud рекомендуется использовать [Яндекс браузер](https://browser.yandex.ru).

Примерно за сутки или двое до начала практикума вы получите специальное письмо с логином и паролем для доступа в облако.
Вам необходимо использовать их для входа в веб-консоль Yandex Cloud.
Ваш пользователь уникальный и создан в федерации, для входа воспользуйтесь следующей ссылкой —
[URL для подключения](https://console.cloud.yandex.ru/federations/bpffbnnnuauomglir5k7).

После входа будет редирект в Keycloak. В котором нужно аутентифицироваться с полученной учётной записью,
после чего вас вернёт в веб-консоль вашего облака.

Не выходите из веб-консоли Yandex Cloud и приступите к следующему пункту инструкции.

### Настройка профиля yc

Для работы с облаком настройте утилиту `yc`, рекомендуется создать профиль.
Настройте профиль по [инструкции](https://cloud.yandex.ru/docs/cli/operations/profile/profile-create#interactive-create),
помните, что вы работаете от имени федеративного пользователя. Идентификатор федерации — `bpffbnnnuauomglir5k7`

Перейдите в консоль, и, используя идентификатор, федерации приступите к созданию нового профиля:

    yc init --federation-id=<ID федерации>

## Подключение к чату практикума

Вся совместная работа будет проходить в чате комьюнити [Yandex Serverless Ecosystem](https://t.me/YandexCloudFunctions),
для этого практикума в телеграм создан отдельный топик, [подключитесь к нему](https://t.me/YandexCloudFunctions/21064).

По завершению настройки, у вас будет открыто облако, создан профайл, и вам будет доступна инструкция.
