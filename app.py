from flask import Flask
from flask import request, redirect, render_template, url_for, session
from flask_wtf import Form
from wtforms import StringField, SubmitField, SelectField, RadioField, FieldList, FormField, validators
import objects as obj
import recommender as reco
import MySQLdb

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
    
class MovieQueryForm(Form):
    query = StringField([validators.DataRequired("Please enter a search term.")])
    category = SelectField('Category', choices=[('title', 'title'), ('genre', 'genre'), ('releaseYear', 'releaseYear')])
    submit = SubmitField("Search")

@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    form = MovieQueryForm()
    username = session['username']

    if request.method == 'POST':
        if not form.validate():
            error = 'Enter a search term.'
            return render_template('homepage.html', form=form, error=error, username=username)
        else:
            return render_template('homepage.html', form=form, username=username)
    elif request.method == 'GET':
        return render_template('homepage.html', form=form, username=username)

class RatingForm(Form):
    rating = RadioField('Rating', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
    submit = SubmitField("Rate")
    movieId = 0

class ChangeRatingForm(Form):
    rating = RadioField('Rating', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
    update = SubmitField("Update")
    remove = SubmitField("Remove")
    movieId = 0

@app.route('/first_search_results', methods=['GET', 'POST'])
def search_results():
    if 'username' not in session:
        return redirect(url_for('homepage'))
    form1 = MovieQueryForm()
    username = session['username']

    category = request.form['category']
    query = request.form['query']

    # If a search was made on re-rendering, perform query & display
    if query and category:
        conn = getConnection()
        cur = conn.cursor()
        sqlStr = "SELECT * FROM moviedata WHERE " + str(category) + " = %s LIMIT 10 OFFSET 0"
        cur.execute(sqlStr, [query])

        movieArr = []
        rating_forms = []
        for movie_info in cur.fetchall():
            cur_movie_obj = obj.createMovie(movie_info[0], movie_info[1], movie_info[2], movie_info[3], movie_info[8])
            movieArr.append(cur_movie_obj)
            rating_form = RatingForm()
            rating_form.movieId = movie_info[0]
            rating_forms.append(rating_form)

        return render_template('search_results.html', form1=form1, form2=rating_forms, username=username, movies=movieArr)

    return render_template('homepage.html', form1=form1, username=username, error="Enter a search term")

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('homepage'))
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

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('homepage'))
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
        rating_forms = []
        delete_forms = []
        for one_movie_rating in movies_and_ratings:
            cur_movie_id = one_movie_rating[0]
            cur_rating = one_movie_rating[1]
            cur.execute("SELECT title, releaseYear, runtime, genre FROM moviedata WHERE movieid = %s", [cur_movie_id])
            movie_info = cur.fetchone()
            cur_movie_obj = obj.createRatedMovie(cur_movie_id, movie_info[0], movie_info[1], movie_info[2], movie_info[3], cur_rating, 0)
            movie_info_arr.append(cur_movie_obj)

            rating_form = ChangeRatingForm()
            rating_form.movieId = cur_movie_id
            rating_forms.append(rating_form)

        sqlStr = "SELECT COUNT(moviedata.movieid), moviedata.genre FROM rated, moviedata WHERE rated.userid = %s AND " \
                 "rated.movieid = moviedata.movieid " \
                 "GROUP BY genre;"

        cur.execute(sqlStr, [_userid])
        pairArr = []
        for pair in cur.fetchall():
            pairObj = obj.createGroupMovie(pair[1], pair[0])
            pairArr.append(pairObj)

        return render_template('profile.html', movieList=movie_info_arr, form2=rating_forms, user=curUser, counts=pairArr)

# TODO advanced queries and integration, import data properly

@app.route('/users')
def users():
    if 'username' not in session:
        return redirect(url_for('homepage'))
    _userid = session['userid']
    conn = getConnection()
    cur = conn.cursor()

    users = []
    cur.execute("SELECT userid,username FROM users WHERE userid != %s", [_userid])
    for user in cur.fetchall():
        userObj = obj.createUser(user[0], user[1])
        users.append(userObj)

    return render_template('users.html', users=users)
