from run import process_message


def lambda_handler(event, context):
    for record in event['Records']:
        process_message(record['body'])
    return {"statusCode": 200}