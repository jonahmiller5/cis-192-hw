'''
Name: Jonah Miller
PennKey: jonahmil
Hours of work required: 11
'''

import os
import flask
from flask import Flask, flash, request, redirect, render_template
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
import re
import requests

app = Flask(__name__)
app.config.update(dict(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='jonahmil@seas.upenn.edu',
    MAIL_PASSWORD='ynqnhrsmpbriygem',
))
mail = Mail(app)
app.secret_key = 'ax9o4klasi-0oakdn'
app.config['EMAIL_UPLOADS'] = 'uploads/email/'
app.config['PHONE_UPLOADS'] = 'uploads/sms/'
email_check = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
KEY = '192-final-project'


'''
Class to represent an SMS message
Makes it easier to hold data for SMS, send SMS, verify
validity of SMS metadata, and write metadata to cache
'''
class SMS():
    '''
    Construct an instance of the SMS class
    args:
        recipient: the phone number receiving the SMS
        message:   the message to send
    ret:
        N/A
    '''
    def __init__(self, recipient, message):
        self.recipient = recipient
        self.message = message

    '''
    Updates SMS instance to have valid fields
    args:
        N/A
    ret:
        N/A
    '''
    def clean(self):
        if not allowed_phone(self.recipient):
            self = None
            return
        if not self.message:
            self.message = '(empty)'

    '''
    Sends the SMS message to its intended recipient,
    provided that the SMS can be 'cleaned'
    args:
        N/A
    ret:
        N/A
    '''
    def send(self):
        self.clean()

        if not self:
            return

        if self.recipient:
            resp = requests.post('https://textbelt.com/text', {
                'phone': self.recipient,
                'message': self.message,
                'key': KEY,
            })

    '''
    Writes SMS metadata (recipient, message) to a text
    file in the server's cache
    args:
        dir: the directory in which the metadata should
             be written
    ret:
        N/A
    '''
    def write_metadata(self, dir):
        mdata = open(os.path.join(dir, 'metadata'), 'a')
        mdata.write('Recipient: ' + self.recipient + '\n')
        mdata.write('Message: ' + self.message + '\n\n')
        mdata.close()


'''
Class to represent an email
Makes it easier to hold data for email, send email, verify
validity of email metadata, and write metadata to cache
'''
class Email():
    '''
    Construct an instance of the Email class
    args:
        recipient: the email address receiving the email
        image:	   a filepath containing the image name
        subject:   the subject of the email
        message:   the body text of the email
    ret:
        N/A
    '''
    def __init__(self, recipient, image, subject, message):
        self.recipient = recipient
        self.image = image
        self.subject = subject
        self.message = message

    '''
    Updates email instance to have valid fields
    args:
        N/A
    ret:
        N/A
    '''
    def clean(self):
        if not allowed_email(self.recipient):
            self = None
            return
        if not allowed_file(self.image):
            self.image = None
        elif self.image is not None:
            self.ext = 'image/' + determine_ext(self.image)
        if not self.subject:
            self.subject = '(no subject)'
        if not self.message:
            self.message = ''

    '''
    Sends the email to its intended recipient,
    provided that the email can be 'cleaned'
    args:
        N/A
    ret:
        N/A
    '''
    def send(self):
        self.clean()
        msg = Message(self.subject,
                      sender='jonahmil@seas.upenn.edu',
                      recipients=[self.recipient],
                      body=self.message)

        if self.image:
            with open(self.image, "rb") as im:
                msg.attach(self.image, self.ext, im.read())

        mail.send(msg)

    '''
    Spams the email 100 times to its intended recipient
    args:
        N/A
    ret:
        N/A
    '''
    def spam(self):
        for i in range(100):
            self.send()

    '''
    Writes email metadata (recipient, message, subject,
    and media) to a text file in the server's cache
    args:
        dir: the directory in which the metadata should
             be written
    ret:
        N/A
    '''
    def write_metadata(self, dir):
        mdata = open(os.path.join(dir, 'metadata'), 'a')
        mdata.write('Recipient: ' + self.recipient + '\n')
        mdata.write('Message: ' + self.message + '\n')
        mdata.write('Subject: ' + self.subject + '\n')
        if not self.image:
            mdata.write('Media: None\n\n')
        else:
            mdata.write('Media: ' + self.image + '\n\n')

        mdata.close()


