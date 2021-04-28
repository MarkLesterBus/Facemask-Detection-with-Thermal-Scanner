from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Persons(db.Model):
    __tablename__ = "persons"

    id = db.Column('id', db.Integer, unique=True, primary_key=True, nullable=False)
    pid = db.Column('pid', db.String, unique=True, nullable=False)
    pimg = db.Column('pimg', db.String, unique=True, nullable=False)
    path = db.Column('path', db.String, nullable=False)
    fname = db.Column('fname', db.String, nullable=False)
    lname = db.Column('lname', db.String, nullable=False)
    age = db.Column('age', db.String, nullable=False)
    gender = db.Column('gender', db.String, nullable=False)
    bdate = db.Column('bdate', db.String, nullable=False)
    email = db.Column('email', db.String, nullable=False, unique=True)
    phone_no = db.Column('phone_no', db.String, nullable=True)
    cell_no = db.Column('cell_no', db.String, nullable=True)
    address = db.Column('address', db.String, nullable=False)
    contacts = db.relationship('Contacts', backref='persons', lazy='dynamic')
    accounts = db.relationship('Accounts', backref='persons', lazy='dynamic')

    def __init__(self, pid, pimg, path, fname, lname, age, gender, bdate, email, phone_no, cell_no, address):
        self.pid = pid
        self.pimg = pimg
        self.path = path
        self.fname = fname
        self.lname = lname
        self.age = age
        self.gender = gender
        self.bdate = bdate
        self.email = email
        self.phone_no = phone_no
        self.cell_no = cell_no
        self.address = address

    def __repr__(self):
        return "<Name: {} {}>".format(self.fname, self.lname)


class Contacts(db.Model):
    __tablename__ = "contacts"  # Must be defined the table name

    id = db.Column('id', db.Integer, unique=True, primary_key=True, nullable=False)
    fname = db.Column('fname', db.String, nullable=False)
    email = db.Column('email', db.String, nullable=False, unique=True)
    phone_no = db.Column('phone_no', db.String, nullable=False)
    cell_no = db.Column('cell_no', db.String, nullable=False)
    address = db.Column('address', db.String, nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'), nullable=False)

    def __init__(self, fname, email, phone_no, cell_no, address, person_id):
        self.fname = fname
        self.email = email
        self.phone_no = phone_no
        self.cell_no = cell_no
        self.address = address
        self.person_id = person_id

    def __repr__(self):
        return "<Contact: {} {}>".format(self.fname, self.phone_no)

class Accounts(db.Model):

    __tablename__ = "accounts"

    id = db.Column('id', db.Integer, unique=True, primary_key=True, nullable=False)
    uname = db.Column('uname', db.String,unique=True, nullable=False)
    pword = db.Column('pword', db.String, nullable=False, unique=True)
    utype = db.Column('utype', db.String, nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'),nullable=False)

    def __init__(self, uname, pword, utype, person_id):
        self.uname = uname
        self.pword = pword
        self.utype = utype
        self.person_id = person_id

    def __repr__(self):
        return "<User: {}>".format(self.uname)


class Attendance(db.Model):
    __tablename__ = "attendance"

    id = db.Column('id', db.Integer, unique=True, primary_key=True, nullable=False)
    pid = db.Column('pid', db.String, db.ForeignKey('persons.pid'), nullable=False)
    temp = db.Column('temp', db.String, nullable=False)
    time = db.Column('time', db.String, nullable=False)
    date = db.Column('date', db.String, nullable=False)


    def __init__(self, pid, temp, time, date):
        self.pid = pid
        self.temp = temp
        self.time = time
        self.date = date

    def __repr__(self):
        return "<Attendance: {} {}>".format(self.pid, self.temp)
