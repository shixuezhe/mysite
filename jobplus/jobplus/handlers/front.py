from flask import Blueprint, url_for, render_template, flash, redirect
from jobplus.models import User, Company, Job, Resume
from jobplus.forms import LoginForm, Phone_RegisterForm, AnalysisForm
from flask_login import login_user, logout_user, login_required
from jobplus.analysis import city_analysis, all_analysis


front = Blueprint('front', __name__)


@front.route('/')
def index():
    job_list = Job.query.order_by(Job.created_at.desc()).limit(6)
    company_list = Company.query.order_by(Company.created_at.desc()).limit(6)
    for company in company_list:
        job_num = Job.query.filter_by(company_id=company.id).all()
        number = len(job_num)
    return render_template('index.html', job_list=job_list, company_list=company_list, number=number)


@front.route('/phoneregister', methods=['GET', 'POST'])
def phone_register():
    form = Phone_RegisterForm()
    if form.validate_on_submit():
        if not form.code.data:
            global a
            a = form.send_code(form.phone.data)
            flash('发送验证码成功，请注意查收', 'success')
        elif form.code.data and form.code.data == a:
            form.create_user()
            flash('注册成功，请登录', 'success')
            return redirect(url_for('front.choice'))

    return render_template('phone_register.html', form=form, active='phone')


@front.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(phone_number=form.phone.data).first()
        if not Resume.query.filter_by(id=user.id).first():
            form.create_resume(user)
        login_user(user, form.remember_me.data)
        flash('登录成功', 'success')
        if user.is_admin:
            return redirect(url_for('admin.user_manage'))
        else:
            return redirect(url_for('front.choice'))
    return render_template('login.html', form=form)


@front.route('/choice')
@login_required
def choice():
    return render_template('choice.html')


@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('退出登录成功', 'success')
    return redirect(url_for('.index'))


@front.route('/login_admin')
def login_admin():
    user = User.query.filter_by(phone_number='18048903250').first()
    login_user(user)
    flash('登录管理员后台成功，点击控制台查看', 'success')
    return redirect(url_for('front.index'))


@front.route('/login_company')
def login_company():
    user = user = User.query.filter_by(phone_number='13512345678').first()
    login_user(user)
    flash('登录企业端后台成功，点击控制台查看', 'success')
    return redirect(url_for('front.index'))