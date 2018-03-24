class User(object):
    userid = -1
    username = ""

    def __init__(self, userid, username):
        self.userid = userid
        self.username = username

class Movie(object):
    movieid = -1
    title = ""
    releaseYear = -1
    runtime = -1
    genre = ""

    def __init__(self, movieid, title, releaseYear, runtime, genre):
        self.movieid = movieid
        self.title = title
        self.releaseYear = releaseYear
        self.runtime = runtime
        self.genre = genre

class RatedMovie(object):
    movieid = -1
    title = ""
    releaseYear = -1
    runtime = -1
    genre = ""
    rating = -1

    def __init__(self, movieid, title, releaseYear, runtime, genre, rating):
        self.movieid = movieid
        self.title = title
        self.releaseYear = releaseYear
        self.runtime = runtime
        self.genre = genre
        self.rating = rating



def createUser(userid, username):
    user = User(userid, username)
    return user

def createRatedMovie(movieid, title, releaseYear, runtime, genre, rating):
    ratedMovie = RatedMovie(movieid, title, releaseYear, runtime, genre, rating)
    return ratedMovie

def createMovie(movieid, title, releaseYear, runtime, genre):
    movie = Movie(movieid, title, releaseYear, runtime, genre)
    return movie

