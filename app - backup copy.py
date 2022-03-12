import datetime
from flask import Flask, redirect, render_template, request, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os
app = Flask(__name__)

app.secret_key = '1234567890'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'group_2'

mysql = MySQL(app)
msg = ""

#the code below is going to load our index page
@app.route("/")
def index():
    email = 'group2@gmail.com'
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM precious_users')
    account = cursor.fetchone()
    if account:
        msg = "exist"
        email = account['email']
    else:
        msg = "not exist"
    return render_template("index.html", msg = msg, email = email)

    email = account['email']


@app.route("/signup", methods=["POST", "GET"])
def register():
    if request.form:
        user_mail = request.form.get("email")
        pwd = request.form.get("pass")
        print(user_mail + pwd)
    return render_template("register.html", msg = msg)

if __name__ == "__main__":
    app.run(debug=true)
  #  app.run()  

#you can use 
