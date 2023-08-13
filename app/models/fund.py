from app import db
from sqlalchemy.orm import relationship


class Fund(db.Model):
    __tablename__ = 'funds'

    id = db.Column(db.Integer, primary_key=True)
    fundname = db.Column(db.String, nullable=False)
    currency = db.Column(db.String, nullable=False)
    equity = db.Column(db.Float, nullable=False)
    cashBalance = db.Column(db.Float, nullable=False)
    sharesIssued = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)

    investment_company_id = db.Column(db.Integer, db.ForeignKey('managing_companies.id'))

    # Many-to-one relationship with ManagingCompany
    managing_company = relationship("ManagingCompany", back_populates="funds")

    # One-to-many relationship with Investor
    investors = relationship("Investor", back_populates="fund")

    # One-to-many relationship with DailyPerformanceStats
    daily_performance_stats = relationship("DailyPerformanceStats", back_populates="fund")

    def __init__(self, fundname, currency, equity, cashBalance, sharesIssued, price, investment_company_id):
        self.fundname = fundname
        self.currency = currency
        self.equity = equity
        self.cashBalance = cashBalance
        self.sharesIssued = sharesIssued
        self.price = price
        self.investment_company_id = investment_company_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def serialize(self):
        investors = []

        for investor in self.investors:
            investors.append(investor.serialize())

        return {
            'fundID': self.id,
            'fundname': self.fundname,
            'currency': self.currency,
            'equity': self.equity,
            'cashBalance': self.cashBalance,
            'sharesIssued': self.sharesIssued,
            'price': self.price,
            'investors':investors
        }

    @staticmethod
    def get_fund_by_id(fundID):
        return db.session.query(Fund).filter_by(id=fundID).first()

