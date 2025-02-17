import uuid

def change_filename(filename):
    ext = filename.split('.')[-1]  # 확장자 추출
    new_filename = f"{uuid.uuid4()}.{ext}"
    return new_filename

def delete_file(instance):
    pass

def profile_upload_path(instance, filename):
    return f'profile/{change_filename(filename)}'

def certificate_upload_path(instance, filename):
    return f'certificate-employment/{change_filename(filename)}'

def thumbnail_upload_path(instance, filename):
    return f'thumbnail/{change_filename(filename)}'

def summary_business_plan_upload_path(instance, filename):
    return f'summary_business_plan/{change_filename(filename)}'

def business_plan_upload_path(instance, filename):
    return f'business_plan/{change_filename(filename)}'

def pitch_deck_upload_path(instance, filename):
    return f'pitch_deck/{change_filename(filename)}'

def traction_data_upload_path(instance, filename):
    return f'traction_data/{change_filename(filename)}'