from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from ..model.schema import db, Persons
from .AuthController import login_required
from werkzeug.utils import secure_filename
import pyqrcode
import uuid
import os

persons = Blueprint('persons', __name__, url_prefix='/system/persons', template_folder='templates')

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


@persons.route('/', methods=['POST', 'GET'])
def index():
    utype = session.get('account_type')
    persons = getAll()
    if request.method == 'POST':

        for form in request.form:
            if request.form[form] is None:
                message = ("[ WARNING ] Missing field: " + str(form), 'warning')
                flashHandler(message)

        file = request.files['Profile Image']
        if file.filename is not "":
            pid = str(uuid.uuid4())
            pid_path = generate_code(pid)
            pimg = upload_image(request.files['Profile Image'])
            fname = request.form['First Name']
            lname = request.form['Last Name']
            age = request.form['Age']
            gender = request.form['Gender']
            bdate = request.form['Birth Date']
            email = request.form['Email']
            phone = request.form['Phone No.']
            cell = request.form['Cell No.']
            address = request.form['Address']

            rs = getById(pid)
            if rs is not None:
                message = ('PID {} already exist.'.format(pid), 'warning')
                flashHandler(message)
            else:
                try:
                    person = Persons(pid, pimg, pid_path, fname, lname, age, gender, bdate, email, phone, cell, address)
                    createRecord(person)
                    message = ('PID {} successfully added!.'.format(pid), 'success')
                    flashHandler(message)
                    return redirect(url_for('persons.index'))
                except Exception as e:
                    message = ('Internal Error! unable to execute request.', 'danger')
                    print(e)
                    flashHandler(message)
        else:
            message = ('No file selected!', 'warning')
            flashHandler(message)
            redirect(request.url)

    return render_template('persons/index.html', persons=persons, utype=utype)


@persons.route('/delete/<id>', methods=['GET'])
@login_required
def delete(id):
    person = getById(id)
    deleteRecord(person)
    message = ('PID {} successfully deleted!.'.format(id), 'success')
    flashHandler(message)
    return redirect(url_for('persons.index'))


def upload_image(file):
    upload_path = os.path.join(os.getcwd(), "system/static/")
    if file.filename == '':
        message = ('No file selected!', 'warning')
        flashHandler(message)
        return redirect(request.url)
    if file and allowed_ext(file.filename):
        filename = "uploads/{}".format(secure_filename(file.filename))
        file.save(os.path.join(upload_path, filename))
    return filename


def allowed_ext(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_code(pid):
    path = os.path.join(os.getcwd(), "system/static/")
    file = "tmp/{}".format(pid)
    code = pyqrcode.create(pid, error="L", mode="binary", version=5)
    code.png(path + file, scale=10)
    return file


def createRecord(person):
    db.session.add(person)
    db.session.commit()


def deleteRecord(person):
    db.session.delete(person)
    db.session.commit()


def getById(id):
    rs = Persons.query.filter_by(id=id).first()
    return rs


def getAll():
    rs = Persons.query.order_by(Persons.lname).all()
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
