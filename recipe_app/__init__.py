# __init__.py
from flask import Flask, session
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "recipeproject"

bcrypt = Bcrypt(app)