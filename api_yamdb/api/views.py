from django.core.mail import send_mail
from django.shortcuts import render
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenViewBase
from reviews.models import User, UserCode

from api_yamdb.settings import FROM_EMAIL

from . import serializers


class APISignup(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = serializers.SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            email = user.email
            code = get_random_string(length=5)
            UserCode.objects.filter(user=user).update_or_create(user=user, code=code)
            send_mail(
                'YamDB - код подтверждения',
                f'Ваш код подтверждения:{code}',
                FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetTokenView(TokenViewBase):
    permission_classes = (AllowAny,)
    serializer_class = serializers.GetTokenSerializer