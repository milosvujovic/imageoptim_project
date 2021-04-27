# Imports
import os
import json
import csv
import datetime
import functools
import stripe
from flask import Flask, render_template, request,redirect,make_response,session, url_for, flash,jsonify
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
from cryptography.fernet import Fernet
from datetime import timedelta
import xlsxwriter

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
# Stripe key
stripe.api_key = "sk_test_51Ij0RhIiHPFxURCath0cVui1kt3mL3f9HSS7u5GBIPiwKkyWSga2E5EZrN06DRdASmH5UO349yPSpgdYXsN7NQAH00wI76I7E9"

mail = Mail(app)
mysql = MySQL(app)

# Functions for logging in
def customer_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
            if  'customerID' not in session:
                return render_template('customer_logInError.html', title = "Log In")
            return func(*args, **kwargs)
    return secure_function

def admin_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if 'admin' not in session:
            return redirect(url_for("adminLogIn", next=request.url))
        return func(*args, **kwargs)
    return secure_function

def basket_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if 'basket' not in session or len(session['basket']) == 0:
            return render_template('user_checkoutWarning.html', title = "Checkout")
        return func(*args, **kwargs)
    return secure_function

# Reference https://devqa.io/encrypt-decrypt-data-python/
# Sets up the key for the encryption and sending the codes
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
    comments = readFromDatabaseUsingStoredProcedures("getAllValidComments()")
    print(comments)
    return render_template('user_home.html', title = "Home", licences = readFromDatabaseUsingStoredProcedures("getListOfLicence()"),comments = comments)

# Displays page with options to select a licence
@app.route("/licence/<licenceID>")
def selectLicence(licenceID):
    callTiers = "getTiersForLicence("+licenceID+")"
    callLengths = "getLengthOfLicences("+licenceID+")"
    callDescription = "getDescription("+licenceID+")"
    # If the user has already selected a licence then gets value so that it will set the selected licence as checked.
    tier = -1
    length = -1
    if 'basket' in session:
        if licenceID in session['basket']:
            tier = int(session['basket'][licenceID]['tier'])
            length = int(session['basket'][licenceID]['length'])
    return render_template('user_licence.html', title = "Licence", tiers = readFromDatabaseUsingStoredProcedures(callTiers), lengths= readFromDatabaseUsingStoredProcedures(callLengths), licenceID = licenceID, selectedTier = tier, selectedLength = length, description = readFromDatabaseUsingStoredProcedures(callDescription))

# Displays basket page.
# Having read the details about each item from the database.
@app.route("/basket")
def basketPage():
    print("basket")
    basketDetails = gatherBasketDetails()
    return render_template('user_basket.html', title = "Basket", basket =  basketDetails[0], size = basketDetails[2], price ="{:.2f}".format(basketDetails[1]))

# Removes selected item from the basket and redirects them to the basket
@app.route("/basket/remove/<licenceID>")
def removeFromBasket(licenceID):
    print("remove item")
    if 'basket' in session:
        if licenceID in session['basket']:
            print("remove item")
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
@app.route("/purchase/<tier>/<length>/<price>")
def addLicence(tier,length,price):
    tier = str(decryptWord(tier))
    length = str(decryptWord(length))
    price = float(decryptWord(price))
    message = 'checkWhetherValidTierAndLength(' + tier + ','+ length +')'
    result = (readFromDatabaseUsingFunction(message))
    print(tier)
    print(length)
    print(price)
    print(result[0][0])
    if (result[0][0] == None or price < 0):
        return "Invalid codes"
    else:
        if 'basket' not in session:
            session['basket'] = {}
        licenceID = result[0][0]
        session['basket'][str(licenceID)] = {'tier' : str(tier), 'length' : str(length), 'price' : str(price)}
        session.modified = True
    return redirect('/basket')

# Displays checkout page asking for users details.
@app.route("/checkout")
@basket_required
def customerPage():
    return render_template('user_customerDetails.html', title = "Customer Details", countries = readFromDatabaseUsingStoredProcedures("getCountries()"))

# Allows the user to purchase a licence at a price that has been negotiated
@app.route("/admin/neg/<tierID>/<lengthID>/<priceID>")
def createLink(tierID,lengthID,priceID):
    # Reference https://cryptography.io/en/latest
    key = load_key()
    f = Fernet(key)
    lengthCode = encryptWord(lengthID)
    priceCode = encryptWord(priceID)
    tierCode = encryptWord(tierID)
    code = lengthCode + "/" + tierCode + "/" + priceCode
    originalLength = decryptWord(lengthCode)
    originalTier = decryptWord(tierCode)
    originalPrice = decryptWord(priceCode)
    code = code + originalLength + "/" + originalPrice + "/" + originalTier
    return redirect("/admin/home")

