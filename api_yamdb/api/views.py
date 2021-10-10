from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from reviews.models import Genre, Categories, Titles, User, UserCode
from rest_framework import filters, permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenViewBase
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from .permissions import ReadOnly, IsAdmin
from . import serializers
from api_yamdb.settings import FROM_EMAIL


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = [IsAdmin, ]
    filter_backends = (DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter)
    filterset_fields = ('name', 'slug')
    ordering_fields = ('name',)
    search_fields = ('name',)

    def get_permissions(self):
        if self.request.method == 'GET':
            return (ReadOnly(),)
        return super().get_permissions()


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = serializers.CategoriesSerializer
    permission_classes = [IsAdmin, ]
    filter_backends = (DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter)
    filterset_fields = ('name', 'slug')
    ordering_fields = ('name',)
    search_fields = ('name',)

    def get_permissions(self):
        if self.request.method == 'GET':
            return (ReadOnly(),)
        return super().get_permissions()


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = serializers.TitlesSerializer
    permission_classes = [IsAdmin, ]
    filter_backends = (DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter)
    filterset_fields = ('name',)
    ordering_fields = ('name',)
    search_fields = ('name',)

    def get_permissions(self):
        if self.request.method == 'GET':
            return (ReadOnly(),)
        return super().get_permissions()


class APISignup(APIView):
    permission_classes = (permissions.AllowAny,)


    def post(self, request):
        serializer = serializers.SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
    def send_code(self, user):

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
    def post(self, request):
        serializer = serializers.SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            self.send_code(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTokenView(TokenViewBase):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.GetTokenSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(methods=['patch', 'get'],
            detail=False,
            permission_classes=[permissions.IsAuthenticated,],
            url_path='me', url_name='me')

    def me(self, request):
        user = request.user
        
        if self.request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        serializer = self.get_serializer(user, data=request.data, partial=True)
        try:
            current_role = user.role
            new_role = request.data['role']
        except:
            if serializer.is_valid():
                serializer.save()
                return Response(user.role, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if current_role == 'user' and new_role !='user':
            return Response('нет прав на смену роли', status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            return Response(user.role, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

