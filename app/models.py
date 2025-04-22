from . import db

class PasswordEntry(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    account = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)