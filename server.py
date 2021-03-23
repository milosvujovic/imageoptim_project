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
def homePage():
    print("Loading page")
    return render_template('home.html', title = "Home", licences = readFromDatabaseUsingStoredProcedures("getListOfLicence()"))

@app.route("/customer")
def customerPage():
    print("Loading page")
    return render_template('customer.html', title = "Customer Details")

@app.route("/purchase/confirmation")
def purchaseConfirmationPage():
    print("Loading page")
    return render_template('purchase_confirmation.html', title = "Purchase Confirmation")

@app.route("/licence/<licenceID>")
def selectLicence(licenceID):
    callTiers = "getTiersForLicence("+licenceID+")"
    callLengths = "getLengthOfLicences("+licenceID+")"
    return render_template('licence.html', title = "Licence", tiers = readFromDatabaseUsingStoredProcedures(callTiers), lengths= readFromDatabaseUsingStoredProcedures(callLengths))

# Example connection to the database
def attemptToReadFromDatabase():
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO tier(idTier, type) VALUES (%s, %s)", (4, "global company"))
    mysql.connection.commit()
    cur.close()

def readFromDatabaseUsingStoredProcedures(function):
        command = "CALL " + function +";"
        print("Reading from the database")
        try:
            cur = mysql.connection.cursor()
            cur.execute(command)
            data = cur.fetchall()
            cur.close()
            print("Succesfully from the database")
            return data
        except Exception as e:
            print("Error " + e)

if __name__ == "__main__":
    app.run(debug=True)
