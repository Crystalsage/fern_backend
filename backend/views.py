from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework import serializers
from rest_framework import status

from functools import wraps

from .serializers import PartnerSerializer
from .utils import *
from .models import Partner, Login
from .decorators import require_token 

class ProfileView(APIView):
    @require_token
    def get(self, request):
        return Response({})

class RegistrationView(APIView):
    def get(self, request):
        content = { "message": "Hello there!" }
        return Response(content)

    def post(self, request):
        partner = PartnerSerializer(data=request.data, context= {'request': request})
        
        if partner.is_valid():
            partner.save()

            session_partner = partner.instance
            session_partner.partner_id = generate_partner_id()
            session_partner.save()

            session = Login.objects.create(partner=session_partner, password_hash = generate_md5_hash(partner.data.get('password')))
            session.save()

            return Response({"Partner ID": session_partner.partner_id}, status=status.HTTP_201_CREATED)

        return Response(partner.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        partner = Partner.objects.get(email_address=request.data['email_address'])
        login_session = Login.objects.select_related().filter(partner=partner)[0]
        input_passwd_hash = generate_md5_hash(request.data['password'])

        if login_session is not None and login_session.password_hash == input_passwd_hash:
            response = Response({ "Logged in!": partner.partner_id }, status=status.HTTP_200_OK)
            response.set_cookie("Authorization", "Bearer " + generate_jwt(partner.partner_id))

            return response
        else:
            return Response("Could not find partner!", status=status.HTTP_404_NOT_FOUND)

class LogoutView(APIView):
    def get(self, request):
        partner_id = jwt_get_partner_id(request.COOKIES.get('Authorization').split(" ")[1])

        response = Response({ "Logged out!": partner_id }, status=status.HTTP_200_OK)
        response.set_cookie("Authorization", None)

        return response
