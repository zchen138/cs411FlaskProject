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
