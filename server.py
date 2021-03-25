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
# Email settings
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
    print("home")
    print(session['basket'])
    return render_template('home.html', title = "Home", licences = readFromDatabaseUsingStoredProcedures("getListOfLicence()"))

# Displays checkout page asking for users details.
@app.route("/checkout")
def customerPage():
    print("checkout")
    print(session['basket'])
    if 'tier' in session and 'length' in session:
        return render_template('customer.html', title = "Customer Details", countries = readFromDatabaseUsingStoredProcedures("getCountries()"))
    else:
        return render_template('checkoutWarning.html', title = "Checkout")

# Displays page with options to select a licence
@app.route("/licence/<licenceID>")
def selectLicence(licenceID):
    print("licence page")
    print(session['basket'])
    callTiers = "getTiersForLicence("+licenceID+")"
    callLengths = "getLengthOfLicences("+licenceID+")"
    return render_template('licence.html', title = "Licence", tiers = readFromDatabaseUsingStoredProcedures(callTiers), lengths= readFromDatabaseUsingStoredProcedures(callLengths),licenceID =licenceID)

# Displays basket page.
# Having read the details about each item from the database.
@app.route("/basket")
def basketPage():
    return (session['basket'])
    # print(session['basket'])
    # print(len(session['basket']))
    # if  len(session['basket']) > 0:
    #     price = 0
    #     basketList = []
    #
    #     for item in session['basket'].values():
    #         print(item)
    #         # callItem = "getBasketDetails(" +item.get('tier')  +","+ item.get('length') + ")"
    #         # holder = readFromDatabaseUsingStoredProcedures(callItem)
    #         # basketList.append(holder[0])
    #         # price = holder[0][4] + price
    #     return render_template('basket.html', title = "Basket", basket =  basketList, size = 1, price = price)
    # else:
    #     return render_template('basket.html', title = "Basket", basket =  [], size = 0, price = 0)

# Displays purchase confirmation page
def purchaseConfirmationPage():
    return render_template('purchase_confirmation.html', title = "Purchase Confirmation")

@app.route("/remove")
def removeFromBasket():
    # Removes everything from the basket and redirects them to the basket
     session.clear()
     return homePage()


# Reading forms.
@app.route("/gatherCustomerData", methods=['POST'])
def customerForm():
    print("Requesting data")
    if request.method == 'POST':
        # Stores the customer details in a dictionary in the server session storage
        session['customer'] = {}
        session['customer']['name'] = request.form['name']
        session['customer']['nameOfContactPerson'] = request.form['nameOfContactPerson']
        session['customer']['email'] = request.form['email']
        session['customer']['street'] = request.form['street']
        session['customer']['city'] = request.form['city']
        session['customer']['country'] = request.form['countries']
        session['customer']['postcode'] = request.form['postcode']
        session['customer']['vatNumber'] = request.form['vatNumber']
        # Calls function to process transactions
        return processTransaction()
    return "Error with form"

@app.route("/gatherLicenceData", methods=['POST'])
def licenceForm():
    if request.method == 'POST':
        print("beforehand")
        print(session['basket'])
        session['basket'][request.form['licenceID']] = {'tier' :  request.form['tier'],  'length' :request.form['length']}
        print("afterwards")
        print(session['basket'])
    return homePage()

# Database Functions
def writeToDatabaseWithCustomerDetails(name, street, city, postcode,country,email,contactPerson,vatNumber):
    # Writes to the database with details of the customer
    cur = mysql.connection.cursor()
    cur.execute("SELECT createCustomer(%s,%s,%s,%s,%s,%s,%s,%s) as 'ID Number';", (name, street, city, postcode,country,email,contactPerson,vatNumber))
    mysql.connection.commit()
    data = cur.fetchall()
    cur.close()
    return data

def writePurchaseIntoDatabase(customerID):
    # Writes to the database with details of the purchase
    cur = mysql.connection.cursor()
    cur.execute("CALL recordPurchase(%s,%s,%s);", (session.get('tier'), session.get('length'), customerID))
    mysql.connection.commit()
    data = cur.fetchall()
    cur.close()

def readFromDatabaseUsingStoredProcedures(function):
        command = "CALL " + function +";"
        # print("Reading from the database")
        try:
            cur = mysql.connection.cursor()
            cur.execute(command)
            data = cur.fetchall()
            cur.close()
            # print("Succesfully from the database")
            return data
        except Exception as e:
            v =2
            # print("Error " + e)


# Functions
def sentCustomerEmail(recipient,name, body):
    # Prepares the email with the main body of the email being a html template
    msg = Message(subject='Confirmation Email',sender='group11IMAGEOPTIM@outlook.com', recipients = [recipient])
    msg.html = render_template('emailConfirmationCustomer.html',basket = body, name = name)
    # Attaches the invoice file
    with app.open_resource('static\invoice\invoice.pdf') as fp:
        msg.attach('invoice.pdf', "invoice/pdf", fp.read())
    # Attaches the contract file
    with app.open_resource('static\contract\contract.pdf') as fp:
        msg.attach('contract.pdf', "contract/pdf", fp.read())
    # Sends the email
    mail.send(msg)

def sentAdminEmail(recipient,companyName, customerName,emailAddress, body):
    # Prepares the email with the main body of the email being a html template
    recipients = [ ]
    for i in recipient:
        recipients.append(i)
    msg = Message(subject='Purchase Confirmation',sender='group11IMAGEOPTIM@outlook.com', recipients = recipients)
    msg.html = render_template('emailConfirmationAdmin.html',basket = body, customer = companyName,employeeName = customerName,emailAddress = emailAddress)
    # Attaches the contract file
    with app.open_resource('static\contract\contract.pdf') as fp:
        msg.attach('contract.pdf', "contract/pdf", fp.read())
    # Sends email
    mail.send(msg)

def processTransaction():
    # Writes the new customer to the database and returns the Id of the customer
    id = writeToDatabaseWithCustomerDetails(session.get("customer")["name"], session.get("customer")["street"], session.get("customer")["city"], session.get("customer")["postcode"],session.get("customer")["country"],session.get("customer")["email"],session.get("customer")["nameOfContactPerson"],session.get("customer")["vatNumber"])
    # Writes the details of the purchase into the database
    writePurchaseIntoDatabase(id)
    # Reads the details of the basket from the datbase to put in email
    callItem = "getBasketDetails(" + session.get('tier') +","+ session.get('length') + ")"
    basketDetails = readFromDatabaseUsingStoredProcedures(callItem)
    # Sents the email to the customer with details of their purchase
    sentCustomerEmail(session.get("customer")["email"], session.get("customer")["nameOfContactPerson"], basketDetails)
    #  Reads the email address of the admin from the datbase
    callItem = "getAdminEmail()"
    adminEmails = readFromDatabaseUsingStoredProcedures(callItem)
    # Sents email to the admin with details of the purchase
    sentAdminEmail(adminEmails[0],session.get("customer")["name"], session.get("customer")["nameOfContactPerson"],session.get("customer")["email"], basketDetails)
    # Clears the basket
    # session.pop('tier', None)
    # session.pop('length', None)
    # Redirects to confirmation page.
    return purchaseConfirmationPage()

if __name__ == "__main__":
    app.secret_key = 'fj590Rt?h40gg'
    app.run(debug=True)
    if 'basket' not in session:
        session['basket'] = {}
