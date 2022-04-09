from config import *
from tools.tools import *

@app.route(f"{API_PREFIX}/<side>/scroll", methods = ["GET"])
def getRandomScroll(side):
	authResult = auth();
	if authResult["status"] != STATUS.OK:
		return authResult;

	randomScrollId = random.choice([scroll["id"] for scroll in db["scrolls"] if scroll["side"] == int(side)]);

	return {
		"status": STATUS.OK,
		"scroll_id": randomScrollId
	};
