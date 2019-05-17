import matplotlib.pyplot as plt
from flask import flash
from jobplus.models import *
from collections import Counter
from pandas import DataFrame
import os
from pylab import *
import pymysql

mpl.rcParams['font.sans-serif'] = ['SimHei']
conn = pymysql.Connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='123456',
    db='liyang',
    charset='utf8'
)
cursor = conn.cursor()


def all_analysis():
    if os.path.exists('./jobplus/static/all.png'):
        os.remove('./jobplus/static/all.png')
    job = Job.query.all()
    job_list = []
    for i in job:
        job_list.append(i.location.split('·')[0])
    con = Counter(job_list).most_common(10)
    data = DataFrame(con)
    x = data[0]
    y = data[1]*10
    plt.xlabel(u'热点城市')
    plt.ylabel(u'在招职位数量')
    plt.title(u'热点城市职位统计')
    plt.bar(x, y)
    for a, b in zip(x, y):
        plt.text(a, b, '%.0f' % b, ha='center', va='bottom', fontsize=12, color='red')
    plt.savefig('./jobplus/static/all.png', dpi=300, bbox_inches='tight')


def city_analysis(city):
    if os.path.exists('./jobplus/static/city.png'):
        os.remove('./jobplus/static/city.png')
    search = '%' + city + '%'
    sql = "SELECT LOCATION,ID FROM JOB WHERE LOCATION LIKE '%s'" % search
    cursor.execute(sql)
    rr = cursor.fetchall()
    location_list = []
    for row in rr:
        location_list.append(row)
    orign_data = DataFrame(location_list)
    data1 = orign_data.groupby(0).sum()[:10]
    labels = [i for i in data1.index]
    fig = plt.figure(0)
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title(u'区域招聘热度', fontsize=14, color='red')
    plt.pie(data1[1], labels=labels, autopct='%3.1f%%')
    plt.legend(loc='upper right', bbox_to_anchor=(0, 1))
    plt.savefig('./jobplus/static/city.png', dpi=300, bbox_inches='tight')


def more_analysis(city, job):
    if os.path.exists('./jobplus/static/more.png'):
        os.remove('./jobplus/static/more.png')
    search_city = '%' + city + '%'
    search_job = '%' + job + '%'
    sql = "SELECT NAME,WAGE_HIGH FROM (SELECT * FROM JOB WHERE LOCATION LIKE '%s') a WHERE NAME LIKE '%s'" % (search_city, search_job)
    cursor.execute(sql)
    rr = cursor.fetchall()
    more_list = []
    for row in rr:
        more_list.append(row)
    data = DataFrame(more_list)
    data = data.groupby(0).max().sort_values(by=1)
    x = data.index
    y = data[1]
    fig = plt.figure(0)
    ax = fig.add_subplot(1, 1, 1)
    ax.axes.set_xticklabels(x, rotation=40, fontsize=8)
    ax.set_title('薪资排行榜', color='red')
    ax.set_ylabel('薪资/k')
    plt.bar(x, y, width=0.5)
    for a, b in zip(x, y):
        plt.text(a, b, '%sk' % b, ha='center', va='bottom', fontsize=15, color='red')
    plt.savefig('./jobplus/static/more.png', dpi=300, bbox_inches='tight')

