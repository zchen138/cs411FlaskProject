from flask import Flask
from flask import request, redirect, render_template, url_for, session
from flask_wtf import Form
from wtforms import StringField, SubmitField, SelectField, RadioField, FieldList, FormField, validators
import objects as obj
import requestRating as requestRating
import recommender as reco
import grabMovieInfo as movieGetter
import MySQLdb
import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds
import movieInfoProcessor as movieInfoProc
import random

app = Flask(__name__)
app.debug=True
app.config["SECRET_KEY"] = "secret-pass"

def getConnection():

    return MySQLdb.connect(host="us-cdbr-iron-east-05.cleardb.net",
                           user="b997f1857ff9ec",
                           password="5eb18692",
                           db="heroku_37da5348cc1f7c7")

    '''
    return MySQLdb.connect(host="localhost",
                           user="root",
                           password="pass",
                           db="cs411flaskproject")
    '''
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
    print("hi how are you doing")
    if 'username' not in session:
        return redirect(url_for('homepage'))
    form1 = MovieQueryForm()
    username = session['username']
    print("hi we are here")
    category = request.form['category']
    query = request.form['query']

    pagenum = 0

    # If a search was made on re-rendering, perform query & display
    if query and category:
        conn = getConnection()
        cur = conn.cursor()
        sqlStr = "SELECT * FROM moviedata WHERE " + str(category) + " = %s LIMIT 10 OFFSET 0"
        cur.execute(sqlStr, [query])

        movieArr = []
        rating_forms = []
        for movie_info in cur.fetchall():
            print(movie_info[0])
            cur_movie_obj = obj.createMovie(movie_info[0], movie_info[1], movie_info[2], movie_info[3], movie_info[8])
            movieArr.append(cur_movie_obj)
            rating_form = RatingForm()
            rating_form.movieId = movie_info[0]
            rating_forms.append(rating_form)
        print("did we get here")
        return render_template('search_results.html', form1=form1, form2=rating_forms, username=username,
                               movies=movieArr, category=category, searchTerm=query, pagenum=pagenum)

    return render_template('homepage.html', form=form1, username=username, error="Enter a search term")

@app.route('/search_result_page/<pagenum>',  methods=['GET', 'POST'])
def search_result_page(pagenum):

    if 'username' not in session:
        return redirect(url_for('homepage'))
    form1 = MovieQueryForm()
    username = session['username']

    category = request.form['category']
    query = request.form['searchTerm']
    print("hub hub hub")
    if query and category:
        print("blah blah blah")
        conn = getConnection()
        cur = conn.cursor()
        sqlStr = "SELECT * FROM moviedata WHERE " + str(category) + " = %s LIMIT 10 OFFSET %s"
        offset = int(pagenum)*10
        cur.execute(sqlStr, (query, offset))
        print("arr arr arr")
        movieArr = []
        rating_forms = []
        for movie_info in cur.fetchall():
            print(movie_info[0])
            cur_movie_obj = obj.createMovie(movie_info[0], movie_info[1], movie_info[2], movie_info[3], movie_info[8])
            movieArr.append(cur_movie_obj)
            rating_form = RatingForm()
            rating_form.movieId = movie_info[0]
            rating_forms.append(rating_form)

        return render_template('searchResultPage.html', form1=form1, form2=rating_forms, username=username,
                               movies=movieArr, category=category, searchTerm=query, pagenum=pagenum)

    return render_template('homepage.html', form=form1, username=username)
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

@app.route('/searchMovie')
def searchMovie():
    if 'username' not in session:
        return redirect(url_for('homepage'))
    form1 = MovieQueryForm()
    username = session['username']

    return render_template('searchMovies.html', form=form1, username=username)

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

