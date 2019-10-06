import datetime
from flask_login import UserMixin
from project import db, login_manager


########################################################################################################################
###############################################* LOGIN MANAGER *########################################################
########################################################################################################################
@login_manager.user_loader
def user_load(id):
    return Users.query.get(id)
########################################################################################################################


########################################################################################################################
#####################################################* USERS *##########################################################
########################################################################################################################
class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(64))
    hashed_password = db.Column(db.String(256))
    mobile_number = db.Column(db.String(12), nullable=False)
    email = db.Column(db.String(128), unique=True, index=True)
    register_date = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    storage = db.relationship('Storage', backref='users', lazy=True)
########################################################################################################################


########################################################################################################################
#################################################* STORAGE *############################################################
########################################################################################################################
class Storage(db.Model):
    __tablename__ = 'storage'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    file = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(1000), nullable=False, unique=True)
########################################################################################################################