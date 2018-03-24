class User(object):
    userid = -1
    username = ""
    movieIds = []

    def __init__(self, userid, username):
        self.userid = userid
        self.username = username

    def addMovie(self, movieid):
        self.movieIds = self.movieIds.append(movieid)

def createUser(userid, username):
    user = User(userid, username)
    return user

