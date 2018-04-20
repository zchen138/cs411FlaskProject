"""
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
    print(movie_names)

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
    print(topten[0])

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
    print(bestGenre)

    sqlStr = "SELECT moviedata.* FROM moviedata WHERE moviedata.genre = %s"    
    cur.execute(sqlStr, [bestGenre])

    moves = cur.fetchall()

    recommendations = []
    recommendations_names= []
    for i in range(10):
        maxwins = 0
        bestMovie = cur.fetchone()
        for movie_info in moves:
            if maxwins < movie_info[5] and ([movie_info[1]] not in movie_names) and (movie_info[1] not in recommendations_names):
                maxwins = movie_info[5]
                bestMovie = movie_info
        recommendations.append(bestMovie)
        recommendations_names.append(bestMovie[1])
    print(recommendations)

    return render_template('recommend.html', movies=recommendations)




"""

"""
import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds

_userid = session['userid']

conn = getConnection()
cur = conn.cursor()

sqlStr = "SELECT movieId, title, year FROM moviedata"    
cur.execute(sqlStr)

movie_list = cur.fetchall()
movies_df = pd.DataFrame(movie_list, columns = ['MovieID', 'Title', 'Year'])

conn2 = getConnection()
cur2 = conn2.cursor()

sqlStr2 = "SELECT userId, movieId, rating FROM rated WHERE userId = %s"    
cur2.execute(sqlStr2, [_userid])

ratings_list = cur2.fetchall()
ratings_df = pd.DataFrame(ratings_list, columns = ['UserID', 'MovieID', 'Rating'])

ratings_df = ratings_df.pivot(index = 'UserID', columns ='MovieID', values = 'Rating').fillna(0)

ratings_matrix = ratings.df.as_matrix()
ratings_mean = np.mean(ratings_matrix, axis=1).reshape(-1,1)
ratings_normalized = ratings_matrix - ratings_mean

U, S, V = svds(ratings_normalized, k = 50)

S = np.diag(S)

predicted_ratings = np.dot(np.dot(U, S), V) + ratings_mean

predicted_df = pd.DataFrame(predicted_ratings, columns = ratings_df.columns)
print(predicted_df)


"""

"""import objects as obj

def recommendation(movies, allMovies):
	#movies in an array of movies that the user has rated
	# allMovies are all movies
	topten = []

	if len(movies) <= 10:
		topten = movies.copy()
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


	d = {}
	for curMovie in topten:
		if curMovie.genre not in d:
			d[curMovie.genre] = curMovie.rating
		else:
			d[curMovie.genre] += curMovie.rating

	bestGenre = d.keys()[0]
	for key in d.keys():
		if d[key] > d[bestGenre]:
			bestGenre = key
	
	conn = getConnection()
	cur = conn.cursor()

	sqlStr = "SELECT * FROM moviedata WHERE genre = %s"    
	cur.execute(sqlStr, [bestGenre])

	maxwins = 0
	bestMovie = []
	for movie_info in cur.fetchall():
		if maxwins < movie_info.numWins:
			maxwins = movie_info.numWins
			bestMovie = movie_info

	return bestMovie
"""
"""
	allScores= []
	for t in topten:
		scores = []
		for cur in allMovies:
			curScore = 0
			if t.releaseYear - cur.releaseYear < 50:
				curScore += 1
			if t.action == 1 and cur.action == 1:
				curScore += 2
			if t.adult == 1 and cur.adult == 1:
				curScore += 2
			if t.adventure == 1 and cur.adventure == 1:
				curScore += 2
			if t.animation == 1 and cur.animation == 1:
				curScore += 2
			if t.biography == 1 and cur.biography == 1:
				curScore += 2
			if t.comedy == 1 and cur.comedy == 1:
				curScore += 2
			if t.crime == 1 and cur.crime == 1:
				curScore += 2
			if t.documentary == 1 and cur.documentary == 1:
				curScore += 2
			if t.drama == 1 and cur.drama == 1:
				curScore += 2
			if t.family == 1 and cur.family == 1:
				curScore += 2
			if t.fantasy == 1 and cur.fantasy == 1:
				curScore += 2
			if t.filmnoir == 1 and cur.filmnoir == 1:
				curScore += 2
			if t.history == 1 and cur.history == 1:
				curScore += 2
			if t.mystery == 1 and cur.mystery == 1:
				curScore += 2
			if t.romantic == 1 and cur.romantic == 1:
				curScore += 2
			if t.scifi == 1 and cur.scifi == 1:
				curScore += 2
			if t.short == 1 and cur.short == 1:
				curScore += 2
			if t.sport == 1 and cur.sport == 1:
				curScore += 2
			if t.thiller == 1 and cur.thiller == 1:
				curScore += 2
			if t.war == 1 and cur.war == 1:
				curScore += 2
			if t.western == 1 and cur.western == 1:
				curScore += 2
			scores.append(curScore)
		allScores.append(scores)

	# allScores is filled
	newScores = []
	for row in allScores:
		newScores.append(sum(row))

	maxscore = -5
	maxi = 0
	for i in range(len(newScores)):
		if (newScores[i] > maxscore and allMovies[i] not in movies):
			maxi = i
			maxscore = newScores[i]

	return allMovies[maxi]"""
		
