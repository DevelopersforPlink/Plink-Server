from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from common.models.choiceModels import ClientPositionChoices

class IsApprovedUser(BasePermission):
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if hasattr(request.user, 'client') and not request.user.client.is_approve:
            raise PermissionDenied({
                "error": "재직증명을 하셔야 해요."
            })
        return True
    
class IsInvestor(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if hasattr(request.user, 'client') and request.user.client.client_position != ClientPositionChoices.INVESTOR:
            raise PermissionDenied({
                "error": "투자자로 등록된 사용자만 접근할 수 있어요."
            })
        return True


class IsEntrepreneur(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if hasattr(request.user, 'client') and request.user.client.client_position != ClientPositionChoices.ENTREPRENEUR:
            raise PermissionDenied({
                "error": "창업가로 등록된 사용자만 접근할 수 있어요."
            })
        return True