from config import *
from tools.tools import *

@app.route(f"{API_PREFIX}/user/<uid>", methods = ["GET"]) 
def getUser(uid): 
	authResult = auth(); 
	if authResult["status"] != STATUS.OK: 
		return authResult; 

	if not isValidId(uid): 
		return { "status": STATUS.INVALID_ID }; 

	result = getUserById(uid); 
	if result["status"] != STATUS.OK: 
		return result; 

	user = result["user"]; 

	return { 
		"status": STATUS.OK, 
		"user": { 
			"nickname": user["nickname"], 
			"image": user["image"], 
			"score": user["score"], 
			"side": user["side"],
			"bio": user["bio"]
		} 
	};