'''
@app.route('/viewUser')
def viewUser():
'''
@app.route('/recommend', methods = ['GET', 'POST'])
def recommend():
    if 'username' not in session:
        return redirect(url_for('homepage'))
    _userid = session['userid']

    conn = getConnection()
    cur = conn.cursor()

    sqlStr = "SELECT movieId, rating FROM rated WHERE userid = %s"    
    cur.execute(sqlStr, [_userid])

    movieArr = []

    for data in cur.fetchall():
        userRating = data[1]
        cur_movie_id = data[0]
        sqlStr = "SELECT * FROM moviedata WHERE movieid = %s"
        cur.execute(sqlStr, [cur_movie_id])
        movieInformation = cur.fetchone()
        movieArr.append(movieInformation)
        


@app.route('/insertRating', methods=['GET', 'POST'])
def insertRating():
    if 'username' not in session:
        return redirect(url_for('homepage'))
    _userid = session['userid']
    movieid = request.form['movieId']
    rating = request.form['rating']

    conn = getConnection()
    cur = conn.cursor()

    sqlStr = "SELECT * FROM rated WHERE userid = %s AND movieid = %s"
    cur.execute(sqlStr, (_userid, movieid))
    if cur.fetchone(): # Check for duplicates
        sqlStr = "UPDATE rated SET rating = %s WHERE userid = %s AND movieid = %s"
        cur.execute(sqlStr, (rating, _userid, movieid))
        conn.commit()
    else:
        sqlStr = "INSERT INTO rated VALUES (%s, %s, %s)"
        cur.execute(sqlStr, (_userid, movieid, rating))
        conn.commit()

    return redirect(url_for('index'))

@app.route('/updateRating', methods=['GET', 'POST'])
def updateRating():
    if 'username' not in session:
        return redirect(url_for('homepage'))
    _userid = session['userid']
    movieid = request.form['movieId']
    conn = getConnection()
    cur = conn.cursor()

    print(movieid)
    if 'update' in request.form:
        rating = request.form['rating']
        sqlStr = "UPDATE rated SET rating = %s WHERE userid = %s AND movieid = %s"
        cur.execute(sqlStr, (rating, _userid, movieid))
    elif 'remove' in request.form:
        sqlStr = "DELETE FROM rated WHERE userid = %s AND movieid = %s"
        cur.execute(sqlStr, (_userid, movieid))
    conn.commit()

    return redirect(url_for('profile'))

@app.route('/users/<userid>')
def viewUser(userid):
    curUserId = session['userid']

    conn = getConnection()
    cur = conn.cursor()

    sqlStr = "SELECT movieid, rating FROM rated WHERE userid = %s AND movieid IN (SELECT movieid FROM rated WHERE userid = %s)"
    cur.execute(sqlStr, ( userid, curUserId))

    movieArr = []
    for movie in cur.fetchall():
        movieid = movie[0]
        movieRating = movie[1]
        cur.execute("SELECT title, releaseYear, runtime, genre FROM moviedata WHERE movieid = %s", [movieid])
        movie_info = cur.fetchone()
        cur.execute("SELECT rating FROM rated WHERE userid = %s AND movieid = %s", (curUserId, movieid))
        myRating = cur.fetchone()[0]
        cur_movie_obj = obj.createRatedMovie(movieid, movie_info[0], movie_info[1], movie_info[2], movie_info[3],
                                             movieRating, myRating)
        movieArr.append(cur_movie_obj)

    sqlStr = "SELECT username FROM users WHERE userid = %s"
    cur.execute(sqlStr, [userid])
    otherUser = cur.fetchone()[0]

    return render_template('view_user.html', movies=movieArr, otherUser=otherUser)

if __name__ == "__main__":
    app.run(debug=True)
