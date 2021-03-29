# Imports
import os
import json
import datetime
import functools
from flask import Flask, render_template, request,redirect,make_response,session, url_for, flash
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
from cryptography.fernet import Fernet
from datetime import timedelta


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
# session data Variables
app.secret_key = 'fj590Rt?h40gg'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

mail = Mail(app)
mysql = MySQL(app)

def customer_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
            if  'customerID' not in session:
                return "You need to access this page by the link in the email"
            print("Valid input")
            return func(*args, **kwargs)
    return secure_function

def admin_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if 'admin' not in session:
            return "You don't have access here"
            # return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)
    return secure_function

def basket_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if 'basket' not in session or len(session['basket']) == 0:
            return render_template('checkoutWarning.html', title = "Checkout")
        return func(*args, **kwargs)
    return secure_function

# Reference https://devqa.io/encrypt-decrypt-data-python/
# Sets up the key for the encryption
def generate_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    """
    Loads the key named `secret.key` from the current directory.
    """
    return open("secret.key", "rb").read()


#Webpage Routes
# User web Routes
@app.route("/")
def homePage():
    return render_template('user_home.html', title = "Home", licences = readFromDatabaseUsingStoredProcedures("getListOfLicence()"))

# Displays checkout page asking for users details.
@app.route("/checkout")
@basket_required
def customerPage():
    return render_template('user_customerDetails.html', title = "Customer Details", countries = readFromDatabaseUsingStoredProcedures("getCountries()"))

# Displays page with options to select a licence
@app.route("/licence/<licenceID>")
def selectLicence(licenceID):
    callTiers = "getTiersForLicence("+licenceID+")"
    callLengths = "getLengthOfLicences("+licenceID+")"
    # If the user has already selected a licence then gets value so that it will set the selected licence as checked.
    tier = -1
    length = -1
    if 'basket' in session:
        if licenceID in session['basket']:
            tier = int(session['basket'][licenceID]['tier'])
            length = int(session['basket'][licenceID]['length'])
    return render_template('user_licence.html', title = "Licence", tiers = readFromDatabaseUsingStoredProcedures(callTiers), lengths= readFromDatabaseUsingStoredProcedures(callLengths), licenceID = licenceID, selectedTier = tier, selectedLength = length)

# Displays basket page.
# Having read the details about each item from the database.
@app.route("/basket")
def basketPage():
        basketDetails = gatherBasketDetails()
        print(basketDetails)
        return render_template('user_basket.html', title = "Basket", basket =  basketDetails[0], size = basketDetails[2], price = basketDetails[1])

# Displays purchase confirmation page
def purchaseConfirmationPage():
    return render_template('user_purchaseConfirmation.html', title = "Purchase Confirmation")

# Removes selected item from the basket and redirects them to the basket
@app.route("/basket/remove/<licenceID>")
def removeFromBasket(licenceID):
    if 'basket' in session:
        if licenceID in session['basket']:
            session['basket'].pop(licenceID, None)
            session.modified = True
    return redirect("/basket")

    # Removes all item from the basket and redirects them to the basket
@app.route("/basket/clear")
def removeAllFromBasket():
    if 'basket' in session:
        session['basket'].clear()
        session.modified = True
    return redirect("/basket")

# Customers Web routes
# Logs  user in
@app.route("/customer/<input>")
def displayCustomerDetails(input):
    try:
        # Decodes the code in the email
        token = input.encode("utf-8")
        key = load_key()
        f = Fernet(key)
        value = f.decrypt(token)
        id = str(value, 'utf-8')
        index = int(id.index(','))
        newId = str(id[2:index])
        # Needs verifying stage
        if (readFromDatabaseUsingFunction('`checkWhetherCustomer`('+newId+')')[0][0] == 1):
            session.clear()
            # Verifies there email address and logs them in by storing it in session storage.
            verifyEmailInDatabase(newId)
            session['customerID'] = newId
            session.modified = True
            # Directs them to edit there details. Will change this path later on.
            return redirect("/customer/edit")
        else:
            return "You can't be here"
    except:
        return "Invalid Code"

