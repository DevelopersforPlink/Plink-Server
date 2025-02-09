import uuid

def change_filename(instance, filename):
    ext = filename.split('.')[-1]  # 확장자 추출
    new_filename = f"{uuid.uuid4()}.{ext}"
    return new_filename

def delete_file(instance):
    pass