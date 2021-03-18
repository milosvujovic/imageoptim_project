# Imports
import os
import json
from flask import Flask, render_template, request
from flask_mysqldb import MySQL

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# Variables
app = Flask(__name__)
# Connects to the database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'comsc'
app.config['MYSQL_DB'] = 'imageoptim'

mysql = MySQL(app)



#Webpage Routes
@app.route("/")
def defaultPage():
    return "Default Page"


# Example connection to the database
def attemptToReadFromDatabase():
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tier(idTier, type) VALUES (%s, %s)", (4, "global company"))
        mysql.connection.commit()
        cur.close()



if __name__ == "__main__":
    app.run(debug=True)