# To Save us having to get a code each time.
@app.route("/customer/hack")
def hackSystem():
    session['customerID'] = '1'
    session.modified = True
    return redirect("/customer/edit")

# Logs a user out
@app.route("/customer/logOut")
@customer_required
def customerLogOut():
    session.clear()
    session.modified = True
    return "Logged Out"

# Lets a user edit there details
@app.route("/customer/edit")
@customer_required
def editCustomerDetails():
    customerID = session['customerID']
    details = readFromDatabaseUsingStoredProcedures("getCustomerDetails("+customerID+")")[0]
    return render_template('customer_edit.html', title = 'Edit Company Details', countries = readFromDatabaseUsingStoredProcedures("getCountries()"), customer = details)


# Admin routes
@app.route("/admin/login")
def adminLogIn():
    return render_template('admin_logIn.html', title = 'Admin Log in')


# Route to show all of the licences that they sell
@app.route("/admin/home")
@admin_required
def adminHome():
    return "Top Secret Admin Details"

# Route to show all of the details about whose bought a specfic licence
@app.route("/admin/licence/<licenceID>")
@admin_required
def adminLicence(licenceID):
    return "Top Secret Details about the licence"

@app.route("/admin/logOut")
@admin_required
def adminLogOut():
    session.clear()
    session.modified = True
    return "Logged Out"


# Reading forms.
@app.route("/gatherCustomerData", methods=['POST'])
@basket_required
def customerForm():
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
        session.modified = True
        # Calls function to process transactions
        return processTransaction()
    return "Error with form"

@app.route("/gatherLicenceData", methods=['POST'])
def licenceForm():
    if request.method == 'POST':
        if 'basket' not in session:
            session['basket'] = {}
        call = "getPrice("+ request.form['tier'] +","+ request.form['length'] +")"
        read = readFromDatabaseUsingFunction(call)
        price = read[0][0]
        print(price)
        licenceID = (request.form['licenceID'])
        session['basket'][licenceID] = {'tier' : request.form['tier'], 'length' : request.form['length'], 'price' : price }
        session.modified = True
    # Redirects them to the basket
        return redirect("/basket")

@app.route("/addLicence/<licenceID>/<tier>/<length>/<price>")
def addLicence(licenceID,tier,length,price):
    if 'basket' not in session:
        session['basket'] = {}
    print(price)
    session['basket'][licenceID] = {'tier' : tier, 'length' : length, 'price' : float(price)}
    session.modified = True
    # Redirects them to the basket
    return redirect("/basket")

@app.route("/updatedCustomerData", methods=['POST'])
def editCustomerForm():
    if 'customerID' in session:
        if request.method == 'POST':
            name = request.form['name']
            nameOfContactPerson = request.form['nameOfContactPerson']
            email = request.form['email']
            street = request.form['street']
            city = request.form['city']
            country = request.form['countries']
            postcode = request.form['postcode']
            vatNumber = request.form['vatNumber']
            customerID = session['customerID']
                # Space to save to database
            return "Updated details"
        return "Error with form"
    return "Error you can't view this area"

@app.route("/formLogIn", methods=['POST'])
def logInForm():
    print("receiving data")
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        if username == "group11IMAGEOPTIM@outlook.com" and password == "password":
            session.clear()
            session['admin'] = True
            session.modified = True
            return redirect("/admin/home")
        else:
            flash("Incorrect username or password")
    return redirect("/admin/login")

# Database Functions
def writeToDatabaseWithCustomerDetails(name, street, city, postcode,country,email,contactPerson,vatNumber):
    # Writes to the database with details of the customer
    cur = mysql.connection.cursor()
    cur.execute("SELECT createCustomer(%s,%s,%s,%s,%s,%s,%s,%s) as 'ID Number';", (name, street, city, postcode,country,email,contactPerson,vatNumber))
    mysql.connection.commit()
    data = cur.fetchall()
    cur.close()
    return data

