import itchat
import os
from flask_login import login_user
from jobplus.models import db, User
from faker import Faker

fake = Faker()


def wechat():
    itchat.auto_login(enableCmdQR=False)
    uuid = itchat.get_QRuuid()
    while uuid is None:
        uuid = itchat.get_QRuuid()
    waitForConfirm = False
    while True:
        status = itchat.check_login(uuid)
        if status == '200':
            os.remove('QR.png')
        elif status == '201':
            if waitForConfirm:
                waitForConfirm = True
        elif status == '408':
            uuid = itchat.get_QRuuid()
            waitForConfirm = False
        login_user = itchat.get_friends(update=True)[0]
        user = User(username=login_user[u'NickName'],
                    email=fake.email(),
                    password='123456')
        db.session.add(user)
        db.session.commit()
        login_user(user)


if __name__ == '__main__':
    wechat()

