import os
import time

from flask import request
from flask import Flask, render_template, jsonify
import pyodbc 

application = Flask(__name__)
app = application


def get_db_creds():
#     db = os.environ.get("DB", None)
#     username = os.environ.get("USER", None)
#     password = os.environ.get("PASSWORD", None)
#     hostname = os.environ.get("HOST", None)
    db, username, password, hostname = "HackTX2018", "Hacktx", "Password1234", "hacktx2018.database.windows.net"
    return db, username, password, hostname


def create_table():
    # Check if table exists or not. Create and populate it only if it does not exist.
    # db, username, password, hostname = get_db_creds()
    table_ddl = 'DROP TABLE if exists movies; CREATE TABLE movies(id INT NOT NULL, year INT, title VARCHAR, director VARCHAR, actor VARCHAR, release_date CHAR, rating REAL, PRIMARY KEY (id))'

    cnx = ''
    try:
        cnx = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};Server=tcp:hacktx2018.database.windows.net,1433;Database=HackTX2018;Uid=hacktx@hacktx2018;Pwd=Password1234;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
    except Exception as exp:
        print(exp)

    cur = cnx.cursor()

    # try:
    cur.execute(table_ddl)
    cnx.commit()
    # except mysql.connector.Error as err:
    #     if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
    #         print("already exists.")
    #     else:
    #         print(err.msg)


@app.route('/add_movie', methods=['POST'])
def add_movie():
    print("Received request.")
    print(request.form['title'])
    year = request.form['year']
    title = request.form['title'].upper()
    director = request.form['director'].upper()
    actor = request.form['actor'].upper()
    release_date = request.form['release_date']
    rating = request.form['rating']

    db, username, password, hostname = get_db_creds()

    cnx = ''
    try:
        cnx = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};Server=tcp:hacktx2018.database.windows.net,1433;Database=HackTX2018;Uid=hacktx@hacktx2018;Pwd=Password1234;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
    except Exception as exp:
        print(exp)

    cur = cnx.cursor()
    messages = []
    try:
        cur.execute("SELECT * FROM movies WHERE title='" + title + "'")
        # movie already in db
        if len(cur.fetchall()) > 0:
            message = ('Movie %s already in database. Please use Update Movie to edit movie.' % (title))
            messages.append(dict(message=message))
        # insert movie
        else:
            cur.execute("INSERT INTO movies (year, title, director, actor, release_date, rating) values ('" + year + "', '" + title + "', '" + director + "', '" + actor + "', '" + release_date + "', '" + rating + "')")
            message = ('Movie %s successfully inserted' % (title))
            messages.append(dict(message=message))
        cnx.commit()
    except Exception as exp:
        message = ('Movie %s could not be inserted - %s' % (title, exp))
        messages.append(dict(message=message))

    return hello(messages)

@app.route('/update_movie', methods=['POST'])
def update_movie():
    print("Received request.")
    print(request.form['title'])
    year = request.form['year']
    title = request.form['title'].upper()
    director = request.form['director'].upper()
    actor = request.form['actor'].upper()
    release_date = request.form['release_date']
    rating = request.form['rating']

    db, username, password, hostname = get_db_creds()

    cnx = ''
    try:
        cnx = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};Server=tcp:hacktx2018.database.windows.net,1433;Database=HackTX2018;Uid=hacktx@hacktx2018;Pwd=Password1234;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
    except Exception as exp:
        print(exp)

    cur = cnx.cursor()
    messages = []
    try:
        cur.execute("SELECT * FROM movies WHERE title='" + title + "'")
        # update movie
        if len(cur.fetchall()) > 0:
            cur.execute("UPDATE movies SET year='" + year + "', director='" + director + "', actor='" + actor + "', release_date='" + release_date + "', rating='" + rating + "' WHERE title='" + title + "'")
            message = ('Movie %s successfully updated ' % (title))
            messages.append(dict(message=message))
        # movie doesn't exist
        else:
            message = ('Movie with title %s does not exist' % (title))
            messages.append(dict(message=message))
        cnx.commit()
    except Exception as exp:
        message = ('Movie %s could not be inserted - %s' % (title, exp))
        messages.append(dict(message=message))

    return hello(messages)
