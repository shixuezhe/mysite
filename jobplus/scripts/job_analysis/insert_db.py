import json
from analysis.web.models import *

job_list = []
with open('data.json', 'r') as f:
    jobs = json.load(f)
    for i in jobs:
        job_list.append(i)


def iter_jobs():
    for job in job_list:
        yield Job(
            title=job['title'],
            city=job['city'],
            area=job['area'],
            experience=job['experience'],
            education=job['education'],
            salary_lower=job['salary_lower'],
            salary_upper=job['salary_upper'],
            tags=' '.join(job['tags']),
            company=job['company']
        )


def run():
    for job in iter_jobs():
        db.session.add(job)
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()


if __name__ == '__main__':
    run()
