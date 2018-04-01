import objects as obj

def recommendation(movies, allMovies):
	#movies in an array of movies that the user has rated
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
				if cur.rating = topRating:
					topten.append(cur)
			topRating -= 1
	#topten now had users top ten rated movies

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

	for scores in allScores:
		
		
