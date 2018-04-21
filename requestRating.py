import math


def requestRating(_userid, _targetMovie, cur):
    predictedScore = 0
    denom = 0

    sqlStr = "SELECT * FROM rated WHERE userid = %s"
    cur.execute(sqlStr, [_userid])
    userAvg = 0
    userCt = 0

    for rating in cur.fetchall():
        userAvg = userAvg + rating[2]
        userCt = userCt + 1

    if userCt == 0:
        return -1
    userAvg = userAvg / userCt  # Determine the user's average rating

    sqlStr = "SELECT * FROM users WHERE userid <> %s"
    cur.execute(sqlStr, [_userid])

    otherUsers = cur.fetchall()
    for otherUser in otherUsers:  # Go through each other user in the database
        _otherid = otherUser[0]
        otherTargetRating = 0

        sqlStr = "SELECT * FROM rated WHERE userid = %s AND movieid = %s"
        cur.execute(sqlStr, (_otherid, _targetMovie))
        if cur.rowcount == 0:
            continue  # We are only interested in others who have rated this movie
        else:
            otherTargetRating = cur.fetchone()[2]

        sqlStr = "SELECT * FROM rated WHERE userid = %s"
        cur.execute(sqlStr, [_otherid])

        otherAvg = 0
        otherCt = 0
        for rating in cur.fetchall():
            otherAvg = otherAvg + rating[2]
            otherCt = otherCt + 1
        otherAvg = otherAvg / otherCt  # Determine the other user's average rating

        sqlStr = "SELECT * FROM rated WHERE userid = %s AND movieid IN (SELECT movieid FROM rated WHERE userid = %s)"
        cur.execute(sqlStr, (_userid, _otherid))  # Find the movies that both users liked
        sumProductDifferences = 0
        sumSquaredDiffUser = 0
        sumSquaredDiffOther = 0

        for rating in cur.fetchall():
            sharedMovie = rating[1]
            userRating = rating[2]
            otherRating = 0

            sqlStr = "SELECT * FROM rated WHERE userid = %s AND movieid = %s"
            cur.execute(sqlStr, (_otherid, sharedMovie))
            otherRating = cur.fetchone()[2]

            sumProductDifferences = diffSquareAdder(sumProductDifferences, userRating, userAvg, otherRating, otherAvg)
            sumSquaredDiffUser = diffSquareAdder(sumSquaredDiffUser, userRating, userAvg, userRating, userAvg)
            sumSquaredDiffOther = diffSquareAdder(sumSquaredDiffOther, otherRating, otherAvg, otherRating, otherAvg)

        if math.sqrt(sumSquaredDiffUser * sumSquaredDiffOther) == 0:
            return -1
        pearsonCoeff = sumProductDifferences / math.sqrt(sumSquaredDiffUser * sumSquaredDiffOther)
        if pearsonCoeff != 0:
            predictedScore = predictedScore + ((otherTargetRating - otherAvg) * pearsonCoeff)
            denom = denom + pearsonCoeff

    if predictedScore != 0:
        predictedScore = userAvg + (predictedScore / denom)  # Calculate the total predicted score based on deviations
    else:
        predictedScore = userAvg  # Default value if no related data can be found

    return truncate(predictedScore, 2)


def diffSquareAdder(sumarg, rating1, avg1, rating2, avg2):
    return sumarg + ((rating1 - avg1) * (rating2 - avg2))


def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    '''Source: https://stackoverflow.com/questions/783897/truncating-floats-in-python'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d + '0' * n)[:n]])