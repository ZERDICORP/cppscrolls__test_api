from config import *
from tools.tools import *

@app.route(f"{API_PREFIX}/user/nickname", methods = ["PUT"]) 
def updateNickname(): 
	authResult = auth(); 
	if authResult["status"] != STATUS.OK: 
		return authResult; 

	req = request.json; 

	if not req["nickname"]:
		return { "status": STATUS.INVALID_NICKNAME };

	if len([True for user in db["users"] if user["nickname"] == req["nickname"]]) > 0:
		return { "status": STATUS.NICKNAME_ALREADY_IN_USE };

	# UPDATE NICKNAME #
	db["users"][authResult["index"]]["nickname"] = req["nickname"];

	return { "status": STATUS.OK };
