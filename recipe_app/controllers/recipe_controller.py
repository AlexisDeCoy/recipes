from flask import render_template, request, redirect, session
from recipe_app import app
from recipe_app.models.user import User, bcrypt
from recipe_app.models.recipe import Recipe

@app.route("/recipe-info/<int:recipe_id>")
def show_recipe(recipe_id):

    data = {
        "recipe_id" : recipe_id
    }

    recipe = Recipe.get_by_id(data)
    
    print(recipe)
    return render_template("recipe_info.html", recipe = recipe)

@app.route("/add-recipe")
def show_add_recipe():

    return render_template("add_recipe.html")

@app.route("/edit-recipe/<int:recipe_id>")
def show_edit_recipe(recipe_id):
    data = {
        'recipe_id': recipe_id
    }

    recipe = Recipe.get_by_id(data)
    return render_template("edit_recipe.html", recipe=recipe)

@app.route("/recipes/make-recipe", methods=['POST'])
def add_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/add-recipe')

    Recipe.make_recipe(request.form)
    return redirect('/recipes')

@app.route('/edit-recipe', methods=['POST'])
def edit_recipe():
    recipe_id = request.form['recipe_id']
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/edit-recipe/{recipe_id}')

    Recipe.edit_recipe(request.form)
    return redirect('/recipes')


@app.route('/recipes/delete/<int:recipe_id>')
def remove_recipe(recipe_id):
    data = {
        'recipe_id': recipe_id
    }
    Recipe.delete_recipe(data)
    return redirect('/recipes')


