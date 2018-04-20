from imdb import IMDb

ia = IMDb()

def getMovieInformation(imbdId):

    curMovie = ia.get_movie(imbdId)
    keys = curMovie.keys()
    directors = []
    if "directors" in keys:
        directors = curMovie['directors']
    directorArr = []
    for director in directors:
        directorArr.append(director['name'])

    actors = []
    if "cast" in keys:
        actors = curMovie['cast']
    actorsArr = []
    for actor in actors:
        actorsArr.append(actor['name'])

    plot = curMovie['plot']

    url = curMovie['cover url']

    return directorArr, actorsArr, plot, url

def returnMovieInfo(title, year):
    movies = ia.search_movie(title)
    for movie in movies:
        keys = movie.keys()
        if ('year' in keys) and (movie['year']==year):
            directors, actors, plot, url = getMovieInformation(movie.getID())
            return directors, actors, plot, url
