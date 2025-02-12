from random import randint

def create_code(): # 보안코드 생성
    code = ''
    for i in range(6):
        c = randint(0,9)
        code += str(c)
    return code