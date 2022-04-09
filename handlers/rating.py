from config import *
from tools.tools import *

@app.route(f"{API_PREFIX}/rating", methods = ["GET"])
def rating():
    authResult = auth();
    if authResult["status"] != STATUS.OK:
            return authResult;

    bright_side_score = sum([user["score"] for user in db["users"] if user["side"] == False]);
    dark_side_score = sum([user["score"] for user in db["users"] if user["side"] == True]);

    dark_users = [user for user in db["users"] if user["side"] == False];
    bright_users = [user for user in db["users"] if user["side"] == True];

    best_dark_users = sorted(dark_users, key = lambda user: user["score"], reverse = True);
    best_bright_users = sorted(bright_users, key = lambda user: user["score"], reverse = True);

    return {
        "status": STATUS.OK,
        "bright_side": {
            "score": bright_side_score,
            "best_user": {
                "id": best_bright_users[0]["id"],
                "image": best_bright_users[0]["image"]
            }
        },
        "dark_side": {
            "score": dark_side_score,
            "best_user": {
                "id": best_dark_users[0]["id"],
                "image": best_dark_users[0]["image"]
            }
        }
    };
