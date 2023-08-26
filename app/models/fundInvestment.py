from app import db

class FundInvestment(db.Model):
    __tablename__ = 'fund_investment'

    id = db.Column(db.Integer, primary_key=True)
    investment_date = db.Column(db.String, nullable=False)
    fund_id = db.Column(db.Integer, db.ForeignKey('funds.id'), nullable=False)
    investor_id = db.Column(db.Integer, db.ForeignKey('investors.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    shares_purchased = db.Column(db.Float, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)

    fund = db.relationship('Fund', backref='fund_investment')
    investor = db.relationship('Investor', backref='fund_investment')

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def fetchfundInvestmentByFundID(fundID):
        return db.session.query(FundInvestment).filter_by(fund_id=fundID).all()

    @staticmethod
    def fetchfundInvestmentByFundIDSerialized(fundID):
        investments = FundInvestment.fetchfundInvestmentByFundID(fundID)
        serialized_investment = []
        for investment in investments:
            serialized_investment.append(investment.serialize())
        return serialized_investment

    def serialize(self):
        return {
            'id': self.id,
            'investment_date': self.investment_date,
            'fund_id': self.fund_id,
            'investor_id': self.investor_id,
            'amount': self.amount,
            'shares_purchased': self.shares_purchased,
            'purchase_price': self.purchase_price
        }


