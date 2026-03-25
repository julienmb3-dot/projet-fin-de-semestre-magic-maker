from flask import Flask, render_template, url_for, request, session, redirect

from pymongo import MongoClient

from dotenv import load_dotenv

from werkzeug.utils import secure_filename

from bson.objectid import ObjectId

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
                    session["role"] = user["role"]
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


@app.route("/game")
def game():
    return render_template("game.html", game="game")

"""
@app.route("/update_game", methods=["POST"])
def update_game():
    score = request.form["score"]
    time = request.form["time"]
    image = request.files()

    if image:
        nom_fichier = secure_filename()
        upload_path = os.path.join(app.static_folder, "images/game_user", nom_fichier)
        image.save(upload_path)

        image_path = f"/static/images/game_user"
        
    else:
        image_path = ""
    
    data = {
        "score" = score
        "time" = time
        "image" = image
    }
    db["games_data"].insert_one(data)
    return redirect(url_for("play"))
"""

@app.route("/admin")
def admin():
    if "user" in session and session["role"] == "admin":
        users_find = list(db["Users"].find())
        return render_template("back/welcome.html", admin = "oui", users=users_find)
    else:
        data_find = list(db["data"].find())
        return render_template("index.html", erreur = "tu n'est pas administrateur !", data=data_find)

@app.route("/admin/search", methods = ["GET"])
def admin_search():
    query = request.args.get("q", "").strip()

    if query == "":
        users_find = list(db["Users"].find())
        return render_template("back/welcome.html", admin = "oui", users=users_find)
    else:
        results = list(db["Users"].find({
            "$or" : [
                {"user_id" : {"$regex" : query, "$options" : "i"}},
                {"role" : {"$regex" : query, "$options" : "i"}}
            ]
        }))
        print(results[0]["user_id"])
    return render_template("back/welcome.html", admin = "oui", users=results, query=query)

@app.route("/admin/update_role/<_id>", methods=["Post"])
def update_role(_id):
    if "user" in session and session["role"] == "admin":
        new_role = request.form.get("role")

        db["Users"].update_one(
            {"_id" : ObjectId(_id)},
            {"$set" : {"role" : new_role}}
        )
    
    return redirect(url_for("admin"))

@app.route("/admin/delete_user/<_id>")
def delete_user(_id):
    if "user" in session and session["role"] == "admin":
        db["Users"].delete_one({"_id" : ObjectId(_id)})
        db["data"].delete_one({"_id" : ObjectId(_id)})

    return redirect(url_for("admin"))

@app.route('/admin/user/<_id>')
def show_user(_id):
    if "user" in session and session["role"] == "admin":
        user = db["Users"].find_one({"_id" : ObjectId(_id)})

        if not user:
            return redirect(url_for('admin'))
            
        return render_template('user_profile.html', user=user, admin = "oui", data=db["data"].find_one({"_id" : ObjectId(_id)}))
    return redirect(url_for("admin"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

app.run(host="0.0.0.0", port=81)