from flask import Flask, render_template, request, redirect, session, flash, jsonify
from datetime import datetime
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
import re

from recipes import app

myData = connectToMySQL('recipes')

emailRegEx = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


@app.route("/")
def home():

    return render_template("recipes.html")


@app.route("/dashboard")
def dashboard():

    return render_template("recipes_dashboard.html")


@app.route("/create")
def create():

    return render_template("recipes_create.html")


@app.route("/view")
def view():

    return render_template("recipes_view.html")




if __name__ == "__main__":
    app.run(debug=True)