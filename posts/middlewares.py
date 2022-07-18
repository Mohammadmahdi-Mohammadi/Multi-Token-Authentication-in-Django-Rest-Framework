from rest_framework import status
from rest_framework.response import Response


def simple_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        user_agent = request.META['HTTP_USER_AGENT']
        if user_agent is None:
            Response({"Msg: User-Agent is empty! "},status=status.HTTP_400_BAD_REQUEST)
        response = get_response(request)


        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware