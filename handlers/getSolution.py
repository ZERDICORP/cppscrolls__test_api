from config import *
from tools.tools import *

@app.route(f"{API_PREFIX}/solution/<sid>", methods = ["GET"])
def getSolution(sid):
	authResult = auth();
	if authResult["status"] != STATUS.OK:
		return authResult;

	solutions = [solution for solution in db["solutions"] if solution["id"] == sid];	
	if len(solutions) == 0:
		return { "status": STATUS.SOLUTION_DOES_NOT_EXIST };
	solution = solutions[0].copy();

	res = getUserById(solution["author_id"]); 
	if res["status"] == STATUS.OK:
		solution["author"] = {
				"id": res["user"]["id"],
				"image": res["user"]["image"]
		}; 

	del solution["author_id"];	

	return {
		"status": STATUS.OK,
		"solution": {
			"author": solution["author"],
			"time": solution["time"],
			"script": solution["script"]
		}
	};
