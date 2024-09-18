from marshmallow import Schema, fields, post_load, ValidationError
from argon2 import PasswordHasher
from . import db

def encrypt_password(plain_text):
    """ This function will encrypt the password using argon2."""
    return PasswordHasher().hash(plain_text)


class UserRegistrationSchema(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)

    @post_load
    def decrypt_password(self, data, **kwargs):
        data['password'] = encrypt_password(data['password'])
        return data

    @post_load
    def validate_email(self, data, **kwargs):
        mongo = db.MongoDBConnection()
        with mongo:
            database = mongo.connection['myDB']
            collection = database['registrations']

            # check if email already exists

            if collection.find_one({'email': data['email']}) is not None:
                raise ValidationError('Email already exists')
        return data
