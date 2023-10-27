import jwt
import datetime
from flask import jsonify
def encodeToken(username,secretkey):
    if username != '':
        token = jwt.encode({
            'user' : username,
            'exp'  : datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
        },
        secretkey)
        return jsonify({'jwt' : token})
    else:
        return jsonify({'message':'Invalid Token'}),403

def decrypt(token,secretkey):
    jwt.decode(token,secretkey)