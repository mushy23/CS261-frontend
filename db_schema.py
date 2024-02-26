from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import text 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class account(db.Model):
    userID = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80))
    password = db.Column(db.String(120), nullable=False)

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

    def __repr__(self):
        return '<News %r>' % self.NewsID

class user(db.Model):
    userID = db.Column(db.Integer, db.ForeignKey('account.userID'), primary_key = True)
    username = db.Column(db.String(80), db.ForeignKey('account.username'), unique=True, nullable=False)
    email = db.Column(db.String(80), db.ForeignKey('account.email'))
    age = db.Column(db.Integer)
    profile_photo = db.Column(db.String(80))

    def __repr__(self):
        return '<user %r>' % self.userID

class company(db.Model):
    companyID = db.Column(db.Integer, primary_key = True)
    companyName = db.Column(db.String(80), unique=True, nullable=False)
    stockID = db.Column(db.String(80), unique = True)

    def __repr__(self):
        return '<company %r>' % self.companyID

class userTrack(db.Model):
    userID = db.Column(db.Integer, db.ForeignKey('account.userID'), primary_key = True)
    followedCompanyName = db.Column(db.String(80), db.ForeignKey('company.companyName'),unique=True, nullable=False)
    followedCompanyID = db.Column(db.String(80), db.ForeignKey('company.companyID'),unique=True, nullable=False)

class news_tmp(db.Model):
    tmp_news_id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text)

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

def insert_company(companyID, companyName, stockID):
    with app.app_context():
        new_company = company(companyID=companyID, companyName=companyName, stockID=stockID)
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


with app.app_context():
    try:
        resettable()
        insert_tmp_news("THIS IS A TEST CONTENT1")
        insert_tmp_news("THIS IS A TEST CONTENT2")
        insert_tmp_news("THIS IS A TEST CONTENT3")
        insert_tmp_news("THIS IS A TEST CONTENT4")
        gettmpnews()
    except Exception as e:
        print("An exception occurred: ", e)

