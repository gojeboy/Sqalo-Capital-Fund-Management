from app import db
from sqlalchemy.orm import relationship

from app.models.fund import Fund


class AssetManager(db.Model):
    __tablename__ = 'assetManager'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    emailAddress = db.Column(db.String, nullable=False, unique=True)
    idNumber = db.Column(db.String, nullable=False, unique=True)
    funds = relationship("Fund", back_populates="assetManager")

    def __int__(self, firstname, lastname, emailAddress, idNumber):
        self.firstname = firstname
        self.lastname = lastname
        self.emailAddress = emailAddress
        self.idNumber = idNumber

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def fetchAssetmanagerByEmail(emailAddress):
        return AssetManager.query.filter_by(emailAddress=emailAddress).first()

    @staticmethod
    def fetchAssetmanagerByID(id):
        return AssetManager.query.filter_by(id=id).first()

    def serialize(self):

        funds= Fund.get_funds_by_managerID(self.id)
        serialized_funds = []
        for fund in funds:
            serialized_funds.append(fund.serialize())
        return {
            'ID': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'emailAddress': self.emailAddress,
            'idNumber': self.idNumber,
            'funds': serialized_funds

        }
