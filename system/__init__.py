from flask import Flask
from flask_toastr import Toastr
from .controller.PersonsController import persons
from .controller.ProfileController import profile
from .controller.ContactsController import contacts
from .controller.AccountsController import accounts
from .controller.AuthController import auth
from .controller.DashboardController import dashboard
from .controller.AttendanceController import attendance
from .model.schema import db, Persons

toastr = Toastr()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("config.Config")

    toastr.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()

        if test_config is None:
            # load the instance config, if it exists, when not testing
            app.config.from_pyfile('config.py', silent=True)
        else:
            # load the test config if passed in
            app.config.from_mapping(test_config)

        app.register_blueprint(auth)
        app.add_url_rule('/system/auth', endpoint='auth.login')
        app.register_blueprint(persons)
        app.add_url_rule('/system/persons', endpoint='persons.index')
        app.register_blueprint(profile)
        app.add_url_rule('/system/profile', endpoint='profile.index')
        app.register_blueprint(contacts)
        app.add_url_rule('/system/contacts', endpoint='contacts.index')
        app.register_blueprint(accounts)
        app.add_url_rule('/system/accounts', endpoint='accounts.index')
        app.register_blueprint(attendance)
        app.add_url_rule('/attendance', endpoint='attendance.index')
        app.register_blueprint(dashboard)
        app.add_url_rule('/', endpoint='dashboard.index')

    return app
