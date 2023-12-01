from jwt import encode, decode 
pwd = '1234567890'

def create_token(data, secret=pwd):
    return encode(payload=data, key=secret, algorithm='HS256')

def validate_token(token):
    return decode(token, pwd, algorithms=['HS256'])