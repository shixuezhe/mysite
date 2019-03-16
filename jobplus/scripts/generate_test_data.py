import os,json,random
from random import randint
from faker import Faker
from jobplus.models import db,User,Company,Job

fake = Faker('zh_CN')
data_company = []
company_name = []

with open(os.path.join(os.path.dirname(__file__),'..','datas','company.json')) as f:
    companies = json.load(f)
    for i in companies:
        if i not in data_company:
            data_company.append(i)
            company_name.append(i['name'])

def iter_users():
    for company in data_company:
        yield User(
            username=company['name'],
            email=fake.email(),
            password='123456',
            role=20
        )

def iter_companys():
    for com in data_company:
        users = User.query.filter_by(username=com['name']).first()
        yield Company(
            users_id=users.id,
            name=com['name'],
            email=users.email,
            number=fake.phone_number(),
            address=fake.address(),
            logo=com['logo'],
            finance=com['finance'],
            type=com['type'],
            staff_num=com['staff_num'],
            description=com['description']
        )

def iter_jobs():
    id_list = []
    companies = Company.query.all() 
    for i in companies:
        id_list.append(i.id)
    with open(os.path.join(os.path.dirname(__file__),'..','datas','job.json')) as f:
        for job in json.load(f):
            yield Job(
                company_id=random.choice(id_list),
                name=job['name'],
                wage_low=job['wage_low'],
                wage_high=job['wage_high'],
                location=job['location'],
                experience=job['experience'],
                degree=job['degree'],
                tags=','.join(job['tags'])
            )


def run():
    for user in iter_users():
        db.session.add(user)
    for company in iter_companys():
        db.session.add(company)
    for job in iter_jobs():
        db.session.add(job)
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
