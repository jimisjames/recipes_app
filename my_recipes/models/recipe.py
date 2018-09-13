from flask import Flask, render_template, request, redirect, session, flash
from my_recipes.config.mysqlconnection import connectToMySQL
from my_recipes import bcrypt



class Recipe():

    def checkEmail(self):
        myDb = connectToMySQL('recipes')
        for user in myDb.query_db("SELECT email FROM users;"):
            if request.form["email"] == user["email"]:
                return True
        return False

    def add_user(self):
        myDb = connectToMySQL('recipes')
        query = "INSERT INTO users (name, email, location, password, created_at, updated_at) VALUES (%(name)s, %(email)s, %(location)s, %(password)s, now(), now());"
        data = {
            "name" : request.form["name"],
            "email" : request.form["email"],
            "location" : request.form["location"],
            "password" : bcrypt.generate_password_hash(request.form["password"] + "melon")
        }
        return myDb.query_db(query, data)

    def getInfo(self):
        myDb = connectToMySQL('recipes')
        query = "SELECT name, email, created_at FROM users WHERE id = %(id)s;"
        data = {
            "id" : session["user_id"]
        }
        return myDb.query_db(query, data)

    def logIn(self):
        myDb = connectToMySQL('recipes')
        query = "SELECT name, id, password, created_at FROM users WHERE name = %(name)s;"
        data = {
            "name" : request.form["name"]
        }
        users = myDb.query_db(query, data)

        for user in users:
            if bcrypt.check_password_hash(user["password"], request.form["password"] + "melon"):
                return user
        return False

    def view(self):
        myDb = connectToMySQL('recipes')
        query = "SELECT * FROM recipes WHERE user_id = %(user_id)s;"
        data = {
            "user_id" : session["user_id"]
        }
        return myDb.query_db(query, data)

    def add_recipe(self):
        myDb = connectToMySQL('recipes')
        query = "INSERT INTO recipes (user_id, name, description, instructions, under_30, created_at, updated_at) VALUES (%(user_id)s, %(name)s, %(description)s, %(instructions)s, %(under_30)s, now(), now());"
        data = {
            "user_id" : session["user_id"],
            "name" : request.form["name"],
            "description" : request.form["description"],
            "instructions" : request.form["instructions"],
            "under_30" : request.form["under_30"]
        }
        newRecipeId = myDb.query_db(query, data)
        return newRecipeId

    def edit_recipe(self):
        myDb = connectToMySQL('recipes')
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under_30 = %(under_30)s, updated_at = now() WHERE id = %(id)s;"
        data = {
            "id" : session["recipe_id"],
            "name" : request.form["name"],
            "description" : request.form["description"],
            "instructions" : request.form["instructions"],
            "under_30" : request.form["under_30"]
        }
        myDb.query_db(query, data)
        return

    def getRecipe(self, recipe_id):
        myDb = connectToMySQL('recipes')
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        data = {
            "id" : recipe_id
        }
        return myDb.query_db(query, data)

    def delete(self, recipe_id):
        myDb = connectToMySQL('recipes')
        myDb.query_db("DELETE FROM recipes WHERE id = %s;" % (recipe_id))
        return