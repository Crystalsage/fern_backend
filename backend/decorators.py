from rest_framework.response import Response
from functools import wraps

from .utils import verify_jwt

def require_token(func):
    @wraps(func)
    def wrapped(self, request, *args, **kwargs):
        token = request.COOKIES.get("Authorization")

        if token is None or not token.startswith('Bearer'):
            return Response({"ERR": "Unauthorized, No token."}, status=401)

        jwt = token.split(" ")[1]
        is_partner, partner_id = verify_jwt(jwt)

        if not is_partner:
            return Response({"ERR": "Unauthorized, not partner."}, status=401)

        response = func(self, request, *args, **kwargs)

        if response is None:
            return Response({"ERR": "No response received."}, status=200)

        response.data["Greetings! Your partner ID is: "] = partner_id

        return response
    return wrapped
