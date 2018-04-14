from imdb import IMDb

ia = IMDb()

def returnMovieInfo(title, year):
    movies = ia.search_movie(title)
    print(movies)
    for movie in movies:
        print(movie['title'])
        print(movie['year'])
        print(movie.getID())

