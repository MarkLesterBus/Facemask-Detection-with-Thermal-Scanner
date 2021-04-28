from flask import (Blueprint, Response, flash, g, redirect, render_template, request, make_response, session, url_for)
from ..model.schema import db, Persons, Contacts, Accounts
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug import secure_filename
from .AuthController import login_required
import os

profile = Blueprint('profile', __name__, url_prefix='/system/profile', template_folder='templates')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


@profile.route('/<id>', methods=['GET'])
@login_required
def index(id):
    person, contacts, account = getAllById(id)
    return render_template('profile/index.html', person=person, contacts=contacts, account=account, id=id)


@profile.route('/print/<id>', methods=['GET'])
def print(id):
    if id == "all":
        person = getAll()
    else:
        person = getById(id)
    return render_template('profile/print.html', person=person, id=id)


@profile.route('<id>/update', methods=['GET', 'POST'])
def update_person(id):
    person = getById(id)
    if request.method == 'POST':
        for form in request.form:
            if request.form[form] is None:
                message = ("[ WARNING ] Missing field: " + str(form), 'warning')
                flashHandler(message)
        file = request.files['Profile Image']
        if file.filename is not "":
            try:
                person.pimg = upload_image(request.files['Profile Image'])
                person.fname = request.form['First Name']
                person.lname = request.form['Last Name']
                person.age = request.form['Age']
                person.gender = request.form['Gender']
                person.bdate = request.form['Birth Date']
                person.email = request.form['Email']
                person.phone = request.form['Phone No.']
                person.cell = request.form['Cell No.']
                person.address = request.form['Address']
                db.session.commit()
                message = ('PID {} successfully updated!.'.format(id), 'success')
                flashHandler(message)
            except Exception as e:
                message = ('Internal Error! unable to execute request.', 'danger')
                flashHandler(message)
                print(e)
        else:
            message = ('No file selected!', 'warning')
            flashHandler(message)
            redirect(request.url)

    return redirect(url_for('profile.index', id=id))


@profile.route('<id>/create', methods=['GET', 'POST'])
def add_contact(id):
    if request.method == 'POST':
        for form in request.form:
            if request.form[form] is None:
                message = ("[ WARNING ] Missing field: " + str(form), 'warning')
                flashHandler(message)

        fname = request.form['Full Name']
        email = request.form['Email']
        phone = request.form['Phone No.']
        cell = request.form['Cell No.']
        address = request.form['Address']

        rs = getByFname(fname)
        if rs is not None:
            message = ('Contact {} already exist.'.format(fname), 'warning')
            flashHandler(message)
        else:
            try:
                person = Contacts(fname, email, phone, cell, address, id)
                createRecord(person)
                message = ('Contact: {} successfully added!.'.format(fname), 'success')
                flashHandler(message)
            except Exception as e:
                message = ('Internal Error! unable to execute request.', 'danger')
                print(e)
                flashHandler(message)
    return redirect(url_for("profile.index", id=id))


@profile.route('<id>/new', methods=['GET', 'POST'])
def new_account(id):
    if request.method == 'POST':

        for form in request.form:
            if request.form[form] is None:
                message = ("[ WARNING ] Missing field: " + str(form), 'warning')
                flashHandler(message)

        uname = request.form['Username']
        pword = generate_password_hash(request.form['Password'])
        utype = request.form['Utype']

        rs = getByUname(uname)
        if rs is not None:
            message = ('Username {} already exist.'.format(uname), 'warning')
            flashHandler(message)
        else:
            try:
                account = Accounts(uname, pword, utype, id)
                createRecord(account)
                message = ('Account: {} successfully added!.'.format(uname), 'success')
                flashHandler(message)
            except Exception as e:
                message = ('Internal Error! unable to execute request.', 'danger')
                print(e)
                flashHandler(message)
    return redirect(url_for("profile.index", id=id))


@profile.route('<id>/edit', methods=['GET', 'POST'])
def edit_account(id):
    account = getAccountById(id)
    if request.method == 'POST':
        for form in request.form:
            if request.form[form] is None:
                message = ("[ WARNING ] Missing field: " + str(form), 'warning')
                flashHandler(message)
        try:
            account.uname = request.form['Username']
            account.pword = generate_password_hash(request.form['Password'])
            account.utype = request.form['Utype']
            db.session.commit()
            message = ('Account: {} successfully updated!.'.format(account.uname), 'success')
            flashHandler(message)
        except Exception as e:
            message = ('Internal Error! unable to execute request.', 'danger')
            flashHandler(message)
            print(e)

    return redirect(url_for("profile.index", id=id))


def upload_image(file):
    upload_path = os.path.join(os.getcwd(), "system/static/")
    if file.filename == '':
        message = ('No file selected!', 'warning')
        flashHandler(message)
    if file and allowed_ext(file.filename):
        filename = "uploads/{}".format(secure_filename(file.filename))
        file.save(os.path.join(upload_path, filename))
    return filename


def allowed_ext(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def getAllById(id):
    person = Persons.query.filter_by(id=id).first()
    contacts = Contacts.query.filter_by(person_id=id).all()
    account = Accounts.query.filter_by(person_id=id).first()
    return person, contacts, account


def getByFname(fname):
    rs = Contacts.query.filter_by(fname=fname).first()
    return rs


def getByUname(uname):
    rs = Accounts.query.filter_by(uname=uname).first()
    return rs


def getAccountById(id):
    rs = Accounts.query.filter_by(id=id).first()
    return rs


def getById(id):
    person = Persons.query.filter_by(id=id).first()
    return person


def getAll():
    persons = Persons.query.order_by(Persons.lname).all()
    return persons


def createRecord(contact):
    db.session.add(contact)
    db.session.commit()


def deleteRecord(contact):
    db.session.delete(contact)
    db.session.commit()


def flashHandler(message):
    (value, category) = message
    if category == 'success':
        flash(value, category)
    elif category == 'info':
        flash(value, category)
    elif category == 'warning':
        flash(value, category)
    elif category == 'danger':
        flash(value, category)
    else:
        flash(value, 'default')
