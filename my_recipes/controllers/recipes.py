from flask import Flask, render_template, request, redirect, session, flash, jsonify
from my_recipes.models.recipe import Recipe
import re
from my_recipes import bcrypt
import datetime



recipe = Recipe()

class Recipes():

    def home(self):

        session["user_id"] = ''
        session["secret_hash"] = ''

        return render_template("recipes.html")


    def dashboard(self):

        session["recipe_name"] = ""  #this block is all to wash these session names so they are not populated when you go to create a new record
        session["description"] = ""
        session["instructions"] = ""
        session["under_30"] = ""


        if session["user_id"] == '':
            flash("Please log in to view this page", "login")
            return redirect("/")
        else:

            session["user"] = recipe.getInfo()
            session["user"] = session["user"][0]
            if "secret_hash" in session.keys() and bcrypt.check_password_hash(session["secret_hash"], str(session["user"]["created_at"]) + "melon"):
                return render_template("recipes_dashboard.html")
            else:
                flash("Don't hack my site you jerk", "login")
                return redirect("/")



    def add_recipe(self):

        session["title"] = "Add a Recipe!"
        session["type"] = "add"

        return render_template("recipes_create.html")


    def delete(self, recipe_id):

        recipe.delete(recipe_id)

        return redirect("/view")


    def view(self):

        session["my_recipes"] = recipe.view()

        return render_template("recipes_view.html")

    
    def reg(self):

        if len(request.form["name"]) < 2:
            flash("Please enter a valid name", "name")
        elif not request.form["name"].isalpha():
            flash("Names may only contain letters", "name")

        emailRegEx = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(request.form["email"]) <= 1:
            flash("Plese enter a valid email", "email")
        elif not emailRegEx.match(request.form["email"]):
            flash("Plese enter a valid email", "email")

        if recipe.checkEmail():
            flash("That email address is already registered!", "email")

        if len(request.form["password"]) < 2:
            flash("Please enter a valid password", "password")
        elif len(request.form["password"]) < 8:
            flash("Passwords must be at least 8 characters", "password")
        
        if len(request.form["confirm_password"]) < 2:
            flash("Please confirm your password", "confirm_password")
        elif request.form["confirm_password"] != request.form["password"]:
            flash("Your password must match", "password")
            flash("Your password must match", "confirm_password")

        today = datetime.datetime.now()

        if len(request.form["birth"]) < 2:
            flash("Please enter your date of birth", "birth")
        elif datetime.datetime.strptime(request.form["birth"], "%m/%d/%Y").year > today.year - 18:
            flash("Sorry you must be 18 to use this site", "birth")

        if "_flashes" in session.keys():
            session["name"] = request.form["name"]
            session["email"] = request.form["email"]
            session["birth"] = request.form["birth"]
            return redirect("/") #failure
        else:
            session["user_id"] = recipe.add_user()
            print(str(session["user_id"]) + "*" * 10)
            return redirect("/dashboard") #success
    

    def logIn(self):

        user = recipe.logIn()
        if user:
            session["user_id"] = user["id"]
            session["secret_hash"] = bcrypt.generate_password_hash(str(user["created_at"]) + "melon")
            return redirect("/dashboard")#success

        session["name2"] = request.form["name"]
        flash("Incorrect name or password", "login")
        return redirect("/")#failure



    def logOut(self):
        session.clear()
        return redirect("/")

    
    def edit(self, recipe_id):

        session["recipe"] = recipe.getRecipe(recipe_id)
        session["recipe"] = session["recipe"][0]
        session["recipe_name"] = session["recipe"]["name"]
        session["description"] = session["recipe"]["description"]
        session["instructions"] = session["recipe"]["instructions"]
        session["under_30"] = session["recipe"]["under_30"]
        session["recipe_id"] = recipe_id
        
        session["title"] = "Edit " + session["recipe_name"] + ":"
        session["type"] = "edit"

        return render_template("recipes_create.html")

    
    def instructions(self, recipe_id):

        session["recipe"] = recipe.getRecipe(recipe_id)
        session["recipe"] = session["recipe"][0]


        return render_template("recipes_instructions.html")


    def form(self):

        if len(request.form["name"]) < 1:
            flash("Please enter a name", "name")

        if len(request.form["description"]) < 1:
            flash("Please enter a description", "description")

        if len(request.form["instructions"]) < 1:
            flash("Please enter instructions", "instructions")

        if not "under_30" in request.form:
            flash("Please indicate time to cook", "under_30")


        if "_flashes" in session.keys():
            session["recipe_name"] = request.form["name"]
            session["description"] = request.form["description"]
            session["instructions"] = request.form["instructions"]
            if "under_30" in request.form.keys():
                session["under_30"] = request.form["under_30"]
            if session["type"] == "add":
                return redirect("/add")
            elif session["type"] == "edit":
                return redirect("/edit/%s" % (session['recipe']['id']))
        else:
            session["recipe_name"] = ""
            session["description"] = ""
            session["instructions"] = ""
            session["under_30"] = ""
            if session["type"] == "add":
                recipe.add_recipe()
            elif session["type"] == "edit":
                recipe.edit_recipe()
            return redirect("/view")