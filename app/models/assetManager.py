from app import db
from sqlalchemy.orm import relationship


class AssetManager(db.Model):
    __tablename__ = 'assetManager'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    emailAddress = db.Column(db.String, nullable=False, unique=True)
    idNumber = db.Column(db.String, nullable=False, unique=True)

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

    def serialize(self):
        return {
            'ID': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'emailAddress': self.emailAddress,
            'idNumber': self.idNumber,
            'funds': []

        }
