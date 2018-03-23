from flask import Flask
from flask import request, redirect, render_template, url_for
import MySQLdb

app = Flask(__name__)
conn = MySQLdb.connect(host="localhost", user="root", password="pass", db="cs411flaskproject")

app.config[""]

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/loginUser', methods=['GET', 'POST'])
def loginUser():
    if request.method == 'POST':

        cur = conn.cursor()

        _username = request.form['username']
        _password = request.form['password']
        cur.execute("SELECT COUNT(1) FROM users WHERE username = %s;", [_username])  # CHECKS IF USERNAME EXSIST
        if cur.fetchone()[0]:
            cur.execute("SELECT password FROM users WHERE username = %s;", [_username])  # FETCH THE HASHED PASSWORD
            for row in cur.fetchall():
                if _password == row[0]:
                    session['username'] = _username
                    return redirect(url_for('index'))
                else:
                    error = "Invalid Credential"
        else:
            error = "Invalid Credential"
    return render_template('login.html', error=error)
