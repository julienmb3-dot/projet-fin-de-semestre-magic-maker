from flask import Flask, render_template, url_for
from pymongo import MongoClient
from dotenv import load_dotenv

import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client.get_database("Main")

app = Flask(__name__)

@app.route("/")
def index():
    data_find = list(db["data"].find())
    return render_template("index.html", data=data_find)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

app.run(host="0.0.0.0", port=81)