from waitress import serve
import sys

from cork.users import *
from cork.scrolls import *
from cork.solutions import *
from cork.topics import *
from cork.unique_scroll_visits import *

from handlers.signup import *
from handlers.confirm import *
from handlers.signin import *
from handlers.rating import *
from handlers.getUserById import *
from handlers.getRandomScroll import *
from handlers.getScrollById import *
from handlers.tryingToSolve import *
from handlers.getSolution import *
from handlers.badMark import *
from handlers.getScrolls import *
from handlers.getUserScrolls import *
from handlers.getHistory import *
from handlers.createScroll import *
from handlers.updateScroll import *
from handlers.deleteScroll import *
from handlers.updateProfileImage import *
from handlers.updateNickname import *
from handlers.updateBio import *
from handlers.updatePassword import *
from handlers.deleteAccount import *
from handlers.getTopics import *
from handlers.getTopicsByPattern import *



db["users"] = users;
db["scrolls"] = scrolls;
db["solutions"] = solutions;
db["topics"] = topics;
db["unique_scroll_visits"] = unique_scroll_visits;



@app.route("/images/<image_name>", methods = ["GET"]) 
def image(image_name): 
    path = f"{os.getcwd()}{request.path}"; 
    if not os.path.isfile(path): 
            abort(404); 
    return send_file(path, mimetype = "image/png");

@app.before_request 
def api_auth_middleware(): 
    if not re.match("\/images\/[a-zA-Z.]*", request.path) and request.headers.get("API-Secret") != API_SECRET: 
            return { "status": STATUS.ACCESS_DENIED };

if len(sys.argv) > 1:
    if sys.argv[1].isdigit():
        PORT = int(sys.argv[1]);

if __name__ == "__main__":
	print(f"Server has been started on port {PORT}..");
	serve(app, host = IP, port = PORT);