# Displays purchase confirmation page
def purchaseConfirmationPage():
    return render_template('user_purchaseConfirmation.html', title = "Purchase Confirmation")

# Displays basket page.
# Having read the details about each item from the database.
@app.route("/contactUs")
def contactPage():
    return render_template('user_contactUs.html', title = "Contact Us")


# Customers Web routes
# Logs  user in
@app.route("/customer/<input>")
def displayCustomerDetails(input):
    # try:
        # Decodes the code in the email
        id = decryptWord(input)
        index = int(id.index(','))
        newId = str(id[2:index])
        print(newId)
        # Needs verifying stage
        if (readFromDatabaseUsingFunction('`checkWhetherCustomer`('+newId+')')[0][0] == 1):
            print("va;od")
            session.clear()
            # command = "CALL verifyEmail(%s);"
            # parameters = (newId)
            command = "CALL verifyEmail('{0}');".format(newId)
            writeToDatabase2(command)
            print("verified the email2")
            session['customerID'] = newId
            session.modified = True
            # Directs them to edit there details. Will change this path later on.
            return redirect("/customer/edit")
        else:
            return render_template('customer_logInError.html', title = "Log In")
    # except:
    #     return "Invalid Code"

# To Save us having to get a code each time.
@app.route("/customer/hack")
def hackSystem():
    session['customerID'] = '1'
    session.modified = True
    return redirect("/customer/edit")

# Gets the list of licences that the customer has
@app.route("/customer/licences")
def gatherCustomersLicences():
    call = "getCustomersCurrentLicences("+ session['customerID'] + ")"
    current= readFromDatabaseUsingStoredProcedures(call)
    print(current)
    call2 = "getCustomersPastLicences("+ session['customerID'] + ")"
    previous = readFromDatabaseUsingStoredProcedures(call2)
    print(previous)
    return render_template('customer_licences.html', title = "Licences", currentLicences = current,previousLicences =previous)

# Allows the user to leave a review
@app.route("/customer/review")
def review():
    return render_template('customer_review.html', title = "Review")

# Lets a user edit there details
@app.route("/customer/edit")
@customer_required
def editCustomerDetails():
    customerID = session['customerID']
    details = readFromDatabaseUsingStoredProcedures("getCustomerDetails("+customerID+")")[0]
    return render_template('customer_edit.html', title = 'Edit Company Details', countries = readFromDatabaseUsingStoredProcedures("getCountries()"), customer = details)

# Logs a user out
@app.route("/customer/logOut")
@customer_required
def customerLogOut():
    session.clear()
    session.modified = True
    return redirect("/")


# Admin

# Admin routes
# Allows the admin to log in
@app.route("/admin/login")
def adminLogIn():
    if 'admin' in session:
        return redirect('/admin/home')
    else:
        return render_template('admin_logIn.html', title = 'Admin Log in')


# Route to show all of the licences that they sell
@app.route("/admin/home")
@admin_required
def adminHome():
    return render_template('admin_home.html',title = "Admin",currentLicences = readFromDatabaseUsingStoredProcedures("getListOfLicence()"),previousLicences = readFromDatabaseUsingStoredProcedures("getDiscontinutedLicences()"))

# Route to show all of the details about whose bought a specfic licence
@app.route("/admin/licence/<licenceID>")
@admin_required
def adminLicence(licenceID):
    call = "getPurchasesForLicences("+ licenceID + ")"
    call2 = "getPastPurchasesForLicences("+ licenceID + ")"
    return render_template('admin_licenceStats.html', title = "Purchases", currentLicences = readFromDatabaseUsingStoredProcedures(call),expiredLicences = readFromDatabaseUsingStoredProcedures(call2))

# Shows all the customer details
@app.route("/admin/customerDetails/<customerID>")
@admin_required
def adminCustomerDetails(customerID):
    call = "getCustomersCurrentLicences("+ customerID + ")"
    call2 = "getCustomersPastLicences("+ customerID + ")"
    call3 = "getDetailsOnCompany(" + customerID + ")"
    return render_template('admin_customerDetails.html', title = "Customer", currentLicences = readFromDatabaseUsingStoredProcedures(call),expiredLicences = readFromDatabaseUsingStoredProcedures(call2), company = readFromDatabaseUsingStoredProcedures(call3)[0])

