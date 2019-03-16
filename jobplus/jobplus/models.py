from flask import url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

class User(Base,UserMixin):
    __tablename__ = 'user'
    ROLE_USER = 10
    ROLE_COMPANY = 20
    ROLE_ADMIN = 30
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(32),unique=True,index=True,nullable=False)
    email = db.Column(db.String(64),unique=True,index=True,nullable=False)
    _password = db.Column('password',db.String(256),nullable=False)
    phone_number = db.Column(db.Integer)
    resume = db.Column(db.String(128))
    experience = db.Column(db.String(24))
    role = db.Column(db.SmallInteger,default=ROLE_USER)
    jobs = db.relationship('Job', backref='user')
    detail = db.relationship('Company',uselist=False)

    def __repr__(self):
        return '<User:{}>'.format(self.username)

    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self,orig_password):
        self._password = generate_password_hash(orig_password)

    def check_password(self,password):
        return check_password_hash(self._password, password)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_company(self):
        return self.role == self.ROLE_COMPANY

    @property
    def is_user(self):
        return self.role == self.ROLE_USER
    

class Company(Base):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(128),unique=True,index=True,nullable=False)
    email = db.Column(db.String(64),nullable=False)
    number = db.Column(db.String(48),nullable=False)
    slug = db.Column(db.String(64),unique=True,index=True)
    address = db.Column(db.String(128))
    site = db.Column(db.String(64))
    logo = db.Column(db.String(128))
    description = db.Column(db.String(64))
    details = db.Column(db.Text())
    finance = db.Column(db.String(32))
    type = db.Column(db.String(32))
    staff_num =db.Column(db.String(32))
    location = db.Column(db.String(32))
    users_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'))
    users = db.relationship('User',uselist=False,backref=db.backref('companies',uselist=False))

    def __repr__(self):
        return '<Company {}>'.format(self.name)
    @property
    def url(self):
        return url_for('company.detail',company_id=self.id)
    
class Job(Base):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),nullable=False)
    wage_low = db.Column(db.Integer,nullable=False)
    wage_high = db.Column(db.Integer,nullable=False)
    location = db.Column(db.String(32),nullable=False)
    tags = db.Column(db.String(64))
    experience = db.Column(db.String(64))
    degree = db.Column(db.String(64))
    is_fulltime = db.Column(db.Boolean,default=True)
    is_open = db.Column(db.Boolean,default=True)
    description = db.Column(db.Text())
    company_id = db.Column(db.Integer,db.ForeignKey('company.id',ondelete='CASCADE'))
    companies = db.relationship('Company',uselist=False,backref=db.backref('jobs'))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id', ondelete='CASCADE'))
    view_count = db.Column(db.Integer,default=0)
    
    def __repr__(self):
        return '<Job:{}>'.format(self.name)

    @property
    def url(self):
        return url_for('job.detail',job_id=self.id)

class Resume(Base):
    __tablename__ = 'resume'
    id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),primary_key=True)
    name = db.Column(db.String(32),nullable=False)
    age = db.Column(db.SmallInteger)
    work_age = db.Column(db.SmallInteger)
    home_city = db.Column(db.String(64))
    job_experience = db.Column(db.Text)
    edu_experience = db.Column(db.Text)
    project_experience = db.Column(db.Text)
    resume_url = db.Column(db.String(128))

class Delivery(Base):
    STATUS_WAITING = 1
    STATUS_ACCEPT = 2
    STATUS_REJECT = 3

    id = db.Column(db.Integer,primary_key=True)
    job_id = db.Column(db.Integer,db.ForeignKey('job.id',ondelete='CASCADE'))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'))
    job = db.relationship('Job', uselist=False, backref=db.backref('job_resume', uselist=False))
    user = db.relationship('User', uselist=False, backref=db.backref('user_resume', uselist=False))
    company_id = db.Column(db.Integer)
    status = db.Column(db.SmallInteger,default=STATUS_WAITING)

