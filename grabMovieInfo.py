from imdb import IMDb

ia = IMDb()

def getMovieInformation(imbdId):
    curMovie = ia.get_movie(imbdId)
    directors = curMovie['directors']
    directorArr = []
    for director in directors:
        directorArr.append(director['name'])
    actors = curMovie['cast']
    actorsArr = []
    for actor in actors:
        actorsArr.append(actor['name'])

    plot = curMovie['plot']

    return directorArr, actorsArr, plot

def returnMovieInfo(title, year):
    movies = ia.search_movie(title)
    for movie in movies:
        keys = movie.keys()
        if ('year' in keys and movie['year']==year):
            directors, actors, plot = getMovieInformation(movie.getID())
            return directors, actors, plot
