from rest_framework import status
from rest_framework.response import Response


def simple_middleware(get_response):

    def middleware(request):

        user_agent = request.META['HTTP_USER_AGENT']
        if user_agent is None:
            Response({"Msg: User-Agent is empty! "},status=status.HTTP_400_BAD_REQUEST)
        response = get_response(request)

        return response

    return middleware