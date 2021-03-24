# Imports
import os
import json
from flask import Flask, render_template, request,redirect,make_response,session
from flask_mysqldb import MySQL
from flask_mail import Mail, Message

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# Variables
app = Flask(__name__)
# Connects to the database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'comsc'
app.config['MYSQL_DB'] = 'imageoptim'
app.config['MAIL_SERVER']='smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'group11IMAGEOPTIM@outlook.com'
app.config['MAIL_PASSWORD'] = '1m@g30ptim'
app.config["MAIL_USE_SSL:1123"] = True
app.config["MAIL_USE_TLS"] = True

mail = Mail(app)
mysql = MySQL(app)

#Webpage Routes
@app.route("/")
def homePage():
    return render_template('home.html', title = "Home", licences = readFromDatabaseUsingStoredProcedures("getListOfLicence()"))

@app.route("/checkout")
def customerPage():
    if 'tier' in session and 'length' in session:
        return render_template('customer.html', title = "Customer Details", countries = readFromDatabaseUsingStoredProcedures("getCountries()"))
    else:
        return render_template('checkoutWarning.html', title = "Checkout")

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

def purchaseConfirmationPage():
    return render_template('purchase_confirmation.html', title = "Purchase Confirmation")

@app.route("/remove")
def removeFromBasket():
     session.pop('tier', None)
     session.pop('length', None)
     return redirect('/basket')


# Reading forms.
@app.route("/gatherCustomerData", methods=['POST'])
def customerForm():
    print("Requesting data")
    if request.method == 'POST':
        name = request.form['name']
        contactPerson = request.form['nameOfContactPerson']
        email = request.form['email']
        street = request.form['street']
        city = request.form['city']
        postcode =request.form['postcode']
        country =request.form['countries']
        vatNumber =request.form['vatNumber']
        id = attemptToWriteToDatabaseUsingFunction(name, street, city, postcode,country,email,contactPerson,vatNumber)
        writePurchaseIntoDatabase(id)
        callItem = "getBasketDetails(" + session.get('tier') +","+ session.get('length') + ")"
        sentEmail(email, contactPerson, readFromDatabaseUsingStoredProcedures(callItem))
        session.pop('tier', None)
        session.pop('length', None)
        return purchaseConfirmationPage()
    return "Recorded purchase"

@app.route("/gatherLicenceData", methods=['POST'])
def licenceForm():
    if request.method == 'POST':
        session['tier'] =  request.form['tier']
        session['length'] = request.form['length']
    return redirect('/basket')

# Example connection to the database
def attemptToWriteToDatabaseUsingFunction(name, street, city, postcode,country,email,contactPerson,vatNumber):
    cur = mysql.connection.cursor()
    cur.execute("SELECT createCustomer(%s,%s,%s,%s,%s,%s,%s,%s) as 'ID Number';", (name, street, city, postcode,country,email,contactPerson,vatNumber))
    mysql.connection.commit()
    data = cur.fetchall()
    cur.close()
    return data

def writePurchaseIntoDatabase(customerID):
    cur = mysql.connection.cursor()
    cur.execute("CALL recordPurchase(%s,%s,%s);", (session.get('tier'), session.get('length'), customerID))
    mysql.connection.commit()
    data = cur.fetchall()
    cur.close()
    print(data)

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

def sentEmail(recipient,name, body):
    msg = Message(subject='Confirmation Email',sender='group11IMAGEOPTIM@outlook.com', recipients = [recipient])
    msg.html = render_template('emailConfirmation.html',basket = body, name = name)
    with app.open_resource('static\invoice\invoice.pdf') as fp:
        msg.attach('invoice.pdf', "invoice/pdf", fp.read())
    # with app.open_resource('static\contract\contract.pdf') as fp:
    #     msg.attach('contract.pdf', "contract/pdf", fp.read())
    mail.send(msg)

if __name__ == "__main__":
    app.secret_key = 'fj590Rt?h40gg'
    app.run(debug=True)
