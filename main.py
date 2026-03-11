from flask import Flask, render_template, url_for, request, session, redirect
from pymongo import MongoClient
from dotenv import load_dotenv

import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client.get_database("Main")

app = Flask("Spoon Box Rush")

app.secret_key = "lkna565s6c%!dhoahjd_d"

@app.route("/")
def index():
    data_find = list(db["data"].find())
    return render_template("index.html", data=data_find)

@app.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        db_users = db["Users"]
        if request.form["user_id"] != "":
            user = db_users.find_one({"user_id" : request.form["user_id"]})
            
            if user:
                if request.form["password"] == user["password"]:
                    session["user"] = request.form["user_id"]
                    session["role"] = "guest"
                    return redirect(url_for("index"))
                else:
                    return render_template('login.html', erreur="On dirait que t'as un 🕳️ de mémoire...")
            else:
                return render_template('login.html', erreur="Je ne te connais pas, tu devrais t'enregistrer ! 😉")
        else:
            return render_template('login.html', erreur="Si tu ne mes rien, je ne peux pas savoir qui tu es ! 😖")
    else:
        return render_template('login.html')
    
@app.route("/signup", methods = ["POST", "GET"])
def signup():
    if request.method == "POST":
        db_users = db["Users"]
        new_user = db_users.find_one({"user_id" : request.form["user_id"]})
        if new_user:
            return render_template('signup.html', erreur="Ce nom d'utilisateur est déjà pris.")
        else:
            if request.form["password"] == request.form["password_confirmation"]:
                if not(request.form["password"] == "" or request.form["user_id"] == ""):
                    db_users.insert_one({
                        "user_id" : request.form["user_id"],
                        "password" : request.form["password"],
                        "role" : "guest"
                    })
                    session["user"] = request.form["user_id"]
                    
                    return redirect(url_for("index"))
                else:
                    return render_template('signup.html', erreur="Le nom d'utilisateur ou le mot de passe est vide.")
            else:
                return render_template('signup.html', erreur="Les deux mots de passe ne correspondent pas.")
    else:
        return render_template("signup.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

app.run(host="0.0.0.0", port=81)