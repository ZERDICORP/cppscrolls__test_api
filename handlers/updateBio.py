from config import *
from tools.tools import *
  
@app.route(f"{API_PREFIX}/user/bio", methods = ["PUT"]) 
def updateBio(): 
  authResult = auth(); 
  if authResult["status"] != STATUS.OK: 
    return authResult; 
  
  req = request.json; 
 
  # UPDATE BIO #
  db["users"][authResult["index"]]["bio"] = req["bio"];
 
  return { "status": STATUS.OK };