# Allows the admin to negotiate a price
@app.route("/admin/negotiate/<licenceID>")
@admin_required
def negotiatePrice(licenceID):
    callTiers = "getTiersForLicence("+licenceID+")"
    callLengths = "getLengthOfLicences("+licenceID+")"
    return render_template('admin_negoitatePrice.html', title = "Negotiate", tiers = readFromDatabaseUsingStoredProcedures(callTiers), lengths= readFromDatabaseUsingStoredProcedures(callLengths))

# Allows the admin to download a list of purchases
@app.route("/admin/purchases")
@admin_required
def adminCSV():
    return render_template('admin_csv.html')

# Allows the admin to download a list of purchases
@app.route("/admin/comment/validate/<id>")
@admin_required
def adminValidateReview(id):
    command = "CALL verifyComment(%s);"
    parameters =(id)
    writeToDatabase(command,parameters)
    return redirect("/admin/home")

@app.route("/admin/comment/remove/<id>")
@admin_required
def adminValidateReviewRemove(id):
    command = "CALL removeComment(%s);"
    parameters =(id)
    writeToDatabase(command,parameters)
    return redirect("/admin/home")

# Allows the admin to verify emails
@app.route("/admin/comments")
@admin_required
def adminComments():
    return render_template('admin_validateReview.html', comments = readFromDatabaseUsingStoredProcedures("getCommentsToVerify()"), currentComments = readFromDatabaseUsingStoredProcedures("getAllValidComments()"))

# Allows the admin to see the data about the stats
@app.route("/admin/bar")
def bar():
    numberOfSales = collectDataForGraph("getNumberOfPurchasesPerLicence()")
    totalRevenue = collectDataForGraph("getRevenue()")
    licenceLength = collectDataForGraph("mostCommonLicenceLength()")
    countriestat =collectDataForGraph("getCountriesFrom()")
    return render_template('admin_bar.html', title = "Stats", labelNumber = numberOfSales[0], figureNumber = numberOfSales[1], labelRevenue = totalRevenue[0], figureRevenue = totalRevenue[1], lengthLabel = licenceLength[0],lengthFigure = licenceLength[1],countryLabel = countriestat[0],countryFigure = countriestat[1])

@app.route("/admin/edit/<id>")
@admin_required
def adminEditLicence(id):
    licenceData = readFromDatabaseUsingStoredProcedures("getDescription("+id+")")
    return render_template("admin_editLicence.html", title = "Edit Licence", licence = licenceData[0], licenceID = id)

def collectDataForGraph(procedure):
    figures = []
    labels = []
    data = readFromDatabaseUsingStoredProcedures(procedure)
    for i in data:
        labels.append(str(i[0]))
        figures.append(str(i[1]))
    return labels, figures

@app.route("/admin/discontinue/<licenceID>")
@admin_required
def adminDiscontinue(licenceID):
    command = "CALL discontinueLicence(%s,%s);"
    parameters = licenceID, True
    writeToDatabase(command,parameters)
    return redirect("/admin/home")

@app.route("/admin/continue/<licenceID>")
@admin_required
def adminContinue(licenceID):
    command = "CALL discontinueLicence(%s,%s);"
    parameters = licenceID, False
    writeToDatabase(command,parameters)
    return redirect("/admin/home")

@app.route("/admin/logOut")
@admin_required
def adminLogOut():
    session.clear()
    session.modified = True
    return redirect("/")

# Encyptions forms

def encryptWord(word):
    # Reference https://cryptography.io/en/latest
    key = load_key()
    encryptor = Fernet(key)
    word = str(word)
    word = word.encode()
    wordCode = encryptor.encrypt(word)
    wordCode = str(wordCode, 'utf-8')
    return wordCode

def decryptWord(word):
    # Reference https://cryptography.io/en/latest
    key = load_key()
    decryptor = Fernet(key)
    word = str(word)
    word = word.encode()
    word = decryptor.decrypt(word)
    word = str(word, 'utf-8')
    return word

# Reading forms.
# User forms
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
        # Stores the customer details in a dictionary in the server session storage
        print(request.form['cardNumber'])
        print(request.form['expiryDateMonth'])
        print(request.form['expiryDateYear'])
        print(request.form['securityCode'])
        print(request.form['issueNumber'])
        # Calls function to process transactions
        # processPayment()
        processTransaction()
        # Redirects to confirmation page.
        return purchaseConfirmationPage()
    return "Error with form"

