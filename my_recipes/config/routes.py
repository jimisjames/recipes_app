from my_recipes import app
from my_recipes.controllers.recipes import Recipes

recipes = Recipes()


@app.route("/")
def home():
    return recipes.home()


@app.route("/dashboard")
def dashboard():
    return recipes.dashboard()


@app.route("/create")
def create():
    return recipes.create()


@app.route("/view")
def view():
    return recipes.view()


@app.route("/edit")
def edit():
    return recipes.edit()


@app.route("/reg", methods=["POST"])
def reg():
    return recipes.reg()


@app.route("/instructions")
def instructions():
    return recipes.instructions()


@app.route("/form")
def form():
    return recipes.form()


@app.route("/logout")
def logOut():
    return recipes.logOut()


@app.route("/login", methods=["POST"])
def logIn():
    return recipes.logIn()