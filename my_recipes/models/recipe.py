from flask import Flask, render_template, request, redirect, session, flash
from my_recipes.config.mysqlconnection import connectToMySQL
from my_recipes import bcrypt



class Recipe():

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


    def add_user(self):
        myDb = connectToMySQL('recipes')
        query = "INSERT INTO users (name, email, location, password, created_at, updated_at) VALUES (%(name)s, %(email)s, %(location)s, %(password)s, now(), now());"
        data = {
            "name" : request.form["name"],
            "email" : request.form["email"],
            "location" : request.form["location"],
            "password" : bcrypt.generate_password_hash(request.form["password"] + "melon")
        }
        newUserId = myDb.query_db(query, data)
        newUserCreated_at = myDb.query_db("SELECT created_at FROM users WHERE id = %s" % (newUserId))
        newUserCreated_at = newUserCreated_at[0]["created_at"]
        return [newUserId, newUserCreated_at]


    def checkEmail(self):
        myDb = connectToMySQL('recipes')
        for user in myDb.query_db("SELECT email FROM users;"):
            if request.form["email"] == user["email"]:
                return True
        return False


    def delete(self, recipe_id):
        myDb = connectToMySQL('recipes')
        myDb.query_db("DELETE FROM recipes WHERE id = %s;" % (recipe_id))
        return


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


    def getInfo(self):
        myDb = connectToMySQL('recipes')
        query = "SELECT name, email, created_at FROM users WHERE id = %(id)s;"
        data = {
            "id" : session["user_id"]
        }
        return myDb.query_db(query, data)


    def getRecipe(self, recipe_id):
        myDb = connectToMySQL('recipes')
        query = "SELECT recipes.*, COUNT(likes.id) AS likes FROM recipes LEFT JOIN likes ON recipes.id = likes.recipe_id WHERE recipes.id = %(id)s GROUP BY recipes.id;"
        data = {
            "id" : recipe_id
        }
        return myDb.query_db(query, data)


    def like(self, recipe_id):
        myDb = connectToMySQL('recipes')
        likes = myDb.query_db("SELECT * FROM likes WHERE recipe_id = %s" % (recipe_id))
        for like in likes:
            if like["user_id"] == session["user_id"]:
                return

        query = "INSERT INTO likes (recipe_id, user_id, created_at, updated_at) VALUES (%(recipe_id)s, %(user_id)s, now(), now());"
        data = {
            "recipe_id" : recipe_id,
            "user_id" : session["user_id"]
        }
        myDb.query_db(query, data)
        return


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


    def unlike(self, recipe_id):
        myDb = connectToMySQL('recipes')
        query = "DELETE FROM likes WHERE recipe_id = %(recipe_id)s and user_id = %(user_id)s"
        data = {
            "recipe_id" : recipe_id,
            "user_id" : session["user_id"]
        }
        myDb.query_db(query, data)
        return


    def view(self):
        myDb = connectToMySQL('recipes')
        query = "SELECT recipes.*, COUNT(likes.id) AS likes FROM recipes LEFT JOIN likes ON recipes.id = likes.recipe_id WHERE recipes.user_id = %(user_id)s GROUP BY recipes.id;"
        data = {
            "user_id" : session["user_id"]
        }
        return myDb.query_db(query, data)


    def view_all(self):
        myDb = connectToMySQL('recipes')
        return myDb.query_db("SELECT recipes.*, users.name AS recipe_owner, COUNT(likes.id) AS likes FROM recipes JOIN users ON recipes.user_id = users.id LEFT JOIN likes ON recipes.id = likes.recipe_id GROUP BY recipes.id;")