# import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug import security
from flask_login import LoginManager, login_user, current_user, logout_user
from flask import session, Flask, render_template, redirect, flash, request, abort, send_file, url_for
from flask_mail import Mail, Message, Connection
from sqlalchemy import bindparam

from sqlalchemy import text
from datetime import datetime, date
from blinker import signal
import time
from io import BytesIO
from smtplib import SMTPRecipientsRefused
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

####
#### WHERE EVER YOU SEE RENDER_TEMPLATE('index3.html'), THERE SHOULD BE A NEW FUNCTION AKA redirect('index3') TO REPRESENT
#### ALL THE FLASK AND JINJA ONCE YOUVE LOGGED IN, I JUST USED RENDER_TEMPLATE TO MAKE IT WORK FOR NOW AND MAKE THE FILE EASY TO EDIT FOR NEW PROJECT
####


# create the Flask app
app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
global reminder # this is for alerting the user when they first log in (it is global but it was much easier than passing in variables)
reminder=False # set it to false, as in they have not been reminded and check for it when first logging in

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def selectuser(): # function to easily grab users to loop through for saying hello "username"
    userid = current_user.id
    qrytext = text("SELECT * FROM users WHERE id=:id;")
    qry = qrytext.bindparams(id=userid)
    resultset = db.session.execute(qry)
    return resultset.fetchall()

# select the database filename
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['TESTING'] = False

app.secret_key = 'any string you want' 

mail = Mail(app)

s = URLSafeTimedSerializer('Secret') # this is used to make the link

# set up a 'model' for the data you want to store
from db_schema import db, User, account, News, user, company, userTrack, news_tmp, dbinit

# init the database so it can connect with our app
db.init_app(app)
mail.init_app(app)

# change this to False to avoid resetting the database every time this app is restarted
resetdb = False # set it so everyone can play with it freely but this should defo be false in normal use
if resetdb:
    with app.app_context():
        # drop everything, create all the tables, then put some data into the tables
        db.drop_all()
        db.create_all()
        dbinit()

#route to the index
@app.route('/')
def index():
    if current_user.is_authenticated: # if already logged in take them to main page
        return render_template('main.html') # this will manage which page to show them
    return render_template('index.html')

@app.route('/registration')
def register():
    if current_user.is_authenticated:
        if not current_user.verified: # this is to force them back to the unverified page
            flash("Please verify your email", "error")
            return render_template('main.html')

        return render_template('main.html')
    return render_template('registration.html')

@app.route('/registeruser', methods = ['GET', 'POST'])
def registeruser():
    global reminder
    if request.method == "POST":
        userName = request.form['username']
        password = request.form['user_password']
        code = request.form['code']
        email = request.form['email']
        dob = request.form['dob']

        if current_user.is_authenticated: # this is for if a user somehow manages to get to registration and tries making a new account
                flash("Please log out first","error")
                return redirect("/index3")

        if email.find("@") == -1: # this probably doesnt run from input="email", but extra validation never hurts
            flash("Enter a correct email.", "error")
            return redirect("/registration")
        if email.find(".com") == -1 and email.find(".uk") == -1: # this can be tweaked to add more domain names
            flash("Enter a correct email.", "error")
            return redirect("/registration")

        password_hash = security.generate_password_hash(password) # make the hash for password
        duplicate = User.query.filter_by(username=userName)
        duplicateemail = User.query.filter_by(email = email) # check if username or email is already taken by checking length of the query
        if len(list(duplicate)) >0: #if a query comes up, username or email is taken
            flash("Username is already taken", "error")
            return redirect("/registration")
        if len(list(duplicateemail)) >0:
            flash("Email is already taken", "error")
            return redirect("/registration")

        token = s.dumps(email,salt='email-confirm') # this will serialize the token so it can be sent over email, and then loaded back in when it reaches the confirm route.
        link = url_for('confirm_email', token=token, _external=True) # here importing url_for from flask helped form the url to the confirm_email route, along with the serialised token containing the email 
        with mail.record_messages() as outbox: # this will catch exceptions for bad emails and make sure email is sent only once
            try:
                mail.send_message(subject='Thanks for registering',
                            sender="Erlind.Caushi@warwick.ac.uk", # this will send the email to the email for the current user
                            body='Welcome to Tickett! Verify here {}'.format(link),#.format(link)), # so for the correct validation i have checked for this above and then made sure
                            recipients=[email])             # that flask-mail is able to send to the email given by the user, if not, flash a warning
                
            except UnicodeEncodeError: # if sending fails to that email return alert, this is really heavy validation and should catch most illegal emails
                flash("Enter a correct email.", "error")
                return redirect("/registration")
            except SMTPRecipientsRefused:
                flash("Enter a correct email.", "error")
                return redirect("/registration") 

            assert len(outbox) == 1

        if code == 'Dc5_G1gz':
            role = 1 # you are an organiser
            reminder = False # make sure reminder is set to false here to reset notifications
        else:
            role = 0 # you are an attendee

        qrytext = text("INSERT INTO users (username, password_hash, role, email, dob, verified) VALUES (:Username, :Password_hash, :Role, :Email, :DOB, :Verified);" )
        qry = qrytext.bindparams(Username=userName, Password_hash=password_hash, Role=role, Email = email, DOB = dob, Verified =False)
        db.session.execute(qry)
        db.session.commit()

        user = User.query.filter_by(username=userName).first() # get user for login

        login_user(user) # log the user session
        return redirect('/registration') # this is so the verify notification can be sent
    
    if request.method=="GET": # this is to catch any sneaky url entering, in which case just redirect them accordingly
        if not current_user.verified:
            flash("Please verify your email", "error")
            return redirect('/')
        return redirect('/')

    return index() # just in case, to avoid any errors call index3 route function

