from config import *
from tools.tools import *

@app.route(f"{API_PREFIX}/user/<user_id>/scrolls/<page>", methods = ["GET"])
def getUserScrolls(user_id, page):
	authResult = auth();
	if authResult["status"] != STATUS.OK:
		return authResult;

	pageStart = CONST.SCROLLS_PAGE_SIZE * int(page);

	allScrolls = [scroll for scroll in db["scrolls"] if scroll["author_id"] == user_id];
	
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

	return {
		"status": STATUS.OK,
		"scrolls": scrolls
	};
