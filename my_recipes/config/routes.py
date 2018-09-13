from my_recipes import app
from my_recipes.controllers.recipes import Recipes

recipes = Recipes()


@app.route("/")
def home():
    return recipes.home()


@app.route("/dashboard")
def dashboard():
    return recipes.dashboard()


@app.route("/add")
def add_recipe():
    return recipes.add_recipe()


@app.route("/view")
def view():
    return recipes.view()


@app.route("/edit/<recipe_id>")
def edit(recipe_id):
    return recipes.edit(recipe_id)


@app.route("/delete/<recipe_id>")
def delete(recipe_id):
    return recipes.delete(recipe_id)


@app.route("/reg", methods=["POST"])
def reg():
    return recipes.reg()


@app.route("/instructions/<recipe_id>")
def instructions(recipe_id):
    return recipes.instructions(recipe_id)


@app.route("/form", methods=["POST"])
def form():
    return recipes.form()


@app.route("/logout")
def logOut():
    return recipes.logOut()


@app.route("/login", methods=["POST"])
def logIn():
    return recipes.logIn()
