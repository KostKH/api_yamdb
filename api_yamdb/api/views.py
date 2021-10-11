from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from reviews.models import Genre, Category, Title, User, UserCode, Review, Comment
from rest_framework import filters, permissions, viewsets, status, pagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenViewBase
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from .permissions import ReadOnly, IsAdmin, IsOwnerOrReadOnly, IsAdminModerator
from . import serializers
from .filters import TitleFilter
from api_yamdb.settings import FROM_EMAIL


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = [IsAdmin | ReadOnly]
    filter_backends = (DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter)
    filterset_fields = ('name', 'slug')
    ordering_fields = ('name',)
    search_fields = ('name',)

    @action(
        detail=False, methods=['delete'],
        url_path=r'(?P<slug>\w+)',
        lookup_field='slug', url_name='category_slug'
    )
    def get_genre(self, request, slug):
        genre = self.get_object()
        serializer = serializers.GenreSerializer(genre)
        genre.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAdmin | ReadOnly]
    filter_backends = [DjangoFilterBackend]
    filter_backends = (DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter)
    filterset_fields = ('name', 'slug')
    ordering_fields = ('name',)
    search_fields = ('name',)

    @action(
        detail=False, methods=['delete'],
        url_path=r'(?P<slug>\w+)',
        lookup_field='slug', url_name='category_slug'
    )
    def get_category(self, request, slug):
        category = self.get_object()
        serializer = serializers.CategorySerializer(category)
        category.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = serializers.TitleSerializer
    permission_classes = [IsAdmin | ReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.TitleReadSerializer
        return serializers.TitleSerializer


class APISignup(APIView):
    permission_classes = (permissions.AllowAny,)

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
            permission_classes=[permissions.IsAuthenticated, ],
            url_path='me', url_name='me')
    def me(self, request):
        user = request.user

        if self.request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                current_role = user.role
                new_role = serializer.validated_data['role']
                if current_role == 'user' and new_role != 'user':
                    serializer.validated_data['role'] = 'user'
            except:
                pass
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAdminModerator | IsOwnerOrReadOnly]
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsAdminModerator | IsOwnerOrReadOnly]
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)
