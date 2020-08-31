import jwt, random, time
from Util import randHex

class Jwt:
    @staticmethod
    def standard(secretKey):
        payload = { 'jti': randHex(10), 
                'iat': str(time.time()*1000), 
                "exp": str((time.time() + 259200) * 1000)
        }
        encoded = jwt.encode(payload, secretKey)
        return encoded
    
    @staticmethod
    def addDate(secretKey):
        payload = { 'jti': randHex(10), 
                'iat': str(time.time()*1000), 
                "exp": str((time.time() + 259200) * 1000),
                'orderTime': str(time.time()*1000)
        }
        encoded = jwt.encode(payload, secretKey)
        return encoded
