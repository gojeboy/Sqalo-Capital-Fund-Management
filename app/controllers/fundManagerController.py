from app import app, db
from flask import request, jsonify
from app.models.assetManager import AssetManager
from app.models.dailyPerformanceStats import DailyPerformanceStats
from app.models.fundInvestment import FundInvestment
from app.models.investor import Investor
from app.models.userLogin import LoginDetails
from werkzeug.security import generate_password_hash
from datetime import datetime
from app.models.fund import Fund
from app.utils.constants import transactionFeePercentage
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
    investor.type = 'Individual'

    investor.save()

    exampleInvestmentTrack = initialPrice * initialSharesIssued

    dailyPerformanceStats = DailyPerformanceStats(date_obj, initialPrice, initialSharesIssued, exampleInvestmentTrack,
                                                  fund.id)

    dailyPerformanceStats.save()

    return jsonify(assetManager.serialize()), 200


@app.route("/addInvestor", methods=["POST"])
def addInvestorTofund():
    data = request.json

    firstname = data['firstname']
    lastname = data['lastname']
    emailAddress = data['emailAddress']
    fundID= data['fundID']
    idNumber = data["idNumber"]
    type = data["type"]

    fund = Fund.get_fund_by_id(fundID)

    investor = Investor()

    investor.firstname = firstname
    investor.lastname = lastname
    investor.email = emailAddress
    investor.idNumber = idNumber
    investor.type = type
    investor.fund_id = fund.id

    investor.save()

    return jsonify(fund.serialize()), 200

@app.route("/fund", methods=["GET"])
def fetchFundByID():
    fundID = request.args['fundID']

    fund = Fund.get_fund_by_id(fundID)

    return jsonify(fund.serialize()), 200

@app.route("/makeDeposit", methods=["POST"])
def makeDeposit():
    data = request.json

    depositAmount = float(data['depositAmount'])
    exchangeRate = float(data['exchangeRate'])
    purchasePrice = float(data['purchasePrice'])

    depositDate = data['depositDate']
    fundID = data['fundID']
    investorID = data['investorID']

    dollarDepositAmount = depositAmount * exchangeRate

    transactionFee = dollarDepositAmount * transactionFeePercentage

    investedAmount = dollarDepositAmount - transactionFee

    investorPurchaseShares = investedAmount / purchasePrice

    companyInvestedShares = transactionFee / purchasePrice


    fund = Fund.get_fund_by_id(fundID)
    investor = Investor.get_investor_by_id(investorID)

    investor_fund_investment = FundInvestment()

    investor_fund_investment.fund_id = fund.id
    investor_fund_investment.investor_id = investor.id
    investor_fund_investment.amount = investedAmount
    investor_fund_investment.shares_purchased = investorPurchaseShares
    investor_fund_investment.purchase_price = purchasePrice
    investor_fund_investment.investment_date = depositDate

    investor_fund_investment.save()

    investor.totalShares = investorPurchaseShares if investor.totalShares is None else investor.totalShares + investorPurchaseShares
    investor.totalCost = investedAmount if investor.totalCost is None else investor.totalCost + investedAmount
    investor.save()

    #Company investment
    assetManager = AssetManager.fetchAssetmanagerByID(fund.asset_manager_id)

    investor_asset_manager = Investor.get_investor_by_id_number(assetManager.idNumber)
    investor_asset_manager.totalShares += companyInvestedShares
    investor_asset_manager.totalCost += transactionFee


    company_fund_investment = FundInvestment()
    company_fund_investment.fund_id = fund.id
    company_fund_investment.investor_id = investor_asset_manager.id
    company_fund_investment.amount = transactionFee
    company_fund_investment.shares_purchased = companyInvestedShares
    company_fund_investment.purchase_price = purchasePrice
    company_fund_investment.investment_date = depositDate

    company_fund_investment.save()

    investor_asset_manager.save()

    fund.sharesIssued += investorPurchaseShares + companyInvestedShares

    fund.save()

    return jsonify(fund.serialize()), 200




    



