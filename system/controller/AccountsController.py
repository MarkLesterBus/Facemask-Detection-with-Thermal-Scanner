from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from .AuthController import login_required
from ..model.schema import db, Accounts

accounts = Blueprint('accounts', __name__, url_prefix='/system/accounts', template_folder='templates')


@accounts.route('/', methods=['POST', 'GET'])
@login_required
def index():
    accounts = getAll()
    # if request.method == 'POST':
    #
    #     for form in request.form:
    #         if request.form[form] is None:
    #             message = ("[ WARNING ] Missing field: " + str(form), 'warning')
    #             flashHandler(message)
    #
    #     uname = request.form['Username']
    #     pword = generate_password_hash(request.form['Password'])
    #     utype = request.form['Utype']
    #
    #     rs = getByUname(uname)
    #     if rs is not None:
    #         message = ('Username {} already exist.'.format(uname), 'warning')
    #         flashHandler(message)
    #     else:
    #         try:
    #             account = Accounts(uname, pword, utype, id)
    #             createRecord(account)
    #             message = ('Account: {} successfully added!.'.format(uname), 'success')
    #             flashHandler(message)
    #             return redirect(url_for('accounts.index', id=id))
    #         except Exception as e:
    #             message = ('Internal Error! unable to execute request.', 'danger')
    #             print(e)
    #             flashHandler(message)
    utype = session.get('account_type')
    return render_template('accounts/index.html', accounts=accounts, id=id, utype=utype)


@accounts.route('/delete/<id>', methods=['GET'])
@login_required
def delete(id):
    account = getById(id)
    deleteRecord(account)
    message = ('Account {} successfully deleted!.'.format(account.uname), 'success')
    flashHandler(message)
    return redirect(url_for('accounts.index', id=id))


def createRecord(account):
    db.session.add(account)
    db.session.commit()


def deleteRecord(account):
    db.session.delete(account)
    db.session.commit()

def getById(id):
    rs = Accounts.query.filter_by(id=id).first()
    return rs

def getByUname(uname):
    rs = Accounts.query.filter_by(uname=uname).first()
    return rs

def getAll():
    rs = Accounts.query.order_by(Accounts.uname).all()
    return rs

def getAllById(id):
    rs = Accounts.query.order_by(Accounts.uname).filter_by(person_id=id).all()
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