@app.route('/delete_movie', methods=['POST'])
def delete_movie():
    print("Received request.")
    print(request.form['delete_title'])
    title = request.form['delete_title'].upper()

    db, username, password, hostname = get_db_creds()

    cnx = ''
    try:
        cnx = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};Server=tcp:hacktx2018.database.windows.net,1433;Database=HackTX2018;Uid=hacktx@hacktx2018;Pwd=Password1234;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
    except Exception as exp:
        print(exp)

    cur = cnx.cursor()
    messages = []
    try:
        cur.execute("SELECT * FROM movies WHERE title='" + title + "'")
        # delete movie
        if len(cur.fetchall()) > 0:
            cur.execute("DELETE FROM movies WHERE title='" + title + "'")
            message = ('Movie %s successfully deleted ' % (title))
            messages.append(dict(message=message))
        # movie doesn't exist
        else:
            message = ('Movie with %s does not exist' % (title))
            messages.append(dict(message=message))
        cnx.commit()
    except Exception as exp:
        message = ('Movie %s could not be deleted - %s' % (title, exp))
        messages.append(dict(message=message))
    return hello(messages)

@app.route('/search_movie', methods=['GET'])
def search_movie():
    print("Received request.")
    # print(request.form['search_actor'])
    actor = request.args.get('search_actor').upper()

    db, username, password, hostname = get_db_creds()

    cnx = ''
    try:
        cnx = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};Server=tcp:hacktx2018.database.windows.net,1433;Database=HackTX2018;Uid=hacktx@hacktx2018;Pwd=Password1234;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
    except Exception as exp:
        print(exp)

    cur = cnx.cursor()
    messages = []
    try:
        cur.execute("SELECT title, year, actor FROM movies WHERE actor='" + actor + "'")
        # search
        results = cur.fetchall()
        if len(results) > 0:
            messages = [dict(message=("Title: " + str(row[0]) + ", Year: " + str(row[1]) + ", Actor: " + str(row[2]))) for row in results]
        # movies with actor doesn't exist
        else:
            message = ('No movies found for actor %s' % (actor))
            messages.append(dict(message=message))
        cnx.commit()
    except Exception as exp:
        message = ('Serching failed - %s' % (exp))
        messages.append(dict(message=message))
    return hello(messages)

@app.route('/highest_rating', methods=['GET'])
def highest_rating():
    print("Received request.")

    db, username, password, hostname = get_db_creds()

    cnx = ''
    try:
        cnx = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};Server=tcp:hacktx2018.database.windows.net,1433;Database=HackTX2018;Uid=hacktx@hacktx2018;Pwd=Password1234;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
    except Exception as exp:
        print(exp)

    cur = cnx.cursor()
    messages = []
    try:
        # highest rating
        cur.execute("SELECT title, year, actor, director, rating FROM movies WHERE rating=(SELECT max(rating) FROM movies)")
        results = cur.fetchall()
        if len(results) == 0:
            message = ('No movies in database. Please insert some movies first.')
            messages.append(dict(message=message))
            return hello(messages)
        messages = [dict(message=("Title: " + str(row[0]) + ", Year: " + str(row[1]) + ", Actor: " + str(row[2]) + ", Director: " + str(row[3]) + ", Rating: " + str(row[4]))) for row in results]
        cnx.commit()
    except Exception as exp:
        message = ('Request failed - %s' % (exp))
        messages.append(dict(message=message))
    return hello(messages)

@app.route('/lowest_rating', methods=['GET'])
def lowest_rating():
    print("Received request.")

    db, username, password, hostname = get_db_creds()

    cnx = ''
    try:
        cnx = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};Server=tcp:hacktx2018.database.windows.net,1433;Database=HackTX2018;Uid=hacktx@hacktx2018;Pwd=Password1234;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
    except Exception as exp:
        print(exp)

    cur = cnx.cursor()
    messages = []
    try:
        # lowest rating
        cur.execute("SELECT title, year, actor, director, rating FROM movies WHERE rating=(SELECT min(rating) FROM movies)")
        results = cur.fetchall()
        if len(results) == 0:
            message = ('No movies in database. Please insert some movies first.')
            messages.append(dict(message=message))
            return hello(messages)
        messages = [dict(message=("Title: " + str(row[0]) + ", Year: " + str(row[1]) + ", Actor: " + str(row[2]) + ", Director: " + str(row[3]) + ", Rating: " + str(row[4]))) for row in results]
        cnx.commit()
    except Exception as exp:
        message = ('Request failed - %s' % (exp))
        messages.append(dict(message=message))
    return hello(messages)


@app.route("/")
def hello(messages=""):
    print("Printing available environment variables")
    print(os.environ)
    print("Before displaying index.html")
    create_table()
    return render_template('index.html', messages=messages)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
