from rest_framework import serializers
from reviews.models import Genre, Categories, Title, User, UserCode, Review, Comment
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
import datetime as dt


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('name', 'slug')


class TitlesSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genres = GenreSerializer(many=True, required=False)
    categories = CategoriesSerializer(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        scores = [i.score for i in Review.objects.filter(title__id=obj.id)]
        if len(scores) > 0:
            return sum(scores) / len(scores)
        else:
            return None

    def validate_year(self, value):
        current_year = dt.datetime.now().year
        if 0 > value > current_year:
            raise serializers.ValidationError(
                'Год выпуска не может быть меньше 0 или больше текущего года!'
            )
        return value


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Username "me" использовать запрещено. Придумайте другой username')
        return data


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField(max_length=5)

    def get_token(self, user):
        return RefreshToken.for_user(user)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        code = get_object_or_404(UserCode, user=user)
        if not code.code:
            raise serializers.ValidationError(
                'Пользователь не запрашивал код')
        
        elif code.code != data['confirmation_code']:
            raise serializers.ValidationError(
                f'Вы отправили неправильный код{data["confirmation_code"]},{code.code}')
        
        token = self.get_token(user)
        return {'token': str(token.access_token),}


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True)

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data

        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        if Review.objects.filter(
                author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже написали отзыв к этому произведению.'
            )
        return data

    def validate_score(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError(
                'Можете оценить от 1 до 10.'
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment

