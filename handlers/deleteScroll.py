from config import *
from tools.tools import *

@app.route(f"{API_PREFIX}/scroll", methods = ["DELETE"]) 
def deleteScroll(): 
	authResult = auth(); 
	if authResult["status"] != STATUS.OK: 
		return authResult; 

	req = request.json; 

	indexes = [index for index, scroll in enumerate(db["scrolls"]) if scroll["id"] == req["scroll_id"]]; 
	if len(indexes) == 0: 
		return { "status": STATUS.SCROLL_DOES_NOT_EXIST }; 
    
	del db["scrolls"][indexes[0]];

	return { "status": STATUS.OK };