@app.route("/gatherContactUs", methods=['POST'])
def contactForm():
    if request.method == 'POST':
        # Stores the customer details in a dictionary in the server session storage
        sentCommentEmail(request.form['nameOfContactPerson'], request.form['email'], request.form['name'], request.form['comment'])
        return redirect("/")
    return "Error with form"




@app.route("/gatherLicenceData", methods=['POST'])
def licenceForm():
    print("This is not meant to be called")
    if request.method == 'POST':
        if 'basket' not in session:
            session['basket'] = {}
        call = "getPrice("+ request.form['tier'] +","+ request.form['length'] +")"
        read = readFromDatabaseUsingFunction(call)
        price = read[0][0]
        print(price)
        licenceID = (request.form['licenceID'])
        session['basket'][str(licenceID)] = {'tier' : str(request.form['tier']), 'length' : str(request.form['length']), 'price' : str(price) }
        session.modified = True
    # Redirects them to the basket
        return redirect("/basket")

@app.route("/GetPrices/<tier>/<length>", methods=['GET'])
def getPrice(tier, length):
    # # call = "getPrice("+ str(1) +","+ str(1) +")"
    # # read = readFromDatabaseUsingFunction(call)
    if request.method == 'GET':
        call = "getPrice("+ str(tier) +","+ str(length) +")"
        read = readFromDatabaseUsingFunction(call)
        return json.dumps(read);

# Customer forms
@app.route("/leaveReview", methods=['POST'])
def reviews():
    if request.method == 'POST':
        command = "CALL writeReviewIntoDatabase(%s,%s,%s);"
        parameters =(request.form['comment'], request.form['rating'], session['customerID'])
        writeToDatabase(command,parameters)
        return redirect('/customer/licences')
    return "Error with form"



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
            command = "CALL updateCustomer(%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            parameters = name, street, city, postcode, country, email, nameOfContactPerson, vatNumber, customerID
            writeToDatabase(command,parameters)
            return redirect("/customer/licences")
        return "Error with form"
    return "Error you can't view this area"



# Admin forms
@app.route("/createLink", methods=['POST'])
@admin_required
def linkForm():
    if request.method == 'POST':
        # Stores the customer details in a dictionary in the server session storage
        tierID = request.form['tier']
        lengthID = request.form['length']
        priceID = request.form['price']
        email =  request.form['email']
        name =  request.form['name']
        key = load_key()
        f = Fernet(key)
        lengthCode = encryptWord(lengthID)
        priceCode = encryptWord(priceID)
        tierCode = encryptWord(tierID)
        code = "http://127.0.0.1:5000/purchase/"+tierCode + "/" + lengthCode + "/" + priceCode
        sentOfferEmail(email,name,code)
        return redirect("/admin/home")

@app.route("/updateLicence/<licenceID>", methods=['POST'])
@admin_required
def editLicence(licenceID):
    if request.method == 'POST':
        # Stores the customer details in a dictionary in the server session storage
        name = request.form['name']
        description = request.form['description']
        command = "CALL updateLicence(%s,%s,%s);"
        parameters = licenceID, name, description
        writeToDatabase(command,parameters)
        return redirect("/admin/home")

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
def writeToDatabase(command,parameters):
    cur = mysql.connection.cursor()
    print("about to proceed the information")
    cur.execute(command, parameters)
    print("executed the information")
    mysql.connection.commit()
    data = cur.fetchall()
    cur.close()
    return data

def writeToDatabase2(command):
    cur = mysql.connection.cursor()
    cur.execute(command)
    mysql.connection.commit()
    data = cur.fetchall()
    cur.close()
    return data

def writeToDatabase(command,parameters):
    cur = mysql.connection.cursor()
    print("about to proceed the information")
    cur.execute(command, parameters)
    print("executed the information")
    mysql.connection.commit()
    data = cur.fetchall()
    cur.close()
    return data

def readFromDatabaseUsingStoredProcedures(function):
        command = "CALL " + function +";"
        return readFromDatabase(command)

def readFromDatabase(command):
    try:
        cur = mysql.connection.cursor()
        cur.execute(command)
        data = cur.fetchall()
        cur.close()
        return data
    except Exception as e:
        print(e)

def readFromDatabaseUsingFunction(function):
        command = "SELECT " + function +";"
        return readFromDatabase(command)

# Functions

# Emails
def sentCustomerEmail(recipient,name, body,id,price):
    # Creates link for the user to access account
    emailBody = "http://127.0.0.1:5000/"
    code = encryptWord(id)
    link = emailBody + "customer/" + code
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

