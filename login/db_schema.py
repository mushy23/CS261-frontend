from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug import security
from datetime import date, time, datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import text 
import pandas as pd

# create the database interface
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

companyList = pd.read_csv('company_list.csv', nrows=100)
# a model of a user for the database
class User(db.Model,UserMixin):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(20))
    role = db.Column(db.Integer)
    email = db.Column(db.String(120), unique=True)
    dob = db.Column(db.Date)
    verified = db.Column(db.Boolean)

class account(db.Model):
    userID = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80))
    password = db.Column(db.String(120), nullable=False)
    @classmethod
    def get_all(cls):
        return cls.query.all()
    def __repr__(self):
        return '<account %r>' % self.userID

class News(db.Model):
    newsID = db.Column(db.Integer, primary_key = True)
    newsTitle = db.Column(db.String(20))
    companyName = db.Column(db.String(80), db.ForeignKey('company.companyName'),unique=True, nullable=False)
    companyID = db.Column(db.String(80), db.ForeignKey('company.companyID'),unique=True, nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    isPositive = db.Column(db.Boolean)
    content = db.Column(db.Text)
    @classmethod
    def get_all(cls):
        return cls.query.all()
    def __repr__(self):
        return '<News %r>' % self.NewsID

class user(db.Model):
    userID = db.Column(db.Integer, db.ForeignKey('account.userID'), primary_key = True)
    username = db.Column(db.String(80), db.ForeignKey('account.username'), unique=True, nullable=False)
    email = db.Column(db.String(80), db.ForeignKey('account.email'))
    age = db.Column(db.Integer)
    profile_photo = db.Column(db.String(80))
    @classmethod
    def get_all(cls):
        return cls.query.all()
    def __repr__(self):
        return '<user %r>' % self.userID

class company(db.Model):
    companyID = db.Column(db.Integer, primary_key = True)
    companyName = db.Column(db.String(80), nullable=False)
    stockID = db.Column(db.String(80), unique = True)
    @classmethod
    def get_all(cls):
        return cls.query.all()
    def __repr__(self):
        return '<company %r>' % self.companyID
    def print_company(self):
        print(f"Company ID: {self.companyID}, Name: {self.companyName}, Stock ID: {self.stockID}\n")

class userTrack(db.Model):
    userID = db.Column(db.Integer, db.ForeignKey('account.userID'), primary_key = True)
    followedCompanyName = db.Column(db.String(80), db.ForeignKey('company.companyName'),unique=True, nullable=False)
    followedCompanyID = db.Column(db.String(80), db.ForeignKey('company.companyID'),unique=True, nullable=False)
    @classmethod
    def get_all(cls):
        return cls.query.all()

class news_tmp(db.Model):
    tmp_news_id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text)
    @classmethod
    def get_all(cls):
        return cls.query.all()

class compAvg(db.Model):
    companyID = db.Column(db.Integer, primary_key =True)
    date = db.Column(db.DateTime, primary_key = True)
    meansentiment = db.Column(db.Float)
    closingprice = db.Column(db.Float)
    @classmethod
    def get_all(cls):
        return cls.query.all()
#===================================schema end===============================================
#============================================================================================
def resettable():
    with app.app_context():
        db.drop_all()
        db.create_all()

def insert_account(username, email, password):
    with app.app_context():
        new_account = account(username=username, email=email, password=password)
        db.session.add(new_account)
        db.session.commit()

def insert_news(newsTitle, companyName, companyID, isPositive, content):
    with app.app_context():
        new_news = News(newsTitle=newsTitle, companyName=companyName, companyID=companyID, isPositive=isPositive, content=content)
        db.session.add(new_news)
        db.session.commit()

def insert_user(userID, username, email, age, profile_photo):
    with app.app_context():
        new_user = user(userID=userID, username=username, email=email, age=age, profile_photo=profile_photo)
        db.session.add(new_user)
        db.session.commit()

def insert_company(companyName, stockID):
    with app.app_context():
        new_company = company(companyName=companyName, stockID=stockID)
        db.session.add(new_company)
        db.session.commit()

def insert_userTrack(userID, followedCompanyName, followedCompanyID):
    with app.app_context():
        new_user_track = userTrack(userID=userID, followedCompanyName=followedCompanyName, followedCompanyID=followedCompanyID)
        db.session.add(new_user_track)
        db.session.commit()

def insert_tmp_news(content):
    with app.app_context():
        new_news = news_tmp(content=content)
        db.session.add(new_news)
        db.session.commit()

def gettmpnews():
    with app.app_context():
        news_records = news_tmp.query.all()
        for record in news_records:
            print(f"ID: {record.tmp_news_id}, Content: {record.content}")

def dbinit():

    # commit all the changes to the database file
    db.session.commit()

with app.app_context():
    # try:
    resettable()
    for i in range(10):
        insert_company(companyList.at[i, 'Name'], companyList.at[i, 'Symbol'])
    for com in company.get_all():
        com.print_company()



