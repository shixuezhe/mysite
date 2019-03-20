import random
import jobplus.zhenzismsclient as smsclient

def send_code(number):
    code = ''
    for i in range(1, 5):
        code = code + str(random.randint(1, 9))
    client = smsclient.ZhenziSmsClient('https://sms_developer.zhenzikj.com','101043', 'MGVjY2FhMzEtZDE3NC00MDA3LWE1NDItNWQwMWQwNmEyYTE4')
    result = client.send(number, '您的验证码为' + code + ',请不要将验证码泄露给他人哦！！！')
    return code
