import os
from flask import Flask, request, render_template,render_template_string, session, redirect, flash
from uuid import uuid4
from werkzeug.exceptions import RequestEntityTooLarge
from bot import visit_url

from db import get_user, verify_user, create_user, update_user

app = Flask(__name__, static_folder='static')
app.secret_key = "QqR%zWypK^Q7q#qQYwW"
app.config['UPLOAD_FOLDER'] = "static/img/"
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = False


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if session:
        if session.get("username"):
            return redirect("/", code=302)
    
    if request.method == "POST":
        if verify_user(request.form["username"], request.form["password"]):
            session["username"] = request.form["username"]
            return redirect("/profile/" + request.form['username'])
        else:
            flash('Login failed.', 'error')
            return redirect("/login", code=302)
            
    return render_template("login.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    if session:
        if session.get("username"):
            return redirect("/", code=302)
    if request.method == "POST":
        if not get_user(request.form['username']) and request.form['username'].isalnum():
            create_user(request.form['username'],request.form['password'],'','')
            session["username"] = request.form["username"]
            return redirect("/profile/" + request.form['username'])

        else:
            flash("Invalid Username", category="error")
            return redirect("/register")
    
    
    return render_template("register.html")

@app.route("/logout")
def logout ():
    session.clear()
    return redirect("/")

@app.errorhandler(RequestEntityTooLarge)
def handle_file_size_error(error):
    flash('File is too large. Maximum size is 5 MB.', 'error')
    return redirect(request.url)

@app.route("/profile/<user_id>", methods=["GET", "POST"])
def profile(user_id):
    with open("templates/profile.html", "r") as f:
        profile = "".join(f.readlines())
    
    user_info = get_user(user_id)
    
    if not user_info:
        return "User not found"
    
    if request.method == "POST":
        if not session: 
            flash("Please log as this user first.", category="error")
            return redirect("/profile/" + user_id)
        
        if user_id.lower() == "admin":
            flash("Not a good idea", category="error")
            return redirect("/profile/" + user_id)
        
        if session.get("username") != user_id:
            flash("Please log as this user first.", category="error")
            return redirect("/profile/" + user_id)
        
        file = request.files.get('profile_image')
        filename = user_info[2]

        if file:
            ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'svg'}
            filename = None
            for x in ALLOWED_EXTENSIONS:
                if file.filename.endswith(x):
                    filename = app.config['UPLOAD_FOLDER'] + str(uuid4()) + "." + x
                    file.save(filename)
                    break
            
            if not filename:
                flash("File type not allowed", category="error")
                return redirect(request.url)
            
            try:
                if "/" in user_info:
                    os.remove(user_info[2][1:])
            except:
                pass
        
        bio = request.form["bio"]

        update_user(session["username"], "/" + filename, bio)

        visit_url(session.get("username"))

        flash("User updated! An admin will review your profile shorlty...", category="success")

        return redirect(request.url)
                    
    if not user_info[2]:
        img = '/static/img/default.png'
    else:
        img = user_info[2]
    return render_template("profile.html", username=user_info[0],img=img, bio=user_info[3], posts=[])


