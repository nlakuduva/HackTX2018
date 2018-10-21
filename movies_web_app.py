import os
import time

from flask import request
from flask import Flask, render_template, jsonify
import pyodbc 

application = Flask(__name__)
app = application


def get_db_creds():
    db, username, password, hostname = "HackTX2018", "Hacktx", "Password1234", "hacktx2018.database.windows.net"
    return db, username, password, hostname

def create_table():
    # Check if table exists or not. Create and populate it only if it does not exist.
    table_ddl = 'CREATE TABLE entrepreneurs(name VARCHAR, value INT, shares INT)'
    table_ddl2 = 'CREATE TABLE funders(name VARCHAR)'
    table_ddl2 = 'CREATE TABLE purchases(fund_name VARCHAR, entr_name VARCHAR, num_shares INT)'

    cnx = ''
    try:
        cnx = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};Server=tcp:hacktx2018.database.windows.net,1433;Database=HackTX2018;Uid=hacktx@hacktx2018;Pwd=Password1234;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
    except Exception as exp:
        print(exp)

    cur = cnx.cursor()
    print("CONNECTED IN CREATE TABLE")

    try:
        cur.execute(table_ddl)
    except Exception as exp:
        print(exp)

    print("EXECUTED IN CREATE TABLE")

    cnx.commit()


@app.route('/add_user', methods=['POST'])
def add_user():
    print("Received request.")
    # print(request.form['name'])
    name = str(request.form['name'])
    value = str(request.form['value'])
    shares = str(request.form['shares'])
    print(name, value, shares)

    cnx = ''
    try:
        cnx = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};Server=tcp:hacktx2018.database.windows.net,1433;Database=HackTX2018;Uid=hacktx@hacktx2018;Pwd=Password1234;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
    except Exception as exp:
        print(exp)

    print("PAST CONNECTION")

    cur = cnx.cursor()
    messages = []
    try:
        print("START")
        cur.execute("SELECT * FROM entrepreneurs WHERE CONVERT(VARCHAR, name)='" + name + "'")
        print("CHECKING IF EXISTS")
        # user already in db
        if len(cur.fetchall()) > 0:
            message = ('User %s already in database. Please use Update user to edit user.' % (name))
            messages.append(dict(message=message))
        # user user
        else:
            print("INSERTING user")
            cur.execute("INSERT INTO entrepreneurs (name, value, shares) values ('" + name + "', '" + value + "', '" + shares + "')")
            message = ('User %s successfully inserted' % (name))
            messages.append(dict(message=message))
        cnx.commit()
    except Exception as exp:
        message = ('User %s could not be inserted - %s' % (name, exp))
        messages.append(dict(message=message))

    print("DONE")
    return hello(messages)

@app.route('/add_funder', methods=['POST'])
def add_funder():
    print("Received request.")
    # print(request.form['name'])
    name = str(request.form['name'])
    print(name)

    cnx = ''
    try:
        cnx = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};Server=tcp:hacktx2018.database.windows.net,1433;Database=HackTX2018;Uid=hacktx@hacktx2018;Pwd=Password1234;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
    except Exception as exp:
        print(exp)

    print("PAST CONNECTION")

    cur = cnx.cursor()
    messages = []
    try:
        print("START")
        cur.execute("SELECT * FROM funders WHERE CONVERT(VARCHAR, name)='" + name + "'")
        print("CHECKING IF EXISTS")
        # user already in db
        if len(cur.fetchall()) > 0:
            message = ('User %s already in database. Please use Update user to edit user.' % (name))
            messages.append(dict(message=message))
        # user user
        else:
            print("INSERTING user")
            cur.execute("INSERT INTO funders (name) values ('" + name + "')")
            message = ('User %s successfully inserted' % (name))
            messages.append(dict(message=message))
        cnx.commit()
    except Exception as exp:
        message = ('User %s could not be inserted - %s' % (name, exp))
        messages.append(dict(message=message))

    print("DONE")
    return hello(messages)

@app.route('/update_user', methods=['POST'])
def update_user():
    print("Received request.")
    name = request.form['name']
    value = request.form['value']
    shares = request.form['shares']

    db, username, password, hostname = get_db_creds()

    cnx = ''
    try:
        cnx = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};Server=tcp:hacktx2018.database.windows.net,1433;Database=HackTX2018;Uid=hacktx@hacktx2018;Pwd=Password1234;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
    except Exception as exp:
        print(exp)

    cur = cnx.cursor()
    messages = []
    try:
        cur.execute("SELECT * FROM entrepreneurs WHERE CONVERT(VARCHAR, name)='" + name + "'")
        # update user
        if len(cur.fetchall()) > 0:
            cur.execute("UPDATE entrepreneurs SET year='" + year + "', director='" + director + "', actor='" + actor + "', release_date='" + release_date + "', rating='" + rating + "' WHERE name='" + name + "'")
            message = ('user %s successfully updated ' % (name))
            messages.append(dict(message=message))
        # user doesn't exist
        else:
            message = ('user with name %s does not exist' % (name))
            messages.append(dict(message=message))
        cnx.commit()
    except Exception as exp:
        message = ('user %s could not be inserted - %s' % (name, exp))
        messages.append(dict(message=message))

    return hello(messages)
