from app import app, db
from flask import request, jsonify
from app.models.assetManager import AssetManager
from app.models.userLogin import LoginDetails
from werkzeug.security import generate_password_hash
@app.route("/registerfundManager", methods= ['POST'])
def registerfundManager():


    data = request.json

    print(data)

    # Mananging company information
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    idNumber = data.get('idNumber')
    emailAddress = data.get('emailAddress')
    password = data.get('password')

    assetManager = AssetManager()

    assetManager.firstname = firstname
    assetManager.lastname = lastname
    assetManager.emailAddress = emailAddress
    assetManager.idNumber = idNumber

    assetManager.save()

    loginDetails = LoginDetails()

    loginDetails.username = emailAddress
    loginDetails.password = generate_password_hash(password)

    loginDetails.save()


    return jsonify(assetManager.serialize()), 200
