from config import *
from tools.tools import *

@app.route(f"{API_PREFIX}/topics/<side>/<page>", methods = ["GET"])
def getTopics(side, page):
	authResult = auth();
	if authResult["status"] != STATUS.OK:
		return authResult;

	pageStart = CONST.TOPICS_PAGE_SIZE * int(page);

	topics = [topic for topic in db["topics"] if topic["side"] == bool(int(side))];
	topics.sort(key = lambda x: x["requests"], reverse = True);

	return {
		"status": STATUS.OK,
		"topics":  [topic["name"] for topic in topics[pageStart:pageStart + CONST.TOPICS_PAGE_SIZE]]
	};
