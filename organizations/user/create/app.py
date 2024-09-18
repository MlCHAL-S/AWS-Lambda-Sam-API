import ujson
from marshmallow import ValidationError
from .utils import db, validator


def lambda_handler(event, context):
    try:
        # parse the request body
        body = ujson.loads(event['body'])

        # validate the request body
        result = validator.UserRegistrationSchema()
        res = not bool(result.validate(body))

        if res:
            mongo = db.MongoDBConnection()
            with mongo:
                database = mongo.connection['myDB']
                collection = database['registrations']
                collection.insert_one(result.load(body))

            return {
                'statusCode': 201,
                'body': ujson.dumps({'message': 'User registered successfully',
                                     'data': result.validate(body)})
            }
        else:
            return {
                'statusCode': 400,
                'body': ujson.dumps({'message': 'Error!',
                                     'data': result.validate(body)})
            }

    except ValidationError as err:
        return {
            'statusCode': 400,
            'body': ujson.dumps({'message': 'Error!',
                                'data': err.messages})
        }
    except KeyError:
        return {
            'statusCode': 400,
            'body': ujson.dumps({'message': 'Invalid request body'})
        }