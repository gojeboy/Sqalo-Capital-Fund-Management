from app import app, db
from flask import request, jsonify
from app.models.assetManager import AssetManager
from app.models.dailyPerformanceStats import DailyPerformanceStats
from app.models.investor import Investor
from app.models.userLogin import LoginDetails
from werkzeug.security import generate_password_hash
from datetime import datetime
from app.models.fund import Fund
@app.route("/registerfundManager", methods= ['POST'])
def registerfundManager():


    data = request.json

    # print(data)

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


@app.route("/addFund", methods=["POST"])
def addFund():
    fundInformation = request.json
    assetManagerID = fundInformation['assetManagerID']
    fundname = fundInformation['fundname']
    fundCurrency = fundInformation['fundCurrency']
    initialCapitalInvested = float(fundInformation['initialCapitalInvested'])
    initialSharesIssued = float(fundInformation['initialSharesIssued'])
    initialPrice = initialCapitalInvested / initialSharesIssued
    fundStartDate = fundInformation['fundStartDate']

    print(fundStartDate)

    date_format = '%Y-%m-%d'
    date_obj = datetime.strptime(fundStartDate, date_format)

    assetManager = AssetManager.fetchAssetmanagerByID(assetManagerID)

    fund = Fund(fundname, currency=fundCurrency, equity=initialCapitalInvested, cashBalance=initialCapitalInvested,
                sharesIssued=initialSharesIssued,
                price=initialPrice, asset_manager_id=assetManager.id)

    fund.save()

    investor = Investor()
    investor.firstname = assetManager.firstname
    investor.lastname = assetManager.lastname
    investor.email = assetManager.emailAddress
    investor.idNumber = assetManager.idNumber
    investor.totalCost = initialCapitalInvested
    investor.totalShares = initialSharesIssued
    investor.fund_id = fund.id

    investor.save()

    exampleInvestmentTrack = initialPrice * initialSharesIssued

    dailyPerformanceStats = DailyPerformanceStats(date_obj, initialPrice, initialSharesIssued, exampleInvestmentTrack,
                                                  fund.id)

    dailyPerformanceStats.save()

    return jsonify(assetManager.serialize()), 200
