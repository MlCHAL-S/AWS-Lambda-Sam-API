import bson
import json
from bson import ObjectId
from .utils import db


def retrieve_info(object_id):
    result = list()
    mongo = db.MongoDBConnection()
    with mongo:
        database = mongo.connection['myDB']
        collection = database['registrations']
        if object_id is not None:
            try:
                single_object = collection.find_one({'_id': ObjectId(object_id)})
                if single_object is None:
                    return {'message': 'ID does not exist'}
            except bson.errors.InvalidId:
                return {'message': 'Please enter a valid ID'}

            return {
                'id': object_id,
                'first_name': single_object['first_name'],
                'last_name': single_object['last_name'],
                'email': single_object['email']
            }
        else:
            for data in collection.find():
                result.append({
                    'id': str(data['_id']),
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'email': data['email']
                })
        return result


def lambda_handler(event, context):
    try:
        object_id = event['pathParameters']['Id']
    except TypeError:
        object_id = None
    except KeyError:
        object_id = None

    try:
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Success!',
                                'data': retrieve_info(object_id)})
        }
    except Exception as err:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Error!',
                                'data': str(err)})
        }
