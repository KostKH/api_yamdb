from rest_framework import serializers
from reviews.models import Genre, Categories, Titles, User, UserCode
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from statistics import mean
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
    rating = serializers.SerializerMethodField
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Categories.objects.all()
    )
    genres = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )

    class Meta:
        model = Titles
        fields = ('name', 'year', 'description', 'category', 'genres',)

    def get_rating(self, obj):
        return mean(obj.review.score)

    def validate_year(self, value):
        current_year = dt.datetime.now().year
        if 0 > value > current_year:
            raise serializers.ValidationError(
                'Год выпуска не может быть меньше 0 или больше текущего года!'
            )
        return value

    def create(self, validated_data):
        if 'genres' not in self.initial_data:
            return Titles.objects.create(**validated_data)
        else:
            genres = validated_data.pop('genres')
            title = Titles.objects.create(**validated_data)
            #title.save()
            title.genres.set([genres])
            return title


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


