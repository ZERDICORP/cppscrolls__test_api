from config import *
from tools.tools import *

@app.route(f"{API_PREFIX}/solve", methods = ["POST"])
def tryingToSolve():
	authResult = auth();
	if authResult["status"] != STATUS.OK:
		return authResult;

	req = request.json;
	
	# IF THERE IS NO SOLUTION - ERROR "
	error = not req["script"];

	if error:
		return {
			"status": STATUS.OK,
			"error": error,
			"output": "Test failed.. [5]"
		};

	time = random.uniform(0.5, 5.5);
	best_solution = False;

	solutions = [{ "index": index, "solution": solution } for index, solution in enumerate(db["solutions"]) if solution["scroll_id"] == req["scroll_id"]];

	if len(solutions) == 0:
		best_solution = True;
		db["solutions"].append({
			"id": genId(),
			"author_id": authResult["user"]["id"],
			"scroll_id": req["scroll_id"],
			"script": req["script"],
			"time": time
		});
	else:
		if solutions[0]["solution"]["time"] - time > 0.1:
			best_solution = True;
			db["solutions"][solutions[0]["index"]].update({
				"author_id": authResult["user"]["id"],
				"scroll_id": req["scroll_id"],
				"script": req["script"],
				"time": time
			});

	if best_solution:
		# ADD SCORE #
		db["users"][authResult["index"]]["score"] += 1;

	return {
		"status": STATUS.OK,
		"error": error,
		"output": [f"Test passed.. [{i + 1}]" + ("\n" if i < 9 else "") for i in range(10)],
		"time": time,
		"best_solution": best_solution
	};
