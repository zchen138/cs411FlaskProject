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
    other_rating = -1

    def __init__(self, movieid, title, releaseYear, runtime, genre, rating, other_rating):
        self.movieid = movieid
        self.title = title
        self.releaseYear = releaseYear
        self.runtime = runtime
        self.genre = genre
        self.rating = rating
        self.other_rating = other_rating

class recommendMovie(object):
    movieid = -1
    title = ""
    releaseYear = -1
    runtime = -1
    rating = -1
    numRatings = -1
    numWins = -1
    numGenres = -1
    genre = -1
    actionMovie = -1
    adult = -1
    adventure = -1
    biography = -1
    comedy = -1
    crime = -1
    documentary = -1
    drama = -1
    family = -1
    fantasy = -1
    filmNoir = -1
    history = -1
    horror = -1
    mystery = -1
    romance = -1
    SciFi = -1
    short = -1
    sport = -1
    thriller = -1
    war = -1
    western = -1

    
    def __init__(self, movieid, title, releaseYear, runtime, rating, numRatings, numWins, numGenres, genre, actionMovie, adult, adventure, animation,
    biography, comedy, crime, documentary, drama, family, fantasy, filmNoir, history, horror, mystery, romance, SciFi, short, sport, 
    thriller, war, western):
        self.movieid = movieid
        self.title = title
        self.releaseYear = releaseYear
        self.runtime = runtime
        self.rating = rating
        self.numRatings = numRatings
        self.numWins = numWins
        self.numGenres = numGenres
        self.genre = genre
        self.actionMovie = actionMovie
        self.adult = adult
        self.adventure = adventure
        self.biography = biography
        self.comedy = comedy
        self.crime = crime
        self.documentary = documentary
        self.drama = drama
        self.family = family
        self.fantasy = fantasy
        self.filmNoir = filmNoir
        self.history = history
        self.horror = horror
        self.mystery = mystery
        self.romance = romance
        self.SciFi = SciFi
        self.short = short
        self.sport = sport
        self.thriller = thriller
        self.war = war
        self.western = western

class GroupedMovie(object):
    genre = ""
    count = -1

    def __init__(self, genre, count):
        self.genre = genre
        self.count = count

def createUser(userid, username):
    user = User(userid, username)
    return user

def createRatedMovie(movieid, title, releaseYear, runtime, genre, rating, other_rating):
    ratedMovie = RatedMovie(movieid, title, releaseYear, runtime, genre, rating, other_rating)
    return ratedMovie

def createMovie(movieid, title, releaseYear, runtime, genre):
    movie = Movie(movieid, title, releaseYear, runtime, genre)
    return movie

def createGroupMovie(genre, count):
    groupMovie = GroupedMovie(genre, count)
    return groupMovie