from flask import Blueprint,url_for,render_template,flash,redirect
from flask import current_app,request
from jobplus.models import User,Company,Job
from jobplus.forms import LoginForm,Phone_RegisterForm
from flask_login import login_user,logout_user,login_required
import random
from jobplus.send_code import send_code

front=Blueprint('front',__name__)

@front.route('/')
def index():
    job_list = Job.query.order_by(Job.created_at.desc()).limit(6)
    company_list = Company.query.order_by(Company.created_at.desc()).limit(6)
    for company in company_list:
        job_num = Job.query.filter_by(company_id=company.id).all()
        number = len(job_num)
    return render_template('index.html',job_list=job_list,company_list=company_list,number=number)

@front.route('/phoneregister',methods=['GET','POST'])
def phone_register():
    form = Phone_RegisterForm()
    if form.validate_on_submit():
        if form.code.data:
            form.create_user()
            flash('注册成功，请登录', 'success')
            return redirect(url_for('front.choice'))
        else:
            form.send_code(form.phone.data)
            flash('发送验证码成功，请注意查收','success')
    return render_template('phone_register.html',form=form,active='phone')


@front.route('/login',methods=['POST','GET'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(phone_number=form.phone.data).first()
        login_user(user,form.remember_me.data)
        flash('登录成功', 'success')
        if user.is_admin:
            return redirect(url_for('admin.user_manage'))
        else:
            return redirect(url_for('front.choice'))

    return render_template('login.html',form=form)

@front.route('/choice')
@login_required
def choice():
    return render_template('choice.html')

@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('退出登录成功','success')
    return redirect(url_for('.index'))
