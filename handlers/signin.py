from config import *
from tools.tools import *

@app.route(f"{API_PREFIX}/signin", methods = ["POST"])
def signin():
    req = request.json;

    if req == None or len(set(req.keys()) & set(["login", "password"])) != 2:
            return { "status": STATUS.INVALID_REQUEST };

    if len([True for value in [req["login"], req["password"]] if not value]) > 0:
            return { "status": STATUS.EMPTY_DATA };

    candidates = [user for user in db["users"] if req["login"] in [user["email"], user["nickname"]]];
    if len(candidates) == 0:
            return { "status": STATUS.USER_DOES_NOT_EXIST };

    if candidates[0]["password_hash"] != hashing(req["password"]):
            return { "status": STATUS.ACCESS_DENIED };

    return {
            "status": STATUS.OK,
            "uid": candidates[0]["id"],
            "token": Token.build(json.dumps({
                    "uid": candidates[0]["id"],
            }), SECRET)
    };
