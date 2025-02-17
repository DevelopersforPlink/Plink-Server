import uuid

def change_filename(filename):
    ext = filename.split('.')[-1]  # 확장자 추출
    new_filename = f"{uuid.uuid4()}.{ext}"
    return new_filename

def delete_file(instance):
    pass

def profile_upload_path(instance, filename):
    model_name = instance.__class__.__name__.lower()
    return f'profile/{model_name}/{change_filename(filename)}'

def certificate_upload_path(instance, filename):
    model_name = instance.__class__.__name__.lower()
    return f'certificate-employment/{model_name}/{change_filename(filename)}'

def thumbnail_upload_path(instance, filename):
    model_name = instance.__class__.__name__.lower()
    return f'thumbnail/{model_name}/{change_filename(filename)}'

def summary_business_plan_upload_path(instance, filename):
    model_name = instance.__class__.__name__.lower()
    return f'summary_business_plan/{model_name}/{change_filename(filename)}'

def business_plan_upload_path(instance, filename):
    model_name = instance.__class__.__name__.lower()
    return f'business_plan/{model_name}/{change_filename(filename)}'

def pitch_deck_upload_path(instance, filename):
    model_name = instance.__class__.__name__.lower()
    return f'pitch_deck/{model_name}/{change_filename(filename)}'

def traction_data_upload_path(instance, filename):
    model_name = instance.__class__.__name__.lower()
    return f'traction_data/{model_name}/{change_filename(filename)}'