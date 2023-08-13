from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
class LoginDetails(db.Model):
    __tablename__ = 'login_details'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    # One-to-one relationship with ManagingCompany
    # managing_company = relationship("ManagingCompany", back_populates="login_details", uselist=False)
    # fun = relationship("ManagingCompany", back_populates="login_details", uselist=False)

    # def __int__(self, username, password):
    #     self.username = username
    #     self.password = generate_password_hash(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()



