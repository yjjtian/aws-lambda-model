import json
import sklearn
import pickle
import boto3
import os

s3 = boto3.resource('s3')
# example code to load a model
print('loading model...')
model = pickle.loads(s3.Bucket(os.getenv('s3Bucket')).Object(os.getenv('modelToLoad')).get()['Body'].read())

def get_prediction():
    # example code to run the model
    print('getting prediction...')
    result = model.predict([[5.9,3.0,5.1,1.8]])[0]
    print(result)
    return result

def lambda_handler(event, context):
    return {
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'statusCode': 200,
        'body': json.dumps({
            'output': f'{get_prediction()}',
            'parameters': event['queryStringParameters']
        }),
    }
