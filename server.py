# Imports
import os
import json
from flask import Flask, render_template, request,redirect,make_response,session
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

@app.route("/checkout")
def customerPage():
    if 'tier' in session and 'length' in session:
    return render_template('customer.html', title = "Customer Details", countries = readFromDatabaseUsingStoredProcedures("getCountries()"))
    else:
        return render_template('checkoutWarning.html', title = "Checkout")

@app.route("/purchase/confirmation")
def purchaseConfirmationPage():
    print("Loading page")
    return render_template('purchase_confirmation.html', title = "Purchase Confirmation")

@app.route("/licence/<licenceID>")
def selectLicence(licenceID):
    callTiers = "getTiersForLicence("+licenceID+")"
    callLengths = "getLengthOfLicences("+licenceID+")"
    return render_template('licence.html', title = "Licence", tiers = readFromDatabaseUsingStoredProcedures(callTiers), lengths= readFromDatabaseUsingStoredProcedures(callLengths))

@app.route("/basket")
def basketPage():
    if 'tier' in session and 'length' in session:
        callItem = "getBasketDetails(" + session.get('tier') +","+ session.get('length') + ")"
        return render_template('basket.html', title = "Basket", basket =  readFromDatabaseUsingStoredProcedures(callItem), size = 1)
    else:
        return render_template('basket.html', title = "Basket", basket =  [], size = 0)

@app.route("/remove")
def removeFromBasket():
     session.pop('tier', None)
     session.pop('length', None)
     return redirect('/basket')

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

@app.route("/gatherLicenceData", methods=['POST'])
def licenceForm():
    if request.method == 'POST':
        session['tier'] =  request.form['tier']
        session['length'] = request.form['length']
    testSession()
    return redirect('/basket')

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

def testSession():
    print(session.get('tier'))
    print(session.get('length'))

if __name__ == "__main__":
    app.secret_key = 'fj590Rt?h40gg'
    app.run(debug=True)
