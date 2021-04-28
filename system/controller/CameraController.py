from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from ..model.schema import db, Camera
from .AuthController import login_required


camera = Blueprint('camera', __name__, url_prefix='/camera', template_folder='templates')

@camera.route('/', methods=['POST','GET'])
@login_required
def index():
    cameras = getAll()
    if request.method == 'POST':

        for form in request.form:
            if request.form[form] is None:
                message = ("Missing field: " + str(form), 'warning')
                flashHandler(message)

        name = request.form['Camera Name']
        desc = request.form['Description']
        url = request.form['URL']

        rs = getByName(name)
        if rs is not None:
            message = ('Camera {} already exist.'.format(name), 'warning')
            flashHandler(message)
        else:
            try:
                person = Camera(name, desc, url)
                createRecord(person)
                message = ('Camera {} successfully added!.'.format(name), 'success')
                flashHandler(message)
                return redirect(url_for('camera.index'))
            except Exception as e:
                message = ('Internal Error! unable to execute request.', 'danger')
                flashHandler(message)

    return render_template('camera/index.html', cameras=cameras)

@camera.route('/update/<id>', methods=['POST', 'GET'])
@login_required
def update(id):
    camera = getById(id)
    if request.method == 'POST':
        for form in request.form:
            if request.form[form] is None:
                message = ("[ WARNING ] Missing field: " + str(form), 'warning')
                flashHandler(message)

        try:
            camera.name = request.form['Camera Name']
            camera.desc = request.form['Description']
            camera.url = request.form['URL']

            db.session.commit()
            message = ('Camera {} successfully updated!.'.format(camera.name), 'success')
            flashHandler(message)
        except Exception as e:
            message = ('Internal Error! unable to execute request.', 'danger')
            flashHandler(message)

    return render_template('camera/update.html', camera=camera)


@camera.route('/delete/<id>', methods=['GET'])
@login_required
def delete(id):
    camera = getById(id)
    deleteRecord(camera)
    message = ('Camera {} successfully deleted!.'.format(camera.name), 'success')
    flashHandler(message)
    return redirect(url_for('camera.index'))

def createRecord(name):
    db.session.add(name)
    db.session.commit()


def deleteRecord(name):
    db.session.delete(name)
    db.session.commit()


def getByName(name):
    rs = Camera.query.filter_by(name=name).first()
    return rs

def getById(id):
    rs = Camera.query.filter_by(id=id).first()
    return rs

def getAll():
    rs = Camera.query.order_by(Camera.name).all()
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
