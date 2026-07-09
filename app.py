import json
from pathlib import Path
from datetime import datetime

from flask import Flask, render_template, request, redirect, send_from_directory

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
STORAGE = BASE_DIR / "storage"
DATA_FILE = STORAGE / "data.json"

STORAGE.mkdir(exist_ok=True)

if not DATA_FILE.exists():
    DATA_FILE.write_text("{}", encoding="utf-8")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/message")
def message():
    return render_template("message.html")


@app.route("/message", methods=["POST"])
def message_post():
    username = request.form.get("username")
    message = request.form.get("message")

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    data[str(datetime.now())] = {
        "username": username,
        "message": message,
    }

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    return redirect("/")


@app.route("/read")
def read():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return render_template("read.html", data=data)


@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)