from premeddb import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    admin = db.Column(db.String(1))
    schedulers = db.relationship('Scheduler', backref='user', lazy='dynamic')

class Scheduler(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    schedulename = db.Column(db.String(50))
    schedule = db.Column(db.String(200))
    data = db.Column(db.LargeBinary)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Grades(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ogpa = db.Column(db.String(5))
    sgpa = db.Column(db.String(5))


class Mcat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    examdate = db.Column(db.String(15))
    overall = db.Column(db.String(5))
    cp = db.Column(db.String(5))
    cars = db.Column(db.String(5))
    bb = db.Column(db.String(5))
    ps = db.Column(db.String(5))


class References(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    type = db.Column(db.String(50))
    status = db.Column(db.String(500))


class Activities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity = db.Column(db.String(50))
    type = db.Column(db.String(50))
    hours = db.Column(db.String(50))
    reference = db.Column(db.String(50))
    startdate = db.Column(db.String(50))
    enddate = db.Column(db.String(50))
    description = db.Column(db.String(10000))


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    university = db.Column(db.String(50))
    primary = db.Column(db.String(50))
    secondary = db.Column(db.String(50))
    interview = db.Column(db.String(50))
    offer = db.Column(db.String(50))
    essay1p = db.Column(db.String(500))
    essay1a = db.Column(db.String(10000))
    essay2p = db.Column(db.String(500))
    essay2a = db.Column(db.String(10000))
    essay3p = db.Column(db.String(500))
    essay3a = db.Column(db.String(10000))
    essay4p = db.Column(db.String(500))
    essay4a = db.Column(db.String(10000))
    essay5p = db.Column(db.String(500))
    essay5a = db.Column(db.String(10000))


class Personal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    essay = db.Column(db.String(10000))