@app.route('/recommend', methods = ['GET', 'POST'])
def recommend():
    if 'username' not in session:
        return redirect(url_for('homepage'))
    _userid = session['userid']

    conn = getConnection()
    cur = conn.cursor()

    sqlStr = "SELECT moviedata.* FROM moviedata, rated WHERE userId = %s AND moviedata.movieId = rated.movieId"    
    cur.execute(sqlStr, [_userid])
    movies = cur.fetchall()

    sqlStr = "SELECT moviedata.title FROM moviedata, rated WHERE userId = %s AND moviedata.movieId = rated.movieId"    
    cur.execute(sqlStr, [_userid])
    movie_names = np.array(cur.fetchall())
    #print(movie_names)

    topten = []
    if len(movies) <= 10:
        topten = movies
    else:
        topRating = movies[0].rating
        for cur in movies:
            if cur.rating > topRating:
                topRating = cur.rating

        while(len(topten) != 10):
            for cur in movies:
                if cur.rating == topRating:
                    topten.append(cur)
            topRating -= 1
    #topten now had users top ten rated movies
    #print(topten[0])

    d = {}
    for curMovie in topten:
        if curMovie[8] not in d:
            d[curMovie[8]] = curMovie[4]
        else:
            d[curMovie[8]] += curMovie[4]

    bestGenre = 'actionMovie'
    for key in d:
        bestGenre = key

    for key in d:
        if d[key] > d[bestGenre]:
            bestGenre = key
    #print(bestGenre)

    sqlStr = "SELECT moviedata.* FROM moviedata WHERE moviedata.genre = %s"    
    cur.execute(sqlStr, [bestGenre])

    moves = cur.fetchall()

    recommendations = []
    recommendations_names= []
    for i in range(90):
        maxwins = 0
        bestMovie = cur.fetchone()
        #if (bestMovie == None):
        #    break
        for movie_info in moves:
            if maxwins < movie_info[5] and ([movie_info[1]] not in movie_names) and (movie_info[1] not in recommendations_names):
                maxwins = movie_info[5]
                bestMovie = movie_info
        if( bestMovie == None):
            break
        recommendations.append(bestMovie)
        recommendations_names.append(bestMovie[1])
    #print(recommendations)

    
    if 'username' not in session:
        return redirect(url_for('homepage'))
    _userid = session['userid']
    conn = getConnection()
    cur = conn.cursor()
    sqlStr = "SELECT moviedata.* FROM moviedata, rated WHERE userId = %s AND moviedata.movieId = rated.movieId"    
    cur.execute(sqlStr, [_userid])
    movies = cur.fetchall()
    sqlStr = "SELECT moviedata.title FROM moviedata, rated WHERE userId = %s AND moviedata.movieId = rated.movieId"    
    cur.execute(sqlStr, [_userid])
    movie_names = np.array(cur.fetchall())
    
    topten = []
    if len(movies) <= 10:
        topten = movies
    else:
        topRating = movies[0].rating
        for cur in movies:
            if cur.rating > topRating:
                topRating = cur.rating
        while(len(topten) != 10):
            for cur in movies:
                if cur.rating == topRating:
                    topten.append(cur)
            topRating -= 1
    user_vector = np.zeros(22 ,dtype = float)
    
    for movie in topten:
        for i in range(22):
            user_vector[i] += int(movie[i+9])
    user_vector /= float(len(topten))

    sqlStr = "SELECT moviedata.* FROM moviedata"    
    cur.execute(sqlStr)
    movies = cur.fetchall()
    similarity_rating = np.zeros(len(movies), dtype=float)
    for m in range(len(movies)):
        cur_movie_vector = np.zeros(22, dtype=float)
        for i in range(22):
            cur_movie_vector[i] += int(movies[m][i+9])
        similarity_rating[m] = np.dot(user_vector, cur_movie_vector)
     
    movie_indices = np.argsort(similarity_rating)[-100:]
    movie_ratings = np.zeros(100, dtype=float)
    
    for i in range(len(movie_indices)):
        movie_ratings[i] = float(movies[movie_indices[i]][4])
    ranked_indices = np.argsort(movie_ratings)[0:]
    recommendations2 = []
    
    for i in range(len(ranked_indices)):
        recommendations2.append(movies[movie_indices[ranked_indices[i]]])

    finalrecs = []
    count = 0
    for rec in recommendations:
        if rec in recommendations2:
            finalrecs.append(rec)
    print(len(finalrecs))
    while len(finalrecs) < 10 and len(finalrecs) != len(recommendations):
        for rec in recommendations:
            if rec not in finalrecs:
                finalrecs.append(rec)
        


    return render_template('recommend.html', movies=finalrecs[0:10])


