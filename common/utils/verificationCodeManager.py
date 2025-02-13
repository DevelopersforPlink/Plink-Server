from random import randint
from django.utils.timezone import now
from datetime import timedelta

def create_code(): # 보안코드 생성
    code = ''
    for i in range(6):
        c = randint(0,9)
        code += str(c)
    return code

def set_expire(): # 유효기간 설정
    return now() + timedelta(minutes=5)