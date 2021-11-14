from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User
import jwt
import datetime
# Create your views here.


class registerView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class loginView(APIView):
    def post(self, request):
        email = request.data['email']
        pw = request.data['password']

        usr = get_object_or_404(User, email=email) or None
        if usr is None:
            raise AuthenticationFailed("User not found")
        if not usr.check_password(pw):
            raise AuthenticationFailed("Incorrect password")

        payload = {
            'id': usr.id,
            'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {"jwt": token}

        return response


class userView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated")

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated")

        usr = get_object_or_404(User, id=payload['id']) or None
        srlzr = UserSerializer(usr)
        return Response(srlzr.data)


class logoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "message": "success"
        }
        return response
