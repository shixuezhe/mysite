from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextField,ValidationError
from wtforms.validators import Required,Length,EqualTo,URL,Email
from jobplus.models import db,User,Company,Job,Delivery,Resume

class User_RegisterForm(FlaskForm):
    username = StringField('用户名',validators=[Required(),Length(3,24)])
    email = StringField('邮箱',validators=[Required(),Email()])
    password = PasswordField('密码',validators=[Required(),Length(6,24)])
    repeat_password = PasswordField('重复密码',validators=[Required(),EqualTo('password')])
    submit = SubmitField('提交')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已存在')

    def create_user(self):
        user = User()
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user

class Company_RegisterForm(FlaskForm):
    username = StringField('企业名称',validators=[Required(),Length(3,24)])
    email = StringField('邮箱',validators=[Required(),Email()])
    password = PasswordField('密码',validators=[Required(),Length(6,24)])
    repeat_password = PasswordField('重复密码',validators=[Required(),EqualTo('password')])
    submit = SubmitField('提交')

    def validate_name(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('企业已存在')
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已存在')

    def create_company(self):
        user = User(
                username=self.username.data,
                email=self.email.data,
                password=self.password.data,
                role=20
                )
        db.session.add(user)
        db.session.commit()
        return user

class LoginForm(FlaskForm):
    email = StringField('邮箱',validators=[Required(),Email()])
    password = PasswordField('密码',validators=[Required(),Length(6,24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_email(self,field):
        if field.data and not User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱未注册')

    def validate_password(self,field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')

    def create_resume(self,user):
        resume = Resume(id=user.id,name=user.username)
        db.session.add(resume)
        db.session.commit()
        return resume

class UserProfileForm(FlaskForm):
    username = StringField('用户名',validators=[Required(),Length(3,24)])
    email = StringField('邮箱',validators=[Required(),Email()])
    password = PasswordField('密码',validators=[Required(),Length(6,24)])
    phone_number = StringField('手机号',validators=[Required(),Length(11)])
    resume = StringField('简历链接',validators=[Required(),URL()])
    experience = StringField('工作年限')
    submit = SubmitField('提交')
    
    def validate_phone(self,field):
        if field.data[0] is not 1 and len(field.data) != 11:
            raise ValidationError('请输入正确11位手机号码')

    def update_user(self,user):
        user.username = self.username.data
        user.email = self.email.data
        if self.password.data:
            user.password = self.password.data
        user.phone_number = self.phone_number.data
        user.resume = self.resume.data
        user.experience = self.experience.data
        db.session.add(user)
        db.session.commit()

class CompanyProfileForm(FlaskForm):
    name = StringField('企业名称',validators=[Required(),Length(3,24)])
    email = StringField('邮箱',validators=[Required(),Email()])
    number = StringField('手机号',validators=[Required(),Length(11)])
    password = PasswordField('密码',validators=[Required(),Length(6,24)])
    slug = StringField('Slug',validators=[Length(3,24)])
    address = StringField('公司地址',validators=[Required(),Length(2,36)])
    site = StringField('公司网址',validators=[Length(9,36)])
    logo = StringField('logo',validators=[Required(),URL()])
    description = StringField('概述',validators=[Length(0,24)])
    details = TextField('公司详情',validators=[Length(0,256)])
    submit = SubmitField('提交')

    def validate_phone(self,field):
        if field.data[0] is not 1 and len(field.data) != 11:
            raise ValidationError('please input correct phone number')

    def update_company(self,user):
        user.username = self.name.data
        user.email = self.email.data
        if self.password.data:
            user.password = self.password.data
        if user.companies:
            companies = user.companies
        else:
            companies = Company()
            companies.users_id = user.id
        self.populate_obj(companies)
        db.session.add(user)
        db.session.add(companies)
        db.session.commit()

class UserEditForm(FlaskForm):
    username = StringField('用户名')
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required(), Length(6, 24)])
    phone_number = StringField('手机号')
    submit = SubmitField('提交')

    def update_user(self,user):
        self.populate_obj(user)
        if self.password.data:
           user.password=self.password.data
        db.session.add(user)
        db.session.commit()

class CompanyEditForm(FlaskForm):
    name = StringField('企业名称')
    email = StringField('邮箱', validators=[Required(), Email()])
    number = StringField('手机号')
    password = PasswordField('密码', validators=[Required(), Length(6, 24)])
    address = StringField('公司地址')
    description = StringField('概述')
    submit = SubmitField('提交')

    def update_company(self,company):
        company.name = self.name.data
        company.email = self.email.data
        if self.password.data:
            company.password = self.password.data
        if company.users:
            users = company.users
        else:
            user = User()
            user.id = company.users_id
        self.populate_obj(user)
        db.session.add(company)
        db.session.add(user)
        db.session.commit()

class JobForm(FlaskForm):
    name = StringField('职位名称',validators=[Required(),Length(2,24)])
    wage_low = StringField('最低薪资',validators=[Required(),Length(1,8)])
    wage_high = StringField('最高薪资',validators=[Required(), Length(1,8)])
    location = StringField('工作地点',validators=[Required(), Length(1,24)])
    tags = StringField('行业标签',validators=[ Length(1,64)])
    experience = StringField('经验要求',validators=[ Length(2,64)])
    degree = StringField('学历要求',validators=[ Length(1,64)])
    is_fulltime = StringField('全职/兼职/实习生',validators=[ Length(1,64)])
    description = StringField('工作描述',validators=[ Length(1,512)])
    submit = SubmitField('提交')

    def create_job(self,company_id):
        job = Job()
        job.company_id = company_id
        self.populate_obj(job)
        db.session.add(job)
        db.session.commit()
        return job

    def update_job(self,job):
        self.populate_obj(job)
        db.session.add(job)
        db.session.commit()
        return job

class ResumeForm(FlaskForm):
    name = StringField('真实姓名',validators=[Required(),Length(2,24)])
    age = StringField('年龄',validators=[Required(),Length(1,8)])
    work_age = StringField('工作年限',validators=[Required(), Length(1,8)])
    home_city = StringField('籍贯',validators=[Required(), Length(1,24)])
    edu_experience = TextField('教育经历',validators=[ Length(1,512)])
    job_experience = TextField('工作经历',validators=[ Length(1,512)])
    project_experience = TextField('项目经历',validators=[ Length(1,512)])
    submit = SubmitField('提交')

    def update_resume(self,resume):
        self.populate_obj(resume)
        db.session.add(resume)
        db.session.commit()
