from app import db
from sqlalchemy.orm import relationship

class DailyPerformanceStats(db.Model):
    __tablename__ = 'daily_performance_stats'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    price = db.Column(db.Float, nullable=False)
    totalSharesIssued = db.Column(db.Float, nullable=False)
    exampleInvestmentTrack = db.Column(db.Float, nullable=False)
    fund_id = db.Column(db.Integer, db.ForeignKey('funds.id'))

    # Many-to-one relationship with Fund
    fund = relationship("Fund", back_populates="daily_performance_stats")

    def __init__(self, date, price,totalSharesIssued, exampleInvestmentTrack, fund_id):
        self.date = date
        self.price = price
        self.totalSharesIssued = totalSharesIssued
        self.exampleInvestmentTrack = exampleInvestmentTrack
        self.fund_id = fund_id


    def save(self):
        db.session.add(self)
        db.session.commit()