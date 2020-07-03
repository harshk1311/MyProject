from datetime import date, datetime
import hashlib
from passlib.hash import bcrypt
import random

def getTimeStamp():
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    return int(timestamp)

def getTodayDate():
    return date.today()

def getCurrentDateTime():
    now = datetime.now()
    return (now.strftime("%Y-%m-%d %H:%M:%S"))

def getMD5Hash(data):
    data = bytes(data, 'utf-8')
    hash_obj = hashlib.md5(data)
    return hash_obj.hexdigest()

def getHashedPassword(password):
    return bcrypt.hash(password)

def encodeID(id):
    id = str(id)
    str_sequence = '0123456789abcdef'
    n = random.randint(2,9)
    token = getMD5Hash(id+str(getTimeStamp()))+id+("".join(random.sample(str_sequence, n)))
    token = token[:1]+str(n)+token[2:]
    return token
    
def decodeID(token):
    inx = int(token[1])
    token = token[32:]
    token = token[:-inx]
    return token
    
