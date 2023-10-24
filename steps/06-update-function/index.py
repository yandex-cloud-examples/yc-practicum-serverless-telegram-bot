import os
import requests
import json

import ydb
import ydb.iam
import random

# Telegram Bot Token
token = os.getenv('TELEGRAM_BOT_TOKEN')

# Create driver in global space.
driver = ydb.Driver(
    endpoint=os.getenv('YDB_ENDPOINT'),
    database=os.getenv('YDB_DATABASE'),
    credentials=ydb.iam.MetadataUrlCredentials(),
)

# Wait for the driver to become active for requests.
driver.wait(fail_fast=True, timeout=5)

# Create the session pool instance to manage YDB sessions.
pool = ydb.SessionPool(driver)

# The first problem ...
quote_counter = 1


# The Second problem ...
def find_max_counter(session):
    # Create the transaction and execute query.
    result = session.transaction().execute(
        'SELECT COUNT(*) FROM Quotes;',
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
    )
    return result[0].rows[0].column0


# The third problem
def get_one_quote(session):
    yql = """
    UPDATE Quotes 
    SET counter = counter + 1 
    WHERE id = %i;  
    
    SELECT * FROM Quotes WHERE id = %i;
    """ % (quote_counter, quote_counter)

    # Create the transaction and execute query.
    result = session.transaction().execute(
        yql,
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
    )

    quote = "%s %s" % (result[0].rows[0].quote, result[0].rows[0].author)

    return quote


# send message function
def send_message(chat_id, text):
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
        print(chat_id)
        print(text_from_user)

        # Execute query with the retry_operation helper.
        max_counter = pool.retry_operation_sync(find_max_counter)
        global quote_counter
        quote_counter = random.randint(1, max_counter)

        text_for_message = "%s %s" % ("Очередная цитата: ", str(pool.retry_operation_sync(get_one_quote)))

        send_message(chat_id, text_for_message)
        r = {'statusCode': 200, 'body': 'Message sent'}

    except Exception as e:
        r = {'statusCode': 404, 'body': 'Same error'}

    return r
