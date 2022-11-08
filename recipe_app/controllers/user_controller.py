from flask import render_template, request, redirect, session
from recipe_app import app
from recipe_app.models.user import User, bcrypt
from recipe_app.models.recipe import Recipe

@app.route("/")
def index():
    # call the get all classmethod to get all
    # users = User.get_all()
    return render_template("main.html")

@app.route("/recipes")
def user_form():
    if not 'uid' in session:
        return redirect('/')

    data = Recipe.get_recipes()

    return render_template("dashboard.html", data=data)

@app.route("/create_user", methods=['POST'])
def create():

    print(request.form)

    if not User.validate_inputs(request.form):
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)

    data = {
        **request.form,
        "password" : pw_hash
    }

    session['uid'] = User.make_user(data)
    session['name'] = request.form('first_name')

    return redirect('/recipes')

@app.route('/login', methods=['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/')
    
    found_user = User.get_by_email(request.form)

    session['uid'] = found_user.id
    session['name'] = found_user.first_name

    return redirect('/recipes')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
