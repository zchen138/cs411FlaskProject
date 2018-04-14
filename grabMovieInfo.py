from imdb import IMDb

ia = IMDb()

title = "Badlands "
movies = ia.search_movie(title)
print(movies)