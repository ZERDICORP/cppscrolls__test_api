from config import *
from tools.tools import *

@app.route(f"{API_PREFIX}/scrolls/<side>/<topic>/<page>", methods = ["GET"])
def getScrolls(side, topic, page):
	authResult = auth();
	if authResult["status"] != STATUS.OK:
		return authResult;



	# FIND TOPIC & INCREASE REQS COUNTER #
	matchedTopics = [tpc for tpc in db["topics"] if tpc["name"] == topic];
	if len(matchedTopics) == 0 or matchedTopics[0]["side"] != int(side):
		return { "status": STATUS.TOPIC_DOES_NOT_EXIST };

	matchedTopics[0]["requests"] += 1;



	pageStart = CONST.SCROLLS_PAGE_SIZE * int(page);

	allScrolls = [scroll for scroll in db["scrolls"] if scroll["side"] == int(side) and topic.lower() in scroll["topics"]];
	
	scrolls = [];
	for scroll in allScrolls[pageStart:pageStart + CONST.SCROLLS_PAGE_SIZE]:
		unique_visits = [visit for visit in db["unique_scroll_visits"] if visit["scroll_id"] == scroll["id"]];
		views = len(unique_visits);

		# DETERMINE REPUTATION #
		badMarks = sum([1 for visit in unique_visits if visit["bad_mark"]]);
		badMarksCoeff = 0 if not views else badMarks / (views / 100);

		res = {
			"id": scroll["id"],
			"title": scroll["title"],
			"description": scroll["description"][:30],
			"bad_marks": badMarks,
			"views": views,
			"bad_reputation": badMarksCoeff > 50,
			"successful_attempts": scroll["successful_attempts"],
			"unsuccessful_attempts": scroll["unsuccessful_attempts"]
		};

		getAuthorRes = getUserById(scroll["author_id"]);
		if getAuthorRes["status"] == STATUS.OK:
			res["author_image"] = getAuthorRes["user"]["image"];

		scrolls.append(res);

	scrolls.sort(key = lambda x: x["successful_attempts"] + x["unsuccessful_attempts"], reverse = True);	
	scrolls.sort(key = lambda x: x["bad_reputation"]);

	return {
		"status": STATUS.OK,
		"scrolls": scrolls
	};
