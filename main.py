from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.userLogin import LoginDetails
from app.models.investor import Investor
from app.models.fund import Fund
from app.models.managinCompany import ManagingCompany
from app.models.dailyPerformanceStats import DailyPerformanceStats
# from flask_script import Manager
# date
from datetime import datetime
from app.controllers.fundManagerController import *

from app import app, db


@app.route('/registerFund', methods=['POST'])
def register():
    data = request.json

    # Mananging company information
    managingCompanyInformation = data.get('managingCompanyInformation')

    companyName = managingCompanyInformation['companyName']
    email = managingCompanyInformation['email']
    firstname = managingCompanyInformation['firstname']
    lastname = managingCompanyInformation['lastname']
    idNumber = managingCompanyInformation['idNumber']

    # Login Details
    loginDetails = data.get('loginDetails')

    username = loginDetails['username']
    password = loginDetails['password']

    managerLogin = LoginDetails()

    managerLogin.username = username
    managerLogin.password = generate_password_hash(password)
    managerLogin.save()

    manangingCompany = ManagingCompany(companyName, idNumber, email, firstname, lastname, managerLogin.id)

    manangingCompany.save()

    # Fund
    fundInformation = data.get('fundInformation')

    fundname = fundInformation['fundname']
    fundCurrency = fundInformation['fundCurrency']
    initialCapitalInvested = float(fundInformation['initialCapitalInvested'])
    initialSharesIssued = float(fundInformation['initialSharesIssued'])
    initialPrice = initialCapitalInvested / initialSharesIssued
    fundStartDate = fundInformation['fundStartDate']

    date_format = '%Y/%m/%d'
    date_obj = datetime.strptime(fundStartDate, date_format)

    fund = Fund(fundname, currency=fundCurrency, equity=initialCapitalInvested, cashBalance=initialCapitalInvested,
                sharesIssued=initialSharesIssued,
                price=initialPrice, investment_company_id=manangingCompany.id)

    fund.save()

    investor = Investor()
    investor.firstname = fundname
    investor.lastname = fundname
    investor.email = email
    investor.idNumber = idNumber
    investor.totalCost = initialCapitalInvested
    investor.totalShares = initialSharesIssued
    investor.fund_id = fund.id

    investor.save()

    exampleInvestmentTrack = initialPrice * initialSharesIssued

    dailyPerformanceStats = DailyPerformanceStats(date_obj, initialPrice,initialSharesIssued, exampleInvestmentTrack, fund.id)

    dailyPerformanceStats.save()

    response = {
        'companyName': manangingCompany.serialize(),
        'fund': fund.serialize(),
    }

    return jsonify(response), 200


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    loginDetails = LoginDetails.query.filter_by(username=username).first()

    if not loginDetails or not loginDetails.check_password(password):
        return jsonify({'message': 'Invalid credentials'}), 401

    assetmanager = AssetManager.fetchAssetmanagerByEmail(emailAddress=loginDetails.username)

    return jsonify(assetmanager.serialize()), 200


@app.route('/fund', methods=['GET'])
def fetch_investors():
    fund_id = request.args.get('fundID')

    fund = Fund.get_fund_by_id(fund_id)

    return jsonify(fund.serialize())

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables
    app.run()
