from flask import Blueprint,url_for,render_template,flash,redirect
from flask import current_app,request
from jobplus.models import User,Company,Job
from jobplus.forms import User_RegisterForm,Company_RegisterForm,LoginForm,Phone_RegisterForm,CodeForm
from flask_login import login_user,logout_user,login_required
from jobplus.send_code import send_code
from faker import Faker

fake = Faker()
front=Blueprint('front',__name__)

@front.route('/')
def index():
    job_list = Job.query.order_by(Job.created_at.desc()).limit(6)
    company_list = Company.query.order_by(Company.created_at.desc()).limit(6)
    for company in company_list:
        job_num = Job.query.filter_by(company_id=company.id).all()
        number = len(job_num)
    return render_template('index.html',job_list=job_list,company_list=company_list,number=number)

@front.route('/userregister',methods=['GET','POST'])
def userregister():
    form=User_RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('注册成功，请登录','success')
        return redirect(url_for('front.login'))
    return render_template('user_register.html',form=form,active='email')

@front.route('/phoneregister',methods=['GET','POST'])
def phoneregister():
    form1 = Phone_RegisterForm()
    form2 = CodeForm()
    if form1.validate_on_submit():
        send_code(form1.phone.data)
        flash('验证码发送成功，请及时查收','success')
        if form2.validate_on_submit():
            if form2.code.data == code:
                form1.create_user()
                flash('注册成功，请登录','success')
                return redirect(url_for('front.login'))
            else:
                flash('验证码错误','success')
    return render_template('phone_register.html',form1=form1,form2=form2,active='phone')

@front.route('/companyregister',methods=['GET','POST'])
def companyregister():
    form=Company_RegisterForm()
    if form.validate_on_submit():
        form.create_company()
        flash('注册成功，请登录','success')
        return redirect(url_for('front.login'))
    return render_template('company_register.html',form=form)

@front.route('/login',methods=['POST','GET'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        login_user(user,form.remember_me.data)
        if user.is_admin:
            return redirect(url_for('admin.index'))
        if user.is_company:
            return redirect(url_for('company.companyprofile'))
        else:
            form.create_resume(user)
            return redirect(url_for('user.userprofile'))
    return render_template('login.html',form=form)

@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('退出登录成功','success')
    return redirect(url_for('.index'))