@app.route('/verify')
def verify():
    if current_user.is_authenticated == False: # this is so if the user opens the url without being signed in
        flash("Cannot verify for unlogged in user","error")
        return redirect('/')

    if current_user.verified: # if the user is already verified
        flash("Email already verified", "error")
        return redirect('/')

    token = s.dumps(current_user.email,salt='email-confirm') # if the user is not verified, then send them another email
    link = url_for('confirm_email', token=token, _external=True) # here importing url_for from flask helped to 
    mail.send_message(subject='Thanks for registering', # this will send the email to the email for the current user
        sender="Erlind.Caushi@warwick.ac.uk", # 
        body='Welcome to Tickett! Verify here {}'.format(link), # .format allows the link to be turned into a flask route, which deals with the verification
        recipients=[current_user.email]) # that flask-mail is able to send to the email given by the user, if not, flash a warning

    flash("New verification email has been sent","info") # otherwise inform them another email has been sent
    return render_template('index3.html')

@app.route('/confirm_email/<token>')
def confirm_email(token):
    if current_user.is_authenticated == False:
        flash("Cannot find user","error")
        return redirect('/')
    try:
        email = s.loads(token, salt='email-confirm', max_age=60) # load the email, if this fails because link has expired, resend it
    except SignatureExpired:
        token = s.dumps(current_user.email,salt='email-confirm')
        link = url_for('confirm_email', token=token, _external=True)
        mail.send_message(subject='Thanks for registering', # this is explained above
                sender="Erlind.Caushi@warwick.ac.uk",
                body='Welcome to Tickett! Verify here {}'.format(link),
                recipients=[current_user.email])
                
        return redirect('/registration')

    qrytext = text("UPDATE users SET verified=True WHERE (id=:userid);" ) # i prefer using sql for these queries as you can be confident in the query
    qry = qrytext.bindparams(userid = current_user.id)
    db.session.execute(qry)
    db.session.commit()

    return render_template('main.html')

@app.route('/login', methods = ['GET','POST'])
def login():

        if request.method == "GET":
            return redirect("/")
            
        if request.method=="POST":
            name = request.form['name']
            password = request.form['password']
            user = User.query.filter_by(username=name).first()
            if name == "": # if no name entered
                flash("Enter a username", "error") # this can be done through javascript but it looks nicer using python
                return redirect('/')
            if password == "": # if no password
                flash("Enter a password", "error")
                return redirect('/')
            if user is None: # if username not found
                flash("Please enter a correct username", "error")
                return redirect('/')

            if not security.check_password_hash(user.password_hash, password): # if password is incorrect
                session['userid'] = user.id
                flash("Please enter a correct password", "error")
                return redirect("/")

            login_user(user) # log the user session
            if current_user.verified == False:
                flash("A new verification email has been sent","info") # again this is explained above, but when user logs in again
                # as unverified user, automatically send an email to the email and alert them.
                token = s.dumps(current_user.email,salt='email-confirm')
                link = url_for('confirm_email', token=token, _external=True)
                mail.send_message(subject='Thanks for registering',
                    sender="Erlind.Caushi@warwick.ac.uk",
                    body='Welcome to Tickett! Please verify your email: {}'.format(link),
                    recipients=[current_user.email])
                
                return redirect("/")
            global reminder
            reminder = False # make sure reminder is set to false here to reset notifications
            return render_template('main.html') #get them to main page


@app.route('/main')
def main():
    if current_user.is_authenticated == False:
        flash("Please register first", "error")
        return redirect('/')
    if request.method == "GET":
        companies = company.query.all()
        return render_template('/main.html', companies = companies)
    
@app.route('/compname')
def companyname():
    if current_user.is_authenticated == False:
        flash("Please register first", "error")
        return redirect('/')
    
    if request.method == "GET":
        # here you get query all the info you need from the database and feed it into the html using jinja
        #return render_template('tickets.html', cancelledtickets=cancelledtickets, tickets= tickets, events = events, user=user, now = now)
        # ^^ u do smth like this and then u can loop through them in jinja
        return render_template('/c_profile.html')


@app.route('/logout')
def logout():
        logout_user() # delete session
        return redirect('/')