@app.route('/featuredActionMovies', methods = ['GET', 'POST'])
def featuredActionMovies():
    if 'username' not in session:
        return redirect(url_for('homepage'))
    _userid = session['userid']
    conn = getConnection()
    cur = conn.cursor()
    sqlStr = "SELECT moviedata.* FROM moviedata, rated WHERE userId = %s AND moviedata.movieId = rated.movieId"    
    cur.execute(sqlStr, [_userid])
    movies = cur.fetchall()
    sqlStr = "SELECT moviedata.title FROM moviedata, rated WHERE userId = %s AND moviedata.movieId = rated.movieId"    
    cur.execute(sqlStr, [_userid])
    movie_names = np.array(cur.fetchall())
    
    

    sqlStr = "SELECT moviedata.* FROM moviedata"    
    cur.execute(sqlStr)
    movies = cur.fetchall()

    topAction = []
    allAction = []
    for m in range(len(movies)):
        if (movies[m][9] == 1):
            allAction.append(m)    

    if (len(allAction) > 100):    
        random.shuffle(allAction)
        allAction = allAction[0:100]

    actionRatings = []

    for i in range(len(allAction)):
        actionRatings.append(movies[allAction[i]][4])


    ranked_indices = np.argsort(actionRatings)[-10:]

    
    for i in range(len(ranked_indices)):
        topAction.append(movies[allAction[ranked_indices[i]]])

    return render_template('featuredActionMovies.html', movies=topAction, genre="Action")


@app.route('/featuredComedyMovies', methods = ['GET', 'POST'])
def featuredComedyMovies():
    if 'username' not in session:
        return redirect(url_for('homepage'))
    _userid = session['userid']
    conn = getConnection()
    cur = conn.cursor()
    sqlStr = "SELECT moviedata.* FROM moviedata, rated WHERE userId = %s AND moviedata.movieId = rated.movieId"    
    cur.execute(sqlStr, [_userid])
    movies = cur.fetchall()
    sqlStr = "SELECT moviedata.title FROM moviedata, rated WHERE userId = %s AND moviedata.movieId = rated.movieId"    
    cur.execute(sqlStr, [_userid])
    movie_names = np.array(cur.fetchall())
    
    

    sqlStr = "SELECT moviedata.* FROM moviedata"    
    cur.execute(sqlStr)
    movies = cur.fetchall()

    topAction = []
    allAction = []
    for m in range(len(movies)):
        if (movies[m][14] == 1):
            allAction.append(m)    

    if (len(allAction) > 100):    
        random.shuffle(allAction)
        allAction = allAction[0:100]

    actionRatings = []

    for i in range(len(allAction)):
        actionRatings.append(movies[allAction[i]][4])


    ranked_indices = np.argsort(actionRatings)[-10:]

    
    for i in range(len(ranked_indices)):
        topAction.append(movies[allAction[ranked_indices[i]]])

    return render_template('featuredComedyMovies.html', movies=topAction, genre="Comedy")



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

@app.route("/viewMovieInfo", methods=['GET', 'POST'])
def viewMovieInfo():
    form = MovieQueryForm()
    _userid = session['userid']
    username = session['username']

    movieid = request.form['movieId']
    query = request.form['searchTerm']
    category = request.form['category']
    pagenum = request.form['pagenum']

    conn = getConnection()
    cur = conn.cursor()

    sqlStr = "SELECT title, releaseYear, rating, runtime FROM moviedata WHERE movieid = %s"
    cur.execute(sqlStr, [movieid])
    curMovieObj = cur.fetchone()
    directors, actors, plot, posterUrl = movieGetter.returnMovieInfo(curMovieObj[0], curMovieObj[1])

    predictedRating = requestRating.requestRating(_userid, movieid, cur)

    if (predictedRating==-1):
        predictedRating = "NA"

    return render_template('movieInformation.html', directors=directors, actors=actors[:5], plot=plot,
                           category=category, query=query, predictedRating=predictedRating,
                           pagenum=pagenum, releaseYear=curMovieObj[1], imdbRating=curMovieObj[2], runtime=curMovieObj[3], posterUrl=posterUrl,  movieTitle=curMovieObj[0])

if __name__ == "__main__":
    app.run(debug=True)
