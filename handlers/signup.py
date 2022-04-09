from config import *
from tools.tools import *

@app.route(f"{API_PREFIX}/signup", methods = ["POST"])
def signup():
	req = request.json;

	if req == None or len(set(req.keys()) & set(["email", "nickname", "password", "side"])) != 4:
		return { "status": STATUS.INVALID_REQUEST };

	if not re.match("[^@]+@[^@]+\.[^@]+", req["email"]):
		return { "status": STATUS.INVALID_EMAIL };

	if not re.match("^[A-Za-z0-9_-]*$", req["nickname"]):
		return { "status": STATUS.INVALID_NICKNAME };

	if len(req["password"]) < CONST.MIN_PASSWORD_LENGTH:
		return { "status": STATUS.TOO_SHORT_PASSWORD };

	if req["side"] not in [CONST.DEVILS_SIDE, CONST.GODS_SIDE]:
		return { "status": STATUS.INVALID_SIDE };

	if len([True for value in [req["email"], req["nickname"], req["password"]] if not value]) > 0:
		return { "status": STATUS.EMPTY_DATA };

	if len([True for user in db["users"] if user["email"] == req["email"]]) > 0:
		return { "status": STATUS.USER_ALREADY_EXIST };

	if len([True for user in db["users"] if user["nickname"] == req["nickname"]]) > 0:
		return { "status": STATUS.NICKNAME_ALREADY_IN_USE };

	uid = genId();

	db["users"].append({
		"id": uid, 
    "email": req["email"], 
    "password_hash": hashing(req["password"]), 
    "nickname": req["nickname"], 
    "image": "/images/default.png", 
    "score": 0, 
    "side": req["side"],  
    "confirmed": 0,  
    "bio": ""
	});

	token = Token.build(json.dumps({"uid": uid}), SECRET);

	mail.to(req["email"]);
	mail.send("CPP Scrolls", f"{HOST}/account_confirmation/{token}");

	return { "status": STATUS.OK };
