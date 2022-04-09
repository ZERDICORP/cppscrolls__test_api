from config import *
from tools.tools import *

@app.route(f"{API_PREFIX}/user/image", methods = ["PUT"]) 
def updateProfileImage(): 
	authResult = auth();
	if authResult["status"] != STATUS.OK: 
		return authResult; 

	image_data = request.get_data(); 

	if authResult["user"]["image"] == "/images/default.png": 
		authResult["user"]["image"] = f"/images/{time.time()}.png"; 

		db["users"][authResult["index"]]["image"] = authResult["user"]["image"];

	with open("." + authResult["user"]["image"], "wb") as f: 
		f.write(image_data); 

	return { "status": STATUS.OK };