'''
Checks whether a file's last 4 characters are part of a valid extension
args:
    filename: string containing the name of the file
ret:
    True if the filename is valid, false otherwise
'''
def allowed_file_3(filename):
    if not filename:
        return True
    if not isinstance(filename, str):
        return False

    filename = filename.lower()
    ext = filename[-4:]

    return ext == '.png' or ext == '.jpg' or ext == '.gif' or ext == '.tif'


'''
Checks whether a file's last 5 characters are part of a valid extension
args:
    filename: string containing the name of the file
ret:
    True if the filename is valid, false otherwise
'''
def allowed_file_4(filename):
    '''
    Check whether the extension is a valid image extension
    args:
        filename: a single string with the name of the file
    ret:
        valid: True if the extension is valid, False otherwise
    '''
    if not filename:
        return True
    if not isinstance(filename, str):
        return False

    filename = filename.lower()
    ext = filename[-5:]

    return ext == '.jpeg' or ext == '.icns' or ext == '.tiff'


'''
Checks whether a file has a valid extension
args:
    filename: string containing the name of the file
ret:
    True if the filename is valid, false otherwise
'''
def allowed_file(filename):
    return allowed_file_3(filename) or allowed_file_4(filename)


'''
Provides the extension of the file
args:
    filename: string containing the name of the file
ret:
    the file extension as a string
'''
def determine_ext(filename):
    if allowed_file_3(filename):
        return filename[-3:]
    elif allowed_file_4(filename):
        return filename[-4:]

    return None


'''
Checks whether an email is a valid email
args:
    email: string containing the email
ret:
    True if the email is valid, false otherwise
'''
def allowed_email(email):
    if not isinstance(email, str) or not email:
        return None

    return re.search(email_check, email)


'''
Checks whether a phone number is a valid number
args:
    numstring: string containing the phone number
ret:
    True if the phone number is valid, false otherwise
'''
def allowed_phone(numstring):
    return (isinstance(numstring, str) and
            len(numstring) == 10 and
            numstring.isdigit())


'''
Presents an HTML page to navigate to either the SMS
webapp or the email webapp
args:
    None
ret:
    The required return by Flask so the user is
    shown the template
'''
@app.route('/')
def home():
    return render_template(secure_filename('home.html'))


'''
Presents an HTML form through which a user can enter SMS
data to send an SMS message
args:
    None
ret:
    The required return by Flask so the user is
    redirected to the correct page upon completion
    of the HTTP request
'''
@app.route('/text', methods=['GET', 'POST'])
def texter():
    if request.method == 'POST':
        form = request.form

        if not allowed_phone(form.get('recipient')):
            flash('Invalid phone number')
            return redirect(request.url)

        dir = os.path.join(app.config['PHONE_UPLOADS'], form.get('recipient'))
        try:
            os.mkdir(dir)
        except FileExistsError:
            pass

        sms = SMS(form.get('recipient'), form.get('message'))
        sms.write_metadata(dir)
        sms.send()

        return redirect('/redir')
    else:
        return render_template(secure_filename('texter.html'))


'''
Presents an HTML form through which a user can enter email
data to send an email
args:
    None
ret:
    The required return by Flask so the user is
    redirected to the correct page upon completion
    of the HTTP request
'''
@app.route('/email', methods=['GET', 'POST'])
def emailer():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if not allowed_file(file.filename):
            flash('Invalid file type')
            return redirect(request.url)

        form = request.form

        if not allowed_email(form.get('recipient')):
            flash('Invalid email address')
            return redirect(request.url)

        dir = os.path.join(app.config['EMAIL_UPLOADS'], form.get('recipient'))
        try:
            os.mkdir(dir)
        except FileExistsError:
            pass

        filepath = None
        if file:
            filepath = os.path.join(dir, secure_filename(file.filename))
            file.save(filepath)

        email = Email(form.get('recipient'),
                      filepath,
                      form.get('subject'),
                      form.get('message'))
        email.write_metadata(dir)

        if form.get('spam') == 'on':
            email.spam()
        else:
            email.send()

        return redirect('/redir')
    else:
        return render_template(secure_filename('email.html'))


'''
Shows a page to indicate a successful message sent
Results from both SMS and email successes
args:
    None
ret:
    The required return by Flask so the user is
    shown the correct image upon completion of
    the redirect
'''
@app.route('/redir')
def redir():
    return app.send_static_file('redir.png')
