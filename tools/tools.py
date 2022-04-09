import base64, json, hashlib, uuid
from easydict import EasyDict as edict
from flask import request
from hashlib import sha256
import constants.status as STATUS
from config import *

def isValidId(value):
    try:
        uuid.UUID(value);
        return True;
    except ValueError:
        return False;

def genId():
    return str(uuid.uuid1());

def getUserById(user_id):
    users = [(index, user) for index, user in enumerate(db["users"]) if user["id"] == user_id];
    if len(users) == 0:
        return { "status": STATUS.USER_DOES_NOT_EXIST };

    index, user = users[0];

    return {
        "status": STATUS.OK,
        "index": index,
        "user": user
    };

def auth():
    token = request.headers.get("Authentication-Token");
    payload = Token.access(token, SECRET);
    if not payload:
        return { "status": STATUS.INVALID_TOKEN };
    return getUserById(payload.uid);

def hashing(data):
    return sha256(data.encode()).hexdigest();

class Token:
    def build(payload, secret):
        signature = hashlib.sha256((payload + secret).encode()).hexdigest();
        payload = base64.b64encode(payload.encode()).decode("utf-8");

        return f"{payload}.{signature}";

    def access(token, secret):
        if not token:
            return False;
        
        if len(token.split(".")) != 2:
            return False;

        payload, signature = token.split(".");
        payload = base64.b64decode(payload.encode()).decode("utf-8");

        if signature != hashlib.sha256((payload + secret).encode()).hexdigest():
            return False;
        return edict(json.loads(payload));
