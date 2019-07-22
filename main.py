from flask import Flask, render_template, request, make_response, Response
import datetime
import random
import uuid         # universal unique identifier

# SECRET = random.randint(1, 10)

SECRETS_DB = {}

# print(SECRET)
app = Flask(__name__)


@app.route("/")
def index():
    some_text = "Message from the handler."
    current_year = datetime.datetime.now().year

    cities = ["Boston", "Vienna", "Paris", "Berlin"]

    return render_template("index.html",
                           some_text=some_text,
                           current_year=current_year,
                           cities=cities)


@app.route("/about-me")
def about():
    return render_template("about.html")


@app.route("/guessing-game", methods=["GET", "POST"])
def guessing_game():
    global SECRETS_DB

    user_id = request.cookies.get("user_id")

    method = request.method
    if method == "GET":
        if not user_id or user_id not in SECRETS_DB:
            user_id = str(uuid.uuid4())
            SECRETS_DB[user_id] = random.randint(1, 10)
        # definieren der variable als Klasse
        resp: Response = make_response(render_template("guessing_game.html"))
        resp.set_cookie("user_id", user_id)
        return resp
    elif method == "POST":
        number = request.form.get("number")
        user_id = request.cookies.get("user_id")
        if number and int(number) == SECRETS_DB[user_id]:
            SECRETS_DB[user_id] = random.randint(1, 10)
            text = "You won"
        else:
            text = f"Try Again {SECRETS_DB[user_id]}"
        return render_template("guessing_game.html", text=text)


if __name__ == '__main__':
    app.run()
