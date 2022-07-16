from rest_framework.authentication import TokenAuthentication
from .models import MultiTokens


class MultiTokenAuthentication(TokenAuthentication):
    model = MultiTokens
