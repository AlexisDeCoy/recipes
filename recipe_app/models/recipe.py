from recipe_app.config.mysqlconnection import connectToMySQL
from flask import flash
from recipe_app import app
from recipe_app.models.user import User

class Recipe:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under30 = data['under30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def make_recipe(cls, data):
        query = "INSERT INTO recipe (name, description, instructions, under30, created_at, user_id) VALUES (%(name)s,%(description)s,%(instructions)s,%(under30)s,%(created_at)s, %(user_id)s)"

        return connectToMySQL('recipes_db').query_db(query, data)

    @classmethod
    def get_recipes(cls):
        query = "SELECT * FROM recipe JOIN user ON user_id = user.id;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('recipes_db').query_db(query)

        recipes = []

        if results:
            for result in results:
                recipe = cls(result)

                user_data = {
                    **result,
                    'id': result['user.id'],
                    'created_at': result['user.created_at'],
                    'updated_at': result['user.updated_at']
                }

                maker = User(user_data)
                recipe.maker = maker
                recipes.append(recipe)
        return recipes

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM recipe JOIN user ON user_id = user.id WHERE recipe.id = %(recipe_id)s;"

        results = connectToMySQL('recipes_db').query_db(query, data)
        
        recipes = []

        if results:
            for result in results:
                recipe = cls(result)

                user_data = {
                    **result,
                    'id': result['user.id'],
                    'created_at': result['user.created_at'],
                    'updated_at': result['user.updated_at']
                }

                maker = User(user_data)
                recipe.maker = maker
                recipes.append(recipe)
        return recipes[0]

    @classmethod
    def edit_recipe(cls, data):
        query = "UPDATE recipe SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, updated_at = NOW() WHERE recipe.id = %(recipe_id)s"

        connectToMySQL('recipes_db').query_db(query, data)

    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipe WHERE recipe.id = %(recipe_id)s;"

        connectToMySQL('recipes_db').query_db(query, data)

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True # we assume this is true
        if len(recipe['name']) < 1:
            flash("Name field empty")
            is_valid = False
        if len(recipe['description']) < 1:
            flash("Description field empty")
            is_valid = False
        if len(recipe['name']) < 1:
            flash("Instructions field empty")
            is_valid = False
        if not recipe['created_at']:
            flash("Date field empty")
            is_valid = False

        return is_valid