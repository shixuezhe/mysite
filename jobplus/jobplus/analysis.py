import matplotlib.pyplot as plt
from flask import flash
from jobplus.models import *
from collections import Counter
from pandas import DataFrame
import pandas as pd
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
    y = data[1] * 10
    plt.xlabel(u'热点城市')
    plt.ylabel(u'在招职位数量')
    plt.title(u'热点城市职位统计')
    plt.bar(x, y)
    for a, b in zip(x, y):
        plt.text(a, b, '%.0f' % b, ha='center', va='bottom', fontsize=7, color='red')
    plt.savefig('./jobplus/static/all.png')


def city_analysis(city):
    if os.path.exists('./jobplus/static/city.png'):
        os.remove('./jobplus/static/city.png')
    search = city + '%'
    sql = "SELECT NAME,WAGE_HIGH,LOCATION FROM JOB WHERE LOCATION LIKE '%s' ORDER BY WAGE_HIGH DESC " % search
    cursor.execute(sql)
    rr = cursor.fetchall()
    #处理数据
    job_list = []
    for row in rr:
        job_list.append(row)
    orign_data = DataFrame(job_list, columns=['name', 'wage_high', 'location'])
    data_location = orign_data['location']
    data_location_count = data_location.apply(pd.value_counts).max()
    data_job_salary = orign_data[['name', 'wage_high']][:10]
    #招聘热度绘图
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.set_title(u'区域招聘前五', fontsize=12, color='red')
    plt.pie(data_location_count.values[:5], labels=data_location_count.index[:5], autopct='%3.1f%%')
    plt.legend(loc='upper right', bbox_to_anchor=(1, -0.2))

    #薪资排行绘图
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.set_title(u'薪资排行前十', fontsize=12, color='red')
    x_list = list(data_job_salary.name)
    x = []
    for i in x_list:
        x.append(i.split('（')[0])
    ax2.set_yticks(data_job_salary.wage_high)
    ax2.set_xticklabels(x, rotation=70, fontsize=7)
    ax2.set_ylabel('薪资/k')
    plt.bar(x, data_job_salary.wage_high)
    for a, b in zip(x, data_job_salary.wage_high):
        plt.text(a, b, '%sk' % b, ha='center', va='bottom', fontsize=12, color='red')
    fig.tight_layout()
    #plt.show()
    plt.savefig('./jobplus/static/city.png')


