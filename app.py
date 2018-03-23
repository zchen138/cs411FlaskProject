from flask import Flask
from flask import request, redirect, render_template, url_for, session
import MySQLdb

app = Flask(__name__)


app.config["SECRET_KEY"] = "secret-pass"
def getConnection():
    return MySQLdb.connect(host="us-cdbr-iron-east-05.cleardb.net",
                           user="b997f1857ff9ec",
                           password="5eb18692",
                           db="heroku_37da5348cc1f7c7")

    '''
     MySQLdb.connect(host="localhost",
                           user="root",
                           password="pass",
                           db="cs411flaskproject")
    '''

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return render_template('logged_in.html', username=username)
    else:
        return render_template('not_logged_in.html')

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/loginUser', methods=['GET', 'POST'])
def loginUser():
    error = None
    conn = getConnection()
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
    conn = getConnection()
    cur = conn.cursor()
    _username = request.form['username']
    _password = request.form['password']

    if _username and _password:
        cur.execute("SELECT * FROM users WHERE username = %s", [_username])
        if cur.rowcount == 0:
            cur.execute("INSERT INTO users(username, password) VALUES (%s, %s)", (_username, _password))
            conn.commit();
            return redirect(url_for('index'))
        else:
            error = "That username is taken. Try again"
            return render_template('register.html', error=error)
    else:
        error = "Enter a valid username and password."
        return render_template('register.html', error=error)

if __name__ == "__main__":
    app.run(debug=True)
