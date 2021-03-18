# Imports
import os
import json
from flask import Flask, redirect, request, render_template, jsonify, make_response, url_for, abort

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# Variables
app = Flask(__name__)

#Webpage Routes
@app.route("/")
def defaultPage():
    return "Default Page"




if __name__ == "__main__":
    app.run(debug=True)
