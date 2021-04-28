from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from ..model.schema import db, Contacts
from .AuthController import login_required


contacts = Blueprint('contacts', __name__, url_prefix='/system/contacts', template_folder='templates')


@contacts.route('/', methods=['POST', 'GET'])
@login_required
def index():
    contacts = getAll()
    # if request.method == 'POST':
    #
    #     for form in request.form:
    #         if request.form[form] is None:
    #             message = ("[ WARNING ] Missing field: " + str(form), 'warning')
    #             flashHandler(message)
    #
    #     fname = request.form['Full Name']
    #     email = request.form['Email']
    #     phone = request.form['Phone No.']
    #     cell = request.form['Cell No.']
    #     address = request.form['Address']
    #
    #     rs = getByFname(fname)
    #     if rs is not None:
    #         message = ('Contact {} already exist.'.format(fname), 'warning')
    #         flashHandler(message)
    #     else:
    #         try:
    #             person = Contacts(fname, email, phone, cell, address, id)
    #             createRecord(person)
    #             message = ('Contact: {} successfully added!.'.format(fname), 'success')
    #             flashHandler(message)
    #             return redirect(url_for('contacts.index', id=id))
    #         except Exception as e:
    #             message = ('Internal Error! unable to execute request.', 'danger')
    #             print(e)
    #             flashHandler(message)

    return render_template('contacts/index.html', contacts=contacts)


@contacts.route('/delete/<id>', methods=['GET'])
@login_required
def delete(id):
    contact = getById(id)
    deleteRecord(contact)
    message = ('Contact {} successfully deleted!.'.format(contact.fname), 'success')
    flashHandler(message)
    return redirect(url_for('contacts.index'))


def createRecord(contact):
    db.session.add(contact)
    db.session.commit()


def deleteRecord(contact):
    db.session.delete(contact)
    db.session.commit()

def getById(id):
    rs = Contacts.query.filter_by(id=id).first()
    return rs

def getByFname(fname):
    rs = Contacts.query.filter_by(fname=fname).first()
    return rs


def getAll():
    rs = Contacts.query.order_by(Contacts.fname).all()
    return rs

def getAllById(id):
    rs = Contacts.query.order_by(Contacts.fname).filter_by(person_id=id).all()
    return rs


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