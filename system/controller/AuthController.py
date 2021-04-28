import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from ..model.schema import db, Accounts, Persons
auth = Blueprint('auth', __name__, url_prefix='/system/auth', template_folder='templates')

@auth.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        for form in request.form:
            if request.form[form] == "":
                message = ("Missing field: " + str(form), 'warning')
                flashHandler(message)

        uname = request.form['Username']
        pword = request.form['Password']

        account = Accounts.query.filter_by(uname=uname).first()
        if account is None:
            message = ("Unknown Username {}".format(uname), 'warning')
            flashHandler(message)
        elif not check_password_hash(account.pword, pword):
            message = ("Incorrect password", 'warning')
            flashHandler(message)
        else:
            session.clear()
            session['account_id'] = account.id
            session['account_type'] = account.utype
            message = ("Incorrect password", 'Success')
            flashHandler(message)
            return redirect(url_for('dashboard.index'))

    return render_template('auth/login.html')



@auth.before_app_request
def load_logged_in_user():
    account_id = session.get('account_id')
    if account_id is None:
        g.user = None
    else:
        g.user = db.session.query(Accounts, Persons).outerjoin(Persons, Accounts.person_id == Persons.id).filter_by(id=account_id).first()


@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


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