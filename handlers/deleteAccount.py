from config import *
from tools.tools import *

@app.route(f"{API_PREFIX}/user", methods = ["DELETE"]) 
def deleteAccount(): 
	authResult = auth(); 
	if authResult["status"] != STATUS.OK: 
		return authResult; 
	
	req = request.json; 
	
	if hashing(req["password"]) != authResult["user"]["password_hash"]: 
		return { "status": STATUS.ACCESS_DENIED };

	del db["users"][authResult["index"]];

	return { "status": STATUS.OK };
