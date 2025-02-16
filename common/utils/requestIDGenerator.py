from random import choices
from string import ascii_uppercase, digits
from django.utils.timezone import now

def generate_request_id(request_type: str) -> str:
    date_part = now().strftime("%y%m%d")
    random_part = ''.join(choices(ascii_uppercase + digits, k=4))
    return f"{request_type}{date_part}{random_part}"