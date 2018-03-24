class User(object):
    userid = -1
    username = ""
    movieIds = []

    def __init__(self, userid, username):
        self.userid = userid
        self.username = username

    def addMovie(self, movieid):
        self.movieIds = self.movieIds.append(movieid)

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

