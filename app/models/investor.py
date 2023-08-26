from app import db
from sqlalchemy.orm import relationship


class Investor(db.Model):
    __tablename__ = 'investors'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    lastname = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    idNumber = db.Column(db.String, nullable=False, unique=True)
    totalShares = db.Column(db.Float, nullable=True)
    totalCost = db.Column(db.Float, nullable=True)

    fund_id = db.Column(db.Integer, db.ForeignKey('funds.id'))

    # Many-to-one relationship with Fund
    fund = relationship("Fund", back_populates="investors")

    def __int__(self, firstname, lastname, email, idNumber, totalShares, totalCost, fund_id):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.idNumber = idNumber
        self.totalShares = totalShares
        self.totalCost = totalCost
        self.fund_id = fund_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def serialize(self):
        return {
            'investorID': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'idNumber': self.idNumber,
            'totalShares': self.totalShares,
            'totalCost': self.totalCost,
            'fund_id': self.fund_id
        }

    @staticmethod
    def get_investor_by_id(investorID):
        return db.session.query(Investor).filter_by(id=investorID).first()

    @staticmethod
    def get_investor_by_id_number(idNumber):
        return db.session.query(Investor).filter_by(idNumber=idNumber).first()
