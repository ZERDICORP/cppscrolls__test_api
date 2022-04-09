from config import *
from tools.tools import *

@app.route(f"{API_PREFIX}/user/confirm", methods = ["POST"]) 
def confirm(): 
	req = request.json; 

	if req == None or len(set(req.keys()) & set(["token"])) != 1: 
		return { "status": STATUS.INVALID_REQUEST }; 

	payload = Token.access(req["token"], SECRET); 
	if not payload: 
		return { "status": STATUS.INVALID_TOKEN }; 

	users = [[index, user] for index, user in enumerate(db["users"]) if user["id"] == payload["uid"]]; 
	if len(users) == 0:
		return { "status": STATUS.INVALID_TOKEN };

	index, user = users[0];

	if user["confirmed"]:
		return { "status": STATUS.INVALID_TOKEN };

	db["users"][index]["confirmed"] = True; 
	 
	return { 
		"status": STATUS.OK,
		"side": user["side"] 
	};
