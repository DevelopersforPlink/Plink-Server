from django.db import models

class ClientPositionChoices(models.TextChoices):
    INVESTOR = '투자자', '투자자'
    ENTREPRENEUR = '창업자', '창업자'

class RequestStatus(models.TextChoices):
    PENDING = "-", "-",
    APPROVED = "Y", "Y"
    REJECTED = "N", "N"
    
class BusinessProgressChoices(models.TextChoices):
    IDEA = "아이디어", "아이디어"
    IN_PROGRESS = "사업 진행중", "사업 진행중"

class BusinessTypeChoices(models.TextChoices):
    SERVICE = "서비스업", "서비스업"
    FINANCE = "금융/은행업", "금융/은행업"
    IT = "IT/정보통신업", "IT/정보통신업"
    RETAIL = "판매/유통업", "판매/유통업"
    MANUFACTURING = "제조/생산/화학업", "제조/생산/화학업"
    EDUCATION = "교육업", "교육업"
    CONSTRUCTION = "건설업", "건설업"
    MEDICAL = "의료/제약업", "의료/제약업"
    MEDIA = "미디어/광고업", "미디어/광고업"
    CULTURE = "문화/예술/디자인업", "문화/예술/디자인업"