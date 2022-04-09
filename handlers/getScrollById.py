from config import *
from tools.tools import *

@app.route(f"{API_PREFIX}/scroll/<sid>", methods = ["GET"]) 
def getScroll(sid): 
	authResult = auth(); 
	if authResult["status"] != STATUS.OK: 
		return authResult; 



	# FIND SCROLL #
	scrolls = [scroll for scroll in db["scrolls"] if scroll["id"] == sid]; 
	if len(scrolls) == 0: 
		return { "status": STATUS.SCROLL_DOES_NOT_EXIST }; 
	scroll = scrolls[0].copy();  



	# ADD A VISIT #
	unique_visits = [visit for visit in db["unique_scroll_visits"] if visit["scroll_id"] == scroll["id"]];
	scroll["views"] = len(unique_visits);

	userVisits = sum([1 for visit in unique_visits if visit["user_id"] == authResult["user"]["id"]]);
	if userVisits == 0:
		visit = {
			"scroll_id": scroll["id"],
			"user_id": authResult["user"]["id"],
			"bad_mark": False
		};

		db["unique_scroll_visits"].append(visit);
		unique_visits.append(visit);
	
		scroll["views"] += 1;



	# FIND SCROLL AUTHOR #
	scroll_author = getUserById(scroll["author_id"]);
	if scroll_author["status"] == STATUS.OK:
		scroll["author"] = {"id": scroll_author["user"]["id"], "image": scroll_author["user"]["image"]};



	# DETERMINE REPUTATION #
	badMarks = sum([1 for visit in unique_visits if visit["bad_mark"]]);
	badMarksCoeff = badMarks / (scroll["views"] / 100);
	scroll["bad_reputation"] = badMarksCoeff > 50;
	scroll["bad_mark"] = len([1 for visit in unique_visits if visit["user_id"] == authResult["user"]["id"] and visit["bad_mark"]]) > 0;
	scroll["bad_marks"] = badMarks;


	# GET TAGS #
	topics = scroll["topics"];



	# REMOVE EXTRA FIELDS #
	del scroll["topics"];
	del scroll["test_func"];
	del scroll["author_id"];



	# FIND SOLUTION #
	solutions = [solution for solution in db["solutions"] if solution["scroll_id"] == scroll["id"]];
	solution = None;
	solution_author = None;
	if len(solutions) == 1:
		solution = solutions[0].copy();



		# FIND SOLUTION AUTHOR #
		solution_author = getUserById(solution["author_id"]);
		if solution_author["status"] == STATUS.OK:
			solution["author_image"] = solution_author["user"]["image"];



	# REMOVE EXTRA FIELD #
	del scroll["id"];



	# CREATE RESPONSE #
	res = {
		"status": STATUS.OK,
		"topics": topics,
		"scroll": scroll
	};
	


	# SET SOLUTION IF IT IS #
	if solution:
		res["solution"] = {
			"id": solution["id"],
			"author_image": solution["author_image"]
		};



	return res;
