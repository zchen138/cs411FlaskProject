import csv
from unidecode import unidecode

def getMainGenre(items):
    genreList = ["actionMovie", "adult", "adventure", "animation", "biography", "comedy", "crime", "documentary", "drama", "family", "fantasy", "filmNoir", "history", "horror", "mystery", "romance", "SciFi", "short", "sport","thriller", "war", "western"]
    for i in range (16, 38):
        if items[i]!="0":
            return genreList[i-16]


def convertSecondsToMinutes(seconds):
    intSec = int(seconds)
    intMin = intSec/60
    return str(int(intMin))

output_file = open('newMovieInfo.txt', 'w')
with open("imdbmovies.csv", "r") as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    i = 0
    while (i<100732):#100732):
        i += 1
        try:
            items = next(reader)
            pline = "INSERT INTO moviedata(movieid, title, releaseYear, runtime, rating, numRatings, " + "numWins, numGenres, genre, actionMovie, adult, adventure, animation, biography, "
            pline = pline + "comedy, crime, documentary, drama, family, fantasy, filmNoir, "
            pline = pline +  "history, horror, mystery, romance, SciFi, short, sport, "
            pline = pline + "thriller, war, western) VALUES ("
            pline = pline + str(i) + ", "
            titleStr = (items[2][:-6])
            titleStr = bytes(titleStr, 'utf-8').decode('utf-8', 'ignore')
            titleStr = unidecode(titleStr)
            titleStr = titleStr.replace("\"", "")
            titleStr = titleStr.replace("<", "")
            pline = pline + "\"" + titleStr + "\" "
            pline = pline +  ", " + items[8] + ", " + convertSecondsToMinutes(items[7]) +  ", " + items[5] + ", " + items[6]
            pline = pline + ", " + items[10] + ", " + items[15] +", " + "\"" + getMainGenre(items) +"\""

            pline = pline + ", " + items[16] + ", " + items[17] + ", " + items[18] + ", " + items[19] + ", " + items[20] + ", " + items[21] + ", " + items[22] + ", " + items[23] + ", " + items[24] + ", " + items[25] + ", " + items[26] + ", " + items[27] + ", " + items[28] + ", " + items[29] + ", " + items[30] + ", " + items[31] + ", " + items[32] + ", " + items[33] + ", " + items[34] + ", " + items[35] + ", " + items[36] + ", " + items[37]
            pline = pline + ");\n"
            #print(pline)
            output_file.write(pline)
        except:
            continue

'''
if items[1] == '\\N' and items[2] == '\\N':
    output_file.write("INSERT INTO movieinfo(title, releaseYear, runtime, genre) VALUES (\"" + items[0] + "\", " + items[1] + "")
elif items[1] == '\\N':
    output_file.write("INSERT INTO movieinfo(title, releaseYear, runtime, genre) VALUES (\"" + items[0] + "\", " + items[1] + ", " + items[2] + ", \"" + items[3] + "\")\n")
elif items[2] == '\\N':
    output_file.write("INSERT INTO movieinfo(title, releaseYear, runtime, genre) VALUES (\"" + items[0] + "\", " + items[1] + ", " + items[2] + ", \"" + items[3] + "\")\n")
else:
    output_file.write("INSERT INTO movieinfo(title, releaseYear, runtime, genre) VALUES (\"" + items[0] + "\", " + items[1] + ", " + items[2] + ", \"" + items[3] + "\")\n")
'''
'''
input_file = open('data.tsv','r')
output_file = open('formattedMovies.txt','w')

flag = True
while(flag):
    try:
        line = input_file.readline()
        if(line==""):
            flag = False
        items = line.split("\t")
        if (items[1] == "movie"):
            genres = items[8].split(",")
            newline = ''
            newline = newline + items[2]+'\t'
            newline = newline + items[5]+'\t'
            newline = newline + items[7]+'\t'
            newline = newline + genres[0]
            if (newline.endswith('\n')!=True):
                newline = newline + '\n'
            output_file.write(newline)

    except:
        continue
'''


'''
input_file = open('formattedMovies.txt','r')
output_file = open('movieUploadSQL.txt', 'w')

i = 0

while(i < 3000):
    line = input_file.readline()
    if line == "":
        break
    items = line.split('\t')
    if items[0] == "\\N":
        items[0] = "NULL"
    if items[3] == "\\N":
        items[3] = "NULL"
    if items[3].endswith('\n'):
        items[3] = items[3][:-1]
    if items[1] != "\\N":
        if int(items[1]) == 2018:
            combined = "\"" + items[0] + "\","
            if items[1] == '\\N' and items[2] == '\\N':
                combined = combined + "NULL,NULL"
            elif items[1] == '\\N':
                combined = combined + "NULL," + items[2]
            elif items[2] == '\\N':
                combined = combined + items[1] + ",NULL"
            else:
                combined = combined + items[1] + "," + items[2]

            if items[3] == "\\N":
                combined = combined + ",NULL"
            else:
                combined = combined + ",\"" + items[3] + "\""
            output_file.write("INSERT INTO heroku_37da5348cc1f7c7" +"."+"movieinfo(title, releaseYear, runtime, genre) VALUES (" + combined + ");\n")
            i = i + 1

'''
#if items[1] == '\\N' and items[2] == '\\N':
 #   output_file.write("INSERT INTO movieinfo(title, releaseYear, runtime, genre) VALUES (\"" + items[0] + "\", " + items[1] + "")
#elif items[1] == '\\N':
#    output_file.write("INSERT INTO movieinfo(title, releaseYear, runtime, genre) VALUES (\"" + items[0] + "\", " + items[1] + ", " + items[2] + ", \"" + items[3] + "\")\n")
#elif items[2] == '\\N':
#    output_file.write("INSERT INTO movieinfo(title, releaseYear, runtime, genre) VALUES (\"" + items[0] + "\", " + items[1] + ", " + items[2] + ", \"" + items[3] + "\")\n")
#else:
 #   output_file.write("INSERT INTO movieinfo(title, releaseYear, runtime, genre) VALUES (\"" + items[0] + "\", " + items[1] + ", " + items[2] + ", \"" + items[3] + "\")\n")
