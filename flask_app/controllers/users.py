from flask_app import app
from flask import flash, redirect, render_template, request, session
from flask_app.models.user import User
from flask_app.models.tvshow import Tvshow

from flask_app import bcrypt


# @app.get("/")
@app.route("/")
def index():
    return render_template("index.html")


# @app.post("/register")
@app.route("/register", methods=["POST"])
def register_user():

    if not User.registration_is_valid(request.form):
        return redirect("/")
    
    potential_user = User.get_by_email(request.form["email"])

    if potential_user:
        flash("Email in Use. Please log In.")
        return redirect("/")
    print("User not found ok to register")
    
    hashed_pw = bcrypt.generate_password_hash(request.form["password"])
     #hash password

    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": hashed_pw,
    }

    user_id = User.create(data)

    session["user_id"] = user_id
    # flash("Thanks for registering.")
    return redirect("/dashboard")

# @app.post("/login")
@app.route("/login", methods=["POST"])
def login():
    print(request.form)
    if not User.login_is_valid(request.form):
        return redirect("/")
    # print("login is valid")
    potential_user = User.get_by_email(request.form["email"])

    if not potential_user:
        flash("Invalid Credentials.")
        return redirect("/")
    print("user exists")
    user = potential_user
    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("Invalid Credentials.")
        return redirect("/")

    session["user_id"] = user.id

    print("user stored in session")
    # flash("Thanks for logging in")
    return redirect("/dashboard")


# @app.get("/dashboard")
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/")

    results = User.get_all()
    tvshows = Tvshow.get_all()

    user = User.get_by_user_id(session["user_id"])
    return render_template("dashboard.html", userList = results, user=user, tvshows=tvshows)



# @app.get("/logout")
@app.route("/logout")
def logout(): 
    """Clear Session"""
    session.clear()
    return redirect("/")