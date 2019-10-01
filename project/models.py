import datetime
from flask_login import UserMixin
from project import db, login_manager
from werkzeug.security import check_password_hash, generate_password_hash


@login_manager.user_loader
def user_load(user_id):
    return User.query.get(user_id)


# class Department(db.Model):
#     __tablename__ = 'department'
#
#     dept_id = db.Column(db.Interger, primary_key=True)
#     name = db.Column(db.String(20))
#
#
# class Applicant(db.Model, UserMixin):
#     __tablename__ = 'applicant'
#
#     app_id = db.Column(db.Integer(8), primary_key=True)
#     hashed_password = db.Column(db.String(256))
#     email = db.Column(db.String(128), unique=True, index=True)
#     name = db.Column(db.String(64))
#     gender = db.Column(db.String(64))
#     birth_date = db.Column(db.DateTime)
#     status = db.Column(db.String(64))
#
#     resumes = db.relationship('Resume', backref='applicant', lazy=True)
#
#
# class Resume(db.Model):
#     __tablename__ = 'resume'
#
#     resume_id = db.Column(db.INTEGER(8), primary_key=True)
#     resume = db.Column(db.String(256))
#     app_id = db.Column(db.Integer(8), db.ForeignKey('applicant.app_id'), nullable=False)
#
#
# class Employee(db.Model):
#     __tablename__ = 'employee'
#
#     emp_id = db.Column(db.INTEGER(8), primary_key=True)
#     name = db.Column(db.String(256), nullable=False)
#     hire_date = db.Column(db.DateTime)
#     status = db.Column(db.String(10), nullable=False)
#     salary = db.Column(db.Double())
#     app_id = db.Column(db.Integer(8), db.ForeignKey('applicant.app_id'), nullable=False)
#
# create table employee
# 	(emplid			varchar(8),
# 	 name			varchar(20) not null,
# 	 hire_dt		date,
# 	 status			varchar(10) not null
# 	 	check (status in ('Active', 'Inactive')),
# 	 salary			numeric(8,2) check (salary > 29000),
# 	 email			varchar(20),
# 	 deptid			varchar(5),
# 	 primary key (emplid),
# 	 foreign key (deptid) references department(deptid)
# 		on delete set null
# 	);
#####################################################
class User(db.Model,UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String(20), nullable=False, default='default_profile.jpg')
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    hashed_password = db.Column(db.String(128))

    posts = db.relationship('BlogPost', backref='author', lazy=True)

    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.hashed_password = generate_password_hash(password)

    def check_hashed_password(self,password):
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return f"Username {self.username}"


class BlogPost(db.Model):
    __tablename__ = 'blogposts'

    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    title = db.Column(db.Text, nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __init__(self,title,text,user_id):
        self.title = title
        self.text = text
        self.user_id = user_id

    def __repr__(self):
        return f"POST ID: {self.id} -- Date: {self.date}"