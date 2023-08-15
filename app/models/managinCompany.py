from app import db
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash
class ManagingCompany(db.Model):
    __tablename__ = 'managing_companies'

    id = db.Column(db.Integer, primary_key=True)
    companyName = db.Column(db.String, nullable=False)
    companyRegistrationNo = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    managerFirstname = db.Column(db.String, nullable=False)
    managerLastname = db.Column(db.String, nullable=False)

    # One-to-one relationship with LoginDetails
    # loginDetailsID = db.Column(db.Integer, db.ForeignKey('login_details.id'))
    # login_details = relationship("LoginDetails", back_populates="managing_company", uselist=False)

    # One-to- many relationship with Fund
    # funds = relationship("Fund", back_populates="managing_company")

    def __init__(self, companyName, companyRegistrationNo, email, managerFirstname, managerLastname, loginDetailsID):
        self.companyName = companyName
        self.companyRegistrationNo = companyRegistrationNo
        self.email = email
        self.managerFirstname = managerFirstname
        self.managerLastname = managerLastname
        self.loginDetailsID = loginDetailsID


    def save(self):
        db.session.add(self)
        db.session.commit()

    def serialize(self):
        return{
            'companyID': self.id,
            'companyName': self.companyName,
            'companyRegistrationNo': self.companyRegistrationNo,
            'email': self.email,
            'managerFirstname': self.managerFirstname,
            'managerLastname': self.managerLastname,
            'loginDetailsID': self.loginDetailsID
        }

    @staticmethod
    def fetchManagingCompanyByLoginID(loginID):
        return ManagingCompany.query.filter_by(loginDetailsID=loginID).first()