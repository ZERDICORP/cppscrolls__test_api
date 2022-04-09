from config import *
from tools.tools import *

@app.route(f"{API_PREFIX}/matched_topics/<pattern>/<page>", methods = ["GET"])
def getTopicsByPattern(pattern, page):
	authResult = auth();
	if authResult["status"] != STATUS.OK:
		return authResult;

	pageStart = CONST.TOPICS_PAGE_SIZE * int(page);	

	topics = [topic for topic in db["topics"] if topic["side"] == authResult["user"]["side"] and pattern in topic["name"]];

	return {
		"status": STATUS.OK,
		"topics": [topic["name"] for topic in topics[pageStart:pageStart + CONST.TOPICS_PAGE_SIZE]]
	};
