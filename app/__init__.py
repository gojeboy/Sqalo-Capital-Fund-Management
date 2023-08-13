from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqalo-capital.db'  # Change the database URI if needed
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with a secure secret key
db = SQLAlchemy(app)


def reset_db():
    db.create_all()