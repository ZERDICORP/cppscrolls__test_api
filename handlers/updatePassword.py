from config import *
from tools.tools import *

@app.route(f"{API_PREFIX}/user/password", methods = ["PUT"]) 
def updatePassword(): 
	authResult = auth(); 
	if authResult["status"] != STATUS.OK: 
		return authResult; 

	req = request.json; 

	if not req["new_password"] or len(req["new_password"]) < 6:
		return { "status": STATUS.INVALID_PASSWORD };

	if hashing(req["password"]) != authResult["user"]["password_hash"]: 
		return { "status": STATUS.ACCESS_DENIED };

	# UPDATE PASSWORD #
	db["users"][authResult["index"]]["password_hash"] = hashing(req["new_password"]); 

	return { "status": STATUS.OK };
