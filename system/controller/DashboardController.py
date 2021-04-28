from flask import (Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for)
from ..model.schema import db, Persons, Contacts, Accounts, Attendance
from .AuthController import login_required

dashboard = Blueprint('dashboard', __name__, url_prefix='/', template_folder='templates')


@dashboard.route('/', methods=['POST'])
@login_required
def index():
    persons, accounts = getAll()
    scanned = getAllDistinct()
    hightemp = getAllTemp()
    return render_template('dashboard/index.html', persons=persons, accounts=accounts, scanned=scanned,
                           hightemp=hightemp)


def getAll():
    persons = Persons.query.filter_by().all()
    accounts = Accounts.query.filter_by().all()
    return persons, accounts


def getByFname(fname):
    rs = Contacts.query.filter_by(fname=fname).first()
    return rs


def getByUname(uname):
    rs = Accounts.query.filter_by(uname=uname).first()
    return rs


def getAllDistinct():
    rs = db.session.query(Attendance.pid).distinct(Attendance.pid).order_by(Attendance.temp).all()
    return rs


def getAllTemp():
    rs = db.session.query(Attendance.pid, Attendance.temp).distinct(Attendance.pid).filter(
        Attendance.temp > 37.00).all()
    return rs


def getById(id):
    person = Persons.query.filter_by(id=id).first()
    return person
