import datetime
from flask import Flask, redirect, render_template, request, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from tp_functions import *

app = Flask(__name__)

app.secret_key = '1234567890'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tour_plateau'

mysql = MySQL(app)
msg = ""
style_class = ""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST' and 'email' in request.form and 'pwd' in request.form: #that means our reg form has been submitted. Proceed to get the supplied form data and store in variables
        email = request.form.get("email")
        passwd = request.form.get("pwd")
        rememberMe = request.form.get("remember")
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tp_users WHERE email = % s AND pass = % s', (email, passwd))
        account = cursor.fetchone()
        if account == None:
            msg = passwd
            style_class = "alert alert-danger"
            return render_template("login.html", msg = msg, style_class = style_class)
        else:
            session['loggedin'] = True
            session['uid'] = account['uid']
            session['fname'] = account['f_name']
            session['lname'] = account['l_name']
            session['email'] = account['email']

            return redirect(url_for('admin_section'))

    return render_template("login.html")

@app.route("/logout", methods=["POST", "GET"])
def logout():
    session.pop('loggedin', None)
    session.pop('uid', None)
    session.pop('fname', None)
    session.pop('lname', None)
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route("/signup", methods=["POST", "GET"])
def register():
    if request.form: #that means our reg form has been submitted. Proceed to get the supplied form data and store in variables
        userName = request.form.get("username")
        user_mail = request.form.get("email")
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        passwd = generate_password_hash(request.form.get("pwd"))
        verifyPass = request.form.get("ver_pwd")
        gender = request.form.get("gender")
        terms_condition = request.form.get("tc")
        uid = uuid.uuid1().hex
        country = request.form.get("country")
        role = 1
        dob = ""
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO tp_users (`uid`,`email`, `pass`, `f_name`, `l_name`, `gender`, `country`, `role`) VALUES (% s, % s, % s, % s, % s, % s, % s, % s)', (uid, user_mail, passwd, firstName, lastName, gender, country, role))
        mysql.connection.commit()
        return redirect(url_for('login', st = 1))
    return render_template("register.html", msg = msg)

@app.route("/recover", methods=["POST", "GET"])
def recover():
    if request.form: #that means our reg form has been submitted. Proceed to get the supplied form data and store in variables
        userName = request.form.get("username")
        user_mail = request.form.get("email")
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        passwd = request.form.get("pwd")
        verifyPass = request.form.get("ver_pwd")
        gender = request.form.get("gender")
        terms_condition = request.form.get("tc")
    return render_template("register.html", msg = msg)

@app.route("/admin/dashboard")
def admin_section():
    if 'loggedin' in session:
        return render_template("dashboard.html")
    else:
        msg = "Bros! Be Humble and LOGIN first"
        return redirect(url_for('login', ts=4))

@app.route("/post/<post_url>")
def viewSinglePost(post_url):
    url = post_url
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(f'SELECT * FROM tp_blog WHERE pid = {url} LIMIT 1')
    FoundPost = cursor.fetchone()

    cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor2.execute(f'SELECT * FROM tp_comments WHERE comment_on = {url} ORDER BY `comment_date` DESC LIMIT 5')
    FoundComments = cursor2.fetchall()
    
    if FoundPost == None:
        msg = "No post Found"
    else:
        return render_template("viewSinglePost.html", thisPost = FoundPost, thisComments = FoundComments)

@app.route("/view/<key>/<page_no>")
def viewSection(key, page_no):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(f'SELECT * FROM ep_blog WHERE section = {key} LIMIT 9')
    FoundPost = cursor3.fetchall()
    return cursor
    """ if FoundPost == None:
        msg = "No post Found"
    else:
        return render_template("viewSectionAll.html", allpost = FoundPost) """


@app.route("/blog/<category>")
def blog_post(category):
    postPerPage = 2
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM tp_blog LIMIT 9')
    allpost = cursor.fetchall()
    return render_template("blog.html", allpost = allpost, cat = category)

@app.route("/test", methods=["POST", "GET"])
def test():
    result = ""
    id = uuid.uuid1()
    #id = id.int
    id = id.hex
    #use uuid4 instead
    test = hello()
    return render_template("test.html", result = test)

if __name__ == "__main__":
    app.run(debug=true)
  # app.run() 