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

    def add(self):
        myDb = connectToMySQL('recipes')
        query = "INSERT INTO users (name, email, location, password, created_at, updated_at) VALUES (%(name)s, %(email)s, %(location)s, %(password)s, now(), now());"
        data = {
            "name" : request.form["name"],
            "email" : request.form["email"],
            "location" : request.form["location"],
            "password" : bcrypt.generate_password_hash(request.form["password"] + "melon")
        }
        newId = myDb.query_db(query, data)
        return newId

    def getInfo(self):
        myDb = connectToMySQL('recipes')
        query = "SELECT name, email, location FROM users WHERE id = %(id)s;"
        data = {
            "id" : session["user_id"]
        }
        return myDb.query_db(query, data)

    def logIn(self):
        myDb = connectToMySQL('recipes')
        query = "SELECT name, id, password FROM users WHERE name = %(name)s;"
        data = {
            "name" : request.form["name"]
        }
        users = myDb.query_db(query, data)

        for user in users:
            if bcrypt.check_password_hash(user["password"], request.form["password"] + "melon"):
                return user["id"]
        return False
