from flask import Flask
from flask import request, redirect, render_template, url_for, session
import MySQLdb

app = Flask(__name__)
conn = MySQLdb.connect(host="localhost", user="root", password="pass", db="cs411flaskproject")
app.config["SECRET_KEY"] = "secret-pass"


@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return 'Logged in as ' + username + '<br>' + \
               "<b><a href = '/logout'>click here to log out</a></b>"


    return "You are not logged in <br><a href = '/login'></b>" + \
       "click here to log in</b></a>\n" + \
    "<br><a href = '/register'></b>" + \
       "click here to register</b></a>"


@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/loginUser', methods=['GET', 'POST'])
def loginUser():
    error = None
    cur = conn.cursor()

    if request.method == 'POST':
        _username = request.form['username']
        _password = request.form['password']
        cur.execute("SELECT COUNT(1) FROM users WHERE username = %s;", [_username])
        if cur.fetchone()[0]:
            cur.execute("SELECT password FROM users WHERE username = %s;", [_username])
            for row in cur.fetchall():
                if _password == row[0]:
                    session['username'] = _username
                    return redirect(url_for('index'))
                else:
                    error = "Invalid username or password"
        else:
            error = "Invalid username or password"
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/registerUser', methods=['POST'])
def registerUser():
    error = None
    cur = conn.cursor()
    _username = request.form['username']
    _password = request.form['password']

    if _username and _password:
        cur.execute("SELECT * FROM users WHERE username = %s", [_username])
        if cur.rowcount == 0:
            cur.execute("INSERT INTO users(username, password) VALUES (%s, %s)", (_username, _password))
            return redirect(url_for('index'))
        else:
            error = "That username is taken. Try again"
            return render_template('register.html', error=error)
    else:
        error = "Enter a valid username and password."
        return render_template('register.html', error=error)

if __name__ == "__main__":
    app.run(debug=True)