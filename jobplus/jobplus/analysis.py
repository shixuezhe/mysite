import matplotlib.pyplot as plt
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
    job = Job.query.all()
    job_list = []
    for i in job:
        job_list.append(i.location.split('·')[0])
    con = Counter(job_list).most_common(10)
    data = DataFrame(con)
    x = data[0]
    y = data[1]*10
    plt.xlabel('热点城市')
    plt.ylabel('在招职位数量')
    plt.title('热点城市职位统计')
    plt.bar(x, y)
    for a, b in zip(x, y):
        plt.text(a, b, '%.0f' % b, ha='center', va='bottom', fontsize=12, color='red')
    if os.path.exists('./static/all.png'):
        os.remove('./static/all.png')
    plt.savefig('./static/all.png')


def city_analysis(city):
    search = '%' + city + '%'
    sql = "SELECT LOCATION,ID FROM JOB WHERE LOCATION LIKE '%s'" % search
    cursor.execute(sql)
    rr = cursor.fetchall()
    location_list = []
    for row in rr:
        location_list.append(row)
    orign_data = DataFrame(location_list)
    data = orign_data.groupby(0).sum()[:10]
    plt.pie(data, labels=data.index, autopct='%3.1f %%')
    plt.title(u'区域招聘热度', fontsize=12, color='red')

    if os.path.exists('./jobplus/static/city.png'):
        os.remove('./jobplus/static/city.png')
    plt.savefig('./jobplus/static/city.png')


def more_analysis(city, job):
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
    plt.bar(x, y)
    for a, b in zip(x, y):
        plt.text(a, b, '%sk' % b, ha='center', va='bottom', fontsize=15, color='red')

    if os.path.exists('./jobplus/static/more.png'):
        os.remove('./jobplus/static/more.png')
    plt.savefig('./jobplus/static/more.png')


if __name__ == '__main__':
    more_analysis('成都', '经理')