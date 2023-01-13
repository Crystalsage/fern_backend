import string
import random
import hashlib

import jwt

from django.conf import settings

import datetime

def generate_jwt(partner_id):
     access_token_payload = {
            'partner_id': partner_id,
            'user_role': 'partner',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=5),
            'iat': datetime.datetime.utcnow(),
        }
     access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm='HS256')
     return access_token

def verify_jwt(encoded_jwt):
    decoded_token = jwt.decode(encoded_jwt, settings.SECRET_KEY, algorithms=["HS256"])
    if decoded_token['user_role'] == 'partner':
        return True, decoded_token['partner_id']
    return False, -1

def jwt_get_partner_id(encoded_jwt):
    decoded_token = jwt.decode(encoded_jwt, settings.SECRET_KEY, algorithms=["HS256"], options={"verify_signature": False})
    return decoded_token['partner_id']

def generate_partner_id():
    partner_id = ""

    partner_id += str(random.randint(100000,999999))
    partner_id += str(random.choice(string.ascii_letters))

    return partner_id

def generate_md5_hash(password):
    return hashlib.md5(password.encode('utf-8')).hexdigest()
