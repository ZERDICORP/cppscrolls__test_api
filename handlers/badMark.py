from config import *
from tools.tools import *

@app.route(f"{API_PREFIX}/bad_mark", methods = ["POST"])
def badMark():
	authResult = auth();
	if authResult["status"] != STATUS.OK:
		return authResult;

	req = request.json;	

	if req == None or len(set(req.keys()) & set(["scroll_id"])) != 1:
		return { "status": STATUS.INVALID_REQUEST };
	
	unique_visits = [visit for visit in db["unique_scroll_visits"] if visit["scroll_id"] == req["scroll_id"] and visit["user_id"] == authResult["user"]["id"]];
	if len(unique_visits) == 0:
		return { "status": STATUS.YOU_HAVE_NOT_VISITED_THIS_SCROLL };

	unique_visits[0]["bad_mark"] = not unique_visits[0]["bad_mark"];

	return { "status": STATUS.OK };
