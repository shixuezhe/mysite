from flask import render_template, Blueprint, request, current_app, redirect, flash, url_for
from jobplus.models import Job, Company, Delivery,db
from datetime import datetime
from flask_login import login_required,current_user

job = Blueprint('job', __name__, url_prefix='/job')


@job.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    pagination = Job.query.order_by(Job.created_at.desc()).paginate(
        page=page,
        per_page=current_app.config['INDEX_PER_PAGE'],
        error_out=False
    )
    return render_template('job/index.html', pagination=pagination, active='job')


@job.route('/<int:job_id>')
def detail(job_id):
    job = Job.query.get_or_404(job_id)
    time = datetime.now()
    return render_template('job/detail.html', job=job, job_id=job_id, time=time)


@job.route('/<int:job_id>/resume')
@login_required
def resume(job_id):
    user = current_user
    job = Job.query.get_or_404(job_id)
    if user.is_user:
        delivery = Delivery.query.get(job_id)
        if delivery:
            flash('您已经投递过该职位了', 'success')
            return redirect(url_for('job.detail', job_id=job_id))
        else:
            delivery = Delivery(job_id=job_id, user_id=user.id, company_id=job.companies.id)
            db.session.add(delivery)
            db.session.commit()
            flash('简历投递成功', 'success')
            return redirect(url_for('job.detail', job_id=job_id))
    else:
        flash('个人用户才能投递简历','success')
        return redirect(url_for('job.detail', job_id=job_id))


@job.route('/analysis')
def analysis():
    return render_template('job/analysis.html')


@job.route('/top10_city')
def top10_city():
    return render_template('job/top10_city.html')


@job.route('/top10_salary')
def top10_salary():
    return render_template('job/top10_salary.html')


@job.route('/top10_tags')
def top10_tags():
    return render_template('job/top10_tags.html')


@job.route('/experience')
def experience():
    return render_template('job/expeience.html')


@job.route('/degree')
def degree():
    return render_template('job/degree.html')


@job.route('/degree_salary')
def degree_salary():
    return render_template('job/degree_salary.html')