def sentOfferEmail(recipient,name, link):
    # Prepares the email with the main body of the email being a html template
    msg = Message(subject='Negotiated Price',sender='group11IMAGEOPTIM@outlook.com', recipients = [recipient])
    msg.html = render_template('customer_offerEmail.html',name = name,link = link)
    # Sends the email
    mail.send(msg)

def sentCommentEmail(customerName, emailAddress, companyName, comment):
    # Prepares the email with the main body of the email being a html template
    msg = Message(subject='Comment from customer',sender='group11IMAGEOPTIM@outlook.com', recipients = ['group11IMAGEOPTIM@outlook.com'],reply_to=emailAddress)
    msg.html = render_template('admin_emailContactUs.html',name = customerName,email = emailAddress,companyName = companyName,comment = comment)
    # Sends the email
    mail.send(msg)


def processTransaction():
    # Writes the new customer to the database and returns the Id of the customer
    command = "SELECT createCustomer(%s,%s,%s,%s,%s,%s,%s,%s) as 'ID Number';"
    parameters = session.get("customer")["name"], session.get("customer")["street"], session.get("customer")["city"], session.get("customer")["postcode"],session.get("customer")["country"],session.get("customer")["email"],session.get("customer")["nameOfContactPerson"],session.get("customer")["vatNumber"]
    id = writeToDatabase(command,parameters)
    # Writes the details of the purchase into the database
    if 'basket' in session:
        for item in session['basket'].values():
            command = "CALL recordPurchase(%s,%s,%s,%s);"
            parameters = (item.get('tier'), item.get('length'), id, item.get('price'))
            writeToDatabase(command,parameters)
    # Reads the details of the basket from the datbase to put in email
    basketDetails = gatherBasketDetails()
    connectWithStripe(int(basketDetails[1]*100),session.get("customer")["email"])
    # Sents the email to the customer with details of their purchase
    sentCustomerEmail(session.get("customer")["email"], session.get("customer")["nameOfContactPerson"],basketDetails[0],str(id),"{:.2f}".format(basketDetails[1]))
    #  Reads the email address of the admin from the datbase
    callItem = "getAdminEmail()"
    adminEmails = readFromDatabaseUsingStoredProcedures(callItem)
    # Sents email to the admin with details of the purchase
    sentAdminEmail(adminEmails[0],session.get("customer")["name"], session.get("customer")["nameOfContactPerson"],session.get("customer")["email"], basketDetails[0],"{:.2f}".format(basketDetails[1]))
    # Clears the basket
    session.clear()


def gatherBasketDetails():
    basketArray = []
    price = 0
    size = 0
    if 'basket' in session:
        for key,item in session['basket'].items():
            callItem = "getBasketDetails(" +str(item['tier']) +","+ str(item['length']) + ")"
            temp = list(readFromDatabaseUsingStoredProcedures(callItem)[0])
            temp.append(key)
            temp.append(item['price'])
            basketArray.append(temp)
            price = price + float(item['price'])
            size =  size + 1
    return basketArray,price,size

def CreateCSVPurchases():
    row_list = readFromDatabaseUsingStoredProcedures("getAllPurchases()")
    counter = 2
    #Creates the file
    workbook = xlsxwriter.Workbook('static/purchases/purchaseHistory.xlsx')
    worksheet = workbook.add_worksheet()
    #Adds heading to the file
    worksheet.write("A1", "Date")
    worksheet.write("B1", "Name")
    worksheet.write("C1", "Price")
    worksheet.write("D1", "Country")
    worksheet.write("E1", "Vat Number")
    #Loops through each student and adds them to the spreadsheet
    for x in row_list:
        Date = "A"+str(counter)
        Name = "B"+str(counter)
        Price = "C"+str(counter)
        Country = "D"+str(counter)
        VAT = "E"+str(counter)
        worksheet.write(Date, str(x[0]))
        worksheet.write(Name, x[1])
        worksheet.write(Price, x[2])
        worksheet.write(Country, x[3])
        worksheet.write(VAT, x[4])
        counter = counter + 1
    workbook.close()
    return row_list

def connectWithStripe(price,emailAddres):
  session = stripe.checkout.Session.create(
    customer_email=emailAddres,
    payment_method_types=['card'],
    line_items=[{
      'price_data': {
        'currency': 'usd',
        'product_data': {
          'name': 'Image Optim Licences',
        },
        'unit_amount': price,
      },
      'quantity': 1,
    }],
    mode='payment',
    success_url='https://bbc.com',
    cancel_url='https://youtube.com',
  )
  return jsonify(id=session.id)



if __name__ == "__main__":
    app.run(debug=True)
