from flask import render_template,Blueprint,request,current_app,flash,url_for,redirect
from jobplus.decorators import admin_required
from jobplus.models import User,db,Company
from jobplus.forms import User_RegisterForm,Company_RegisterForm,CompanyEditForm,UserEditForm

admin = Blueprint('admin',__name__,url_prefix='/admin')

@admin.route('/')
@admin_required
def index():
    return render_template('admin/index.html',active='admin')

@admin.route('/user')
@admin_required
def user_manage():
    page = request.args.get('page',default=1,type=int)
    pagination = User.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/user_manage.html',pagination=pagination)

@admin.route('/company')
@admin_required
def company_manage():
    page = request.args.get('page',default=1,type=int)
    pagination = Company.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/company_manage.html',pagination=pagination)

@admin.route('/user/create',methods=['GET','POST'])
@admin_required
def create_user():
    form = User_RegisterForm()
    if form.is_submitted():
        form.create_user()
        flash('用户创建成功', 'success')
        return redirect(url_for('admin.user_manage'))
    return render_template('admin/create_user.html', form=form)

@admin.route('/company/create',methods=['GET','POST'])
@admin_required
def create_company():
    form=Company_RegisterForm()
    if form.validate_on_submit():
        form.create_company()
        flash('企业创建成功','success')
        return redirect(url_for('admin.company_manage'))
    return render_template('admin/create_company.html',form=form)


@admin.route('/user/<user_id>/edit',methods=['GET','POST'])
@admin_required
def user_edit(user_id):
    user = User.query.get_or_404(user_id)
    form = UserEditForm()
    if form.validate_on_submit():
        form.update_user(user)
        flash('用户信息更新成功','success')
        return redirect(url_for('admin.user_manage'))
    return render_template('admin/user_edit.html',form=form,user=user)

@admin.route('/company/<company_id>/edit',methods=['GET','POST'])
@admin_required
def company_edit(company_id):
    company=Company.query.get_or_404(company_id)
    form = CompanyEditForm(obj=company)
    if form.validate_on_submit():
        form.update_company(company)
        flash('企业信息更新成功','success')
        return redirect(url_for('admin.company_manage'))
    return render_template('admin/company_edit.html',form=form,company=company)

@admin.route('/user/<user_id>/delete',methods=['GET','POST'])
@admin_required
def user_delete(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('用户删除成功','success')
    return redirect(url_for('admin.user_manage'))

@admin.route('/company/<company_id>/delete',methods=['GET','POST'])
@admin_required
def company_delete(company_id):
    company=Company.query.get_or_404(company_id)
    db.session.delete(company)
    db.session.commit()
    flash('企业删除成功','success')
    return redirect(url_for('admin.company_manage'))
