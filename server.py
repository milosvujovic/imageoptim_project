# Imports
import os
import json
from flask import Flask, render_template, request,redirect,make_response
from flask_mysqldb import MySQL

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# Variables
app = Flask(__name__)
# Connects to the database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'comsc'
app.config['MYSQL_DB'] = 'imageoptim'
app.secret_key = 'fj590Rt?h40gg'

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

@app.route("/licence/<licenceID>")
def selectLicence(licenceID):
    callTiers = "getTiersForLicence("+licenceID+")"
    callLengths = "getLengthOfLicences("+licenceID+")"
    return render_template('licence.html', title = "Licence", tiers = readFromDatabaseUsingStoredProcedures(callTiers), lengths= readFromDatabaseUsingStoredProcedures(callLengths))

# @app.route("/gatherLicenceData", methods=['POST'])
# def licenceForm():
#     if request.method == 'POST':
#         resp = make_response(customerPage())
#         resp.set_cookie('tier', request.form['tier'])
#         resp.set_cookie('length', request.form['length'])
#         return resp

@app.route("/gatherCustomerData", methods=['POST'])
def customerForm():
    if request.method == 'POST':
        name = request.form['name']
        contactPerson = request.form['nameOfContactPerson']
        email = request.form['email']
        street = request.form['street']
        city = request.form['city']
        postcode =request.form['postcode']
        country =request.form['country']
        vatNumber =request.form['vatNumber']
    return "Read form"


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
