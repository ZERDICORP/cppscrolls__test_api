from config import *
from tools.tools import *

@app.route(f"{API_PREFIX}/scroll", methods = ["POST"]) 
def createScroll(): 
	authResult = auth(); 
	if authResult["status"] != STATUS.OK: 
		return authResult; 

	# ADD SCORE #
	db["users"][authResult["index"]]["score"] += 1;

	req = request.json; 

	newScroll = { 
		"id": genId(), 
		"author_id": authResult["user"]["id"], 
		"title": req["title"], 
		"description": req["description"], 
		"script_func": req["script_func"], 
		"test_func": req["test_func"],
		"side": authResult["user"]["side"],
		"successful_attempts": 0,
    "unsuccessful_attempts": 0,
		"topics": req["topics"]
	}; 

	db["scrolls"].append(newScroll); 



	# ADD NON-EXISTING TOPICS || INCREASE REQS COUNTER #
	for topicName in req["topics"]:
		matchedTopics = [topic for topic in db["topics"] if topic["side"] == authResult["user"]["side"] and topic["name"] == topicName];
		if len(matchedTopics) == 0:
			db["topics"].append({
				"name": topicName,
				"requests": 1,
				"side": authResult["user"]["side"]
			});
		else:
			matchedTopics[0]["requests"] += 1;



	return { 
		"status": STATUS.OK, 
		"scroll_id": newScroll["id"] 
	};
