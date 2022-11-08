from recipe_app.config.mysqlconnection import connectToMySQL
from flask import flash
from recipe_app import bcrypt
from recipe_app import app
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM user WHERE user.email = %(email)s;"

        results = connectToMySQL('recipes_db').query_db(query, data)
        
        if not results or len(results)<1:
            return False

        else:
            return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM user WHERE user.id = %(id)s;"

        results = connectToMySQL('recipes_db').query_db(query, data)
        
        if not results or len(results)<1:
            return False

        else:
            return cls(results[0])

    @classmethod
    def make_user(cls, data):
        query = "INSERT INTO user ( first_name , last_name , email, password, created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s, NOW() , NOW() );"

        return connectToMySQL('recipes_db').query_db( query, data )

    @staticmethod
    def validate_inputs(user):
        is_valid = True # we assume this is true
        if len(user['first_name']) < 2:
            flash("First Name must be at least 2 characters.")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last Name must be at least 2 characters.")
            is_valid = False
        if not User.get_by_email(user['email']):
            flash("Email already in use")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address")
            is_valid = False

        print(user['password'])
        print(user['pass_con'])
        if user['password'] != user['pass_con']:
            flash("Passwords do not match")
            is_valid = False

        return is_valid

    @staticmethod
    def validate_login(user):
        is_valid = True
        
        found_user = User.get_by_email(user)

        if found_user:
            if not bcrypt.check_password_hash(found_user.password, user['password']):
                flash("Incorrect Login")
                is_valid = False
        
        else:
            flash('Incorrect Login')
            is_valid = False

        return is_valid