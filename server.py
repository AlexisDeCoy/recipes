from recipe_app.controllers import user_controller
from recipe_app.controllers import recipe_controller
from recipe_app import app

if __name__ == "__main__":
    app.run(debug=True)

# MVC = Models, Views, Controllers