from django.db import models

class ClientPositionChoices(models.TextChoices):
    INVESTOR = 'INV', '투자자'
    ENTREPRENEUR = 'ENT', '창업자'

class RequestStatus(models.TextChoices):
    PENDING = "-", "대기중"
    APPROVED = "Y", "승인"
    REJECTED = "N", "거절"
    
class BusinessProgressChoices(models.TextChoices):
    IDEA = "IDEA", "아이디어"
    IN_PROGRESS = "IN_PROGRESS", "사업 진행중"

class BusinessTypeChoices(models.TextChoices):
    SERVICE = "SERVICE", "서비스업"
    FINANCE = "FINANCE", "금융/은행업"
    IT = "IT", "IT/정보통신업"
    RETAIL = "RETAIL", "판매/유통업"
    MANUFACTURING = "MANUFACTURING", "제조/생산/화학업"
    EDUCATION = "EDUCATION", "교육업"
    CONSTRUCTION = "CONSTRUCTION", "건설업"
    MEDICAL = "MEDICAL", "의료/제약업"
    MEDIA = "MEDIA", "미디어/광고업"
    CULTURE = "CULTURE", "문화/예술/디자인업"