from django.core.mail import send_mail
from django.shortcuts import render
from django.utils.crypto import get_random_string
from reviews.models import Genre, Categories, Titles, User, UserCode
from rest_framework import filters, mixins, permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenViewBase
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAdminOrReadOnly, ReadOnly
from . import serializers
from api_yamdb.settings import FROM_EMAIL


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = (DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter)
    filterset_fields = ('name', 'slug')
    ordering_fields = ('name',)
    search_fields = ('name',)


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = serializers.CategoriesSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = (DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter)
    filterset_fields = ('name', 'slug')
    ordering_fields = ('name',)
    search_fields = ('name',)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = serializers.TitlesSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = (DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter)
    filterset_fields = ('name',)
    ordering_fields = ('name',)
    search_fields = ('name',)

    def get_permissions(self):
        # Если в GET-запросе требуется получить информацию об объекте
        if self.action == 'retrieve':
            # Вернем обновленный перечень используемых пермишенов
            return (ReadOnly(),)
        # Для остальных ситуаций оставим текущий перечень пермишенов без изменений
        return super().get_permissions()


class APISignup(APIView):
    permission_classes = (permissions.AllowAny,)

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
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.GetTokenSerializer

