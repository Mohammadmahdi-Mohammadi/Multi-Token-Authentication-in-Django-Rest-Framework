from rest_framework.authentication import TokenAuthentication
from posts.models import MultiTokens


class MultiTokenAuthentication(TokenAuthentication):
    model = MultiTokens