# Writes to the database with details of the purchase
def writePurchaseIntoDatabase(customerID):
    if 'basket' in session:
        for item in session['basket'].values():
            print("Writing purchase")
            cur = mysql.connection.cursor()
            cur.execute("CALL recordPurchase(%s,%s,%s,%s);", (item.get('tier'), item.get('length'), customerID, item.get('price')))
            mysql.connection.commit()
            data = cur.fetchall()
            cur.close()

def verifyEmailInDatabase(customerID):
        cur = mysql.connection.cursor()
        cur.execute("CALL verifyEmail(%s);",[customerID])
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
            return data
            print("Succesfully from the database")
        except Exception as e:
            print("Error " + e)

def readFromDatabaseUsingFunction(function):
        command = "SELECT " + function +";"
        print("Reading from the database")
        try:
            cur = mysql.connection.cursor()
            cur.execute(command)
            data = cur.fetchall()
            cur.close()
            return data
            print("Succesfully from the database")
        except Exception as e:
            print("Error " + e)


# Functions
def sentCustomerEmail(recipient,name, body,id,price):
    # Creates link for the user
    # Reference https://cryptography.io/en/latest
    message = id.encode()
    key = load_key()
    f = Fernet(key)
    code = f.encrypt(message)
    emailBody = "http://127.0.0.1:5000/"
    link = emailBody + "customer/" + str(code, 'utf-8')
    # Prepares the email with the main body of the email being a html template
    msg = Message(subject='Confirmation Email',sender='group11IMAGEOPTIM@outlook.com', recipients = [recipient])
    msg.html = render_template('customer_emailConfirmation.html',basket = body, name = name,link = link,price = price)
    # Attaches the invoice file
    with app.open_resource('static\invoice\invoice.pdf') as fp:
        msg.attach('invoice.pdf', "invoice/pdf", fp.read())
    # Attaches the contract file
    with app.open_resource('static\contract\contract.pdf') as fp:
        msg.attach('contract.pdf', "contract/pdf", fp.read())
    # Sends the email
    mail.send(msg)

def sentAdminEmail(recipient,companyName, customerName,emailAddress, body, price):
    # Prepares the email with the main body of the email being a html template
    recipients = [ ]
    for i in recipient:
        recipients.append(i)
    msg = Message(subject='Purchase Confirmation',sender='group11IMAGEOPTIM@outlook.com', recipients = recipients)
    msg.html = render_template('admin_emailConfirmation.html',basket = body, customer = companyName,employeeName = customerName,emailAddress = emailAddress,price = price)
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
    basketDetails = gatherBasketDetails()
    # Sents the email to the customer with details of their purchase

    sentCustomerEmail(session.get("customer")["email"], session.get("customer")["nameOfContactPerson"],basketDetails[0],str(id),basketDetails[1])
    #  Reads the email address of the admin from the datbase
    callItem = "getAdminEmail()"
    adminEmails = readFromDatabaseUsingStoredProcedures(callItem)
    # Sents email to the admin with details of the purchase
    sentAdminEmail(adminEmails[0],session.get("customer")["name"], session.get("customer")["nameOfContactPerson"],session.get("customer")["email"], basketDetails[0],basketDetails[1])
    # Clears the basket
    session.clear()
    # Redirects to confirmation page.
    return purchaseConfirmationPage()

def gatherBasketDetails():
    basketArray = []
    price = 0
    size = 0
    if 'basket' in session:
        for key,item in session['basket'].items():
            callItem = "getBasketDetails(" +item['tier'] +","+ item['length'] + ")"
            temp = list(readFromDatabaseUsingStoredProcedures(callItem)[0])
            temp.append(key)
            temp.append(item['price'])
            basketArray.append(temp)
            price = price + item['price']
            size =  size + 1
    return basketArray,price,size

if __name__ == "__main__":
    app.run(debug=True)
