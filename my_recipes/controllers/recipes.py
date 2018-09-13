from flask import Flask, render_template, request, redirect, session, flash, jsonify
from my_recipes.models.recipe import Recipe
import re
#from my_recipes import bcrypt
import datetime
#from flask_bcrypt import Bcrypt


recipe = Recipe()

class Recipes():

    def home(self):

        return render_template("recipes.html")


    def dashboard(self):
        if "user_id" in session:
            session["user"] = recipe.getInfo()
            session["user"] = session["user"][0]

            return render_template("recipes_dashboard.html")
        else:
            return redirect("/")


    def create(self):

        return render_template("recipes_create.html")


    def view(self):

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
            return redirect("/") #failure
        else:
            session["user_id"] = recipe.add()
            return redirect("/dashboard") #success
    

    def logIn(self):

        session["user_id"] = recipe.logIn()
        if session["user_id"]:
            return redirect("/dashboard")#success
            

        flash("Incorrect name or password", "login")
        return redirect("/")#failure



    def logOut(self):
        session.clear()
        return redirect("/")

    
    def edit(self):

        return render_template("recipes_edit.html")

    
    def instructions(self):

        return render_template("recipes_instructions.html")


    def form(self):
        #do add or edit
        return redirect("/view")