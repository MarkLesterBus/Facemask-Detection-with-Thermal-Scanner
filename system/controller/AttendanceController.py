from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from ..model.schema import db, Attendance, Persons
from .AuthController import login_required
from datetime import datetime
attendance = Blueprint('attendance', __name__, url_prefix='/attendance', template_folder='templates')


@attendance.route('/', methods=['POST', 'GET'])
@login_required
def index():
    if request.method == 'POST':
        date = request.form['datetime']
        if date != "":
            date = datetime.strptime(date, '%Y-%m-%d').date()
            logs = db.session.query(Attendance, Persons).filter_by(date=date).outerjoin(Persons, Persons.pid == Attendance.pid).all()
        else:
            logs = db.session.query(Attendance, Persons).outerjoin(Persons, Persons.pid == Attendance.pid).order_by(
                Attendance.id).all()
    else:
        logs = db.session.query(Attendance, Persons).outerjoin(Persons, Persons.pid == Attendance.pid).order_by(
            Attendance.id).all()
    return render_template('attendance/index.html', logs=logs)