@app.route('/delete_user', methods=['POST'])
def delete_user():
    print("Received request.")
    print(request.form['delete_name'])
    name = request.form['delete_name']

    db, username, password, hostname = get_db_creds()

    cnx = ''
    try:
        cnx = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};Server=tcp:hacktx2018.database.windows.net,1433;Database=HackTX2018;Uid=hacktx@hacktx2018;Pwd=Password1234;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
    except Exception as exp:
        print(exp)

    cur = cnx.cursor()
    messages = []
    try:
        print("DELETE START")
        cur.execute("SELECT * FROM entrepreneurs WHERE CONVERT(VARCHAR, name)='" + name + "'")
        # delete user
        if len(cur.fetchall()) > 0:
            cur.execute("DELETE FROM entrepreneurs WHERE CONVERT(VARCHAR, name)='" + name + "'")
            message = ('user %s successfully deleted ' % (name))
            messages.append(dict(message=message))
        # user doesn't exist
        else:
            message = ('user with %s does not exist' % (name))
            messages.append(dict(message=message))
        cnx.commit()
    except Exception as exp:
        message = ('user %s could not be deleted - %s' % (name, exp))
        messages.append(dict(message=message))
    return hello(messages)
@app.route('/delete_funder', methods=['POST'])
def delete_funder():
    print("Received request.")
    print(request.form['delete_name'])
    name = request.form['delete_name']

    db, username, password, hostname = get_db_creds()

    cnx = ''
    try:
        cnx = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};Server=tcp:hacktx2018.database.windows.net,1433;Database=HackTX2018;Uid=hacktx@hacktx2018;Pwd=Password1234;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
    except Exception as exp:
        print(exp)

    cur = cnx.cursor()
    messages = []
    try:
        print("DELETE START")
        cur.execute("SELECT * FROM funders WHERE CONVERT(VARCHAR, name)='" + name + "'")
        # delete user
        if len(cur.fetchall()) > 0:
            cur.execute("DELETE FROM funders WHERE CONVERT(VARCHAR, name)='" + name + "'")
            message = ('user %s successfully deleted ' % (name))
            messages.append(dict(message=message))
        # user doesn't exist
        else:
            message = ('user with %s does not exist' % (name))
            messages.append(dict(message=message))
        cnx.commit()
    except Exception as exp:
        message = ('user %s could not be deleted - %s' % (name, exp))
        messages.append(dict(message=message))
    return hello(messages)


@app.route('/search_user', methods=['GET'])
def search_user():
    print("Received request.")
    user = request.args.get('search_user').upper()

    db, username, password, hostname = get_db_creds()

    cnx = ''
    try:
        cnx = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};Server=tcp:hacktx2018.database.windows.net,1433;Database=HackTX2018;Uid=hacktx@hacktx2018;Pwd=Password1234;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
    except Exception as exp:
        print(exp)

    cur = cnx.cursor()
    messages = []
    try:
        cur.execute("SELECT name, value, shares FROM entrepreneurs WHERE CONVERT(VARCHAR, name)='" + user + "'")
        # search
        results = cur.fetchall()
        if len(results) > 0:
            messages = [dict(message=("Name: " + str(row[0]) + ", Company Value: " + str(row[1]) + ", Number of Shares: " + str(row[2]) + ", Price Per Share: $ " + str(int(row[1])/int(row[2])))) for row in results]
        # entrepreneurs with actor doesn't exist
        else:
            message = ('No entrepreneurs found for user %s' % (user))
            messages.append(dict(message=message))
        cnx.commit()
    except Exception as exp:
        message = ('Serching failed - %s' % (exp))
        messages.append(dict(message=message))
    return hello(messages)

@app.route('/search_funder', methods=['GET'])
def search_funder():
    print("Received request.")
    user = request.args.get('search_user').upper()

    db, username, password, hostname = get_db_creds()

    cnx = ''
    try:
        cnx = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};Server=tcp:hacktx2018.database.windows.net,1433;Database=HackTX2018;Uid=hacktx@hacktx2018;Pwd=Password1234;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
    except Exception as exp:
        print(exp)

    cur = cnx.cursor()
    messages = []
    try:
        cur.execute("SELECT name FROM funders WHERE CONVERT(VARCHAR, name)='" + user + "'")
        # search
        results = cur.fetchall()
        if len(results) > 0:
            messages = [dict(message=("Name: " + str(row[0]))) for row in results]
        # entrepreneurs with actor doesn't exist
        else:
            message = ('No funders found for user %s' % (user))
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
        cur.execute("SELECT name, year, actor, director, rating FROM entrepreneurs WHERE rating=(SELECT max(rating) FROM entrepreneurs)")
        results = cur.fetchall()
        if len(results) == 0:
            message = ('No entrepreneurs in database. Please insert some entrepreneurs first.')
            messages.append(dict(message=message))
            return hello(messages)
        messages = [dict(message=("name: " + str(row[0]) + ", Year: " + str(row[1]) + ", Actor: " + str(row[2]) + ", Director: " + str(row[3]) + ", Rating: " + str(row[4]))) for row in results]
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
        cur.execute("SELECT name, year, actor, director, rating FROM entrepreneurs WHERE rating=(SELECT min(rating) FROM entrepreneurs)")
        results = cur.fetchall()
        if len(results) == 0:
            message = ('No entrepreneurs in database. Please insert some entrepreneurs first.')
            messages.append(dict(message=message))
            return hello(messages)
        messages = [dict(message=("name: " + str(row[0]) + ", Year: " + str(row[1]) + ", Actor: " + str(row[2]) + ", Director: " + str(row[3]) + ", Rating: " + str(row[4]))) for row in results]
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
