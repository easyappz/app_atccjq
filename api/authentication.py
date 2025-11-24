from rest_framework.authentication import TokenAuthentication as DRFTokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import Token
from api.models import Member


class MemberTokenAuthentication(DRFTokenAuthentication):
    """
    Custom token authentication for Member model.
    """
    
    def authenticate_credentials(self, key):
        """
        Authenticate the token and return the member.
        """
        try:
            token = Token.objects.select_related('user').get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        if not token.user.is_active:
            raise AuthenticationFailed('User inactive or deleted.')

        # Get the associated Member
        try:
            member = Member.objects.get(id=token.user.id)
        except Member.DoesNotExist:
            raise AuthenticationFailed('Member not found.')

        return (member, token)
