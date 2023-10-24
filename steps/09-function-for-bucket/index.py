import os
import requests
import json
import boto3

import ydb
import ydb.iam

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
BUCKET_NAME = os.getenv('BUCKET_NAME')

TEMP_FILENAME = "/tmp/temp_file"


def write_temp_file(full_quote):
    temp_file = open(TEMP_FILENAME, 'w')
    temp_file.write(full_quote)
    temp_file.close()
    print("\U0001f680 Temp file is writed")


def get_s3_instance():
    session = boto3.session.Session()
    return session.client(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net'
    )


def upload_dump_to_s3(key):
    print("\U0001F4C2 Starting upload to Object Storage")
    get_s3_instance().upload_file(
        Filename=TEMP_FILENAME,
        Bucket=BUCKET_NAME,
        Key="quote-%s.txt" % key
    )
    print("\U0001f680 Uploaded")


def remove_temp_files():
    os.remove(TEMP_FILENAME)
    print("\U0001F44D That's all!")


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
def record_ten_quote(session):
    yql = "SELECT * FROM Quotes WHERE id <= 10;"

    # Create the transaction and execute query.
    result = session.transaction().execute(
        yql,
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
    )

    for row in result[0].rows:
        print("id: ", row.id, ", quote: ", row.quote, ", author: ", row.author)
        quote = "%s %s" % (row.quote, row.author)
        write_temp_file(quote)
        upload_dump_to_s3(str(row.id))
        remove_temp_files()

    return "Ten quotes are recorded to the object storage"


def handler(event, context):
    try:
        text_for_message = str(pool.retry_operation_sync(record_ten_quote))

        r = {'statusCode': 200, 'body': text_for_message}

    except Exception as e:
        r = {'statusCode': 404, 'body': 'Same error'}

    return r
