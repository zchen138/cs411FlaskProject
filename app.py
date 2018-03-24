from flask import Flask
from flask import request, redirect, render_template, url_for, session
import MySQLdb
import objects as obj

app = Flask(__name__)
app.debug=True

app.config["SECRET_KEY"] = "secret-pass"
def getConnection():
    '''
    return MySQLdb.connect(host="us-cdbr-iron-east-05.cleardb.net",
                           user="b997f1857ff9ec",
                           password="5eb18692",
                           db="heroku_37da5348cc1f7c7")

    '''
    return MySQLdb.connect(host="localhost",
                           user="root",
                           password="pass",
                           db="cs411flaskproject")

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
            cur.execute("SELECT * FROM users WHERE username = %s;", [_username])
            for row in cur.fetchall():
                if _password == row[2]:
                    session['username'] = _username
                    session['userid'] = row[0]
                    return redirect(url_for('index'))
                else:
                    error = "Invalid username or password"
        else:
            error = "Invalid username or password"
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('userid', None)
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

@app.route('/getProfile')
def getProfile():

    _username = session['username']
    _userid = session['userid']
    curUser = obj.createUser(_userid, _username)

    error = None
    conn = getConnection()
    cur = conn.cursor()

    if _username and _userid:
        cur.execute("SELECT movieid, rating FROM rated WHERE userid = %s", [_userid])
        movies_and_ratings = cur.fetchall()
        movie_info_arr = []
        for one_movie_rating in movies_and_ratings:
            cur_movie_id = one_movie_rating[0]
            cur_rating = one_movie_rating[1]
            cur.execute("SELECT title, releaseYear, runtime, genre FROM movieinfo WHERE movieid = %s", [cur_movie_id])
            movie_info = cur.fetchone()
            cur_movie_obj = obj.createRatedMovie(cur_movie_id, movie_info[0], movie_info[1], movie_info[2], movie_info[3], cur_rating)
            movie_info_arr.append(cur_movie_obj)

        return render_template('profile.html', movieList=movie_info_arr, user=curUser)



if __name__ == "__main__":
    app.run(debug=True)
