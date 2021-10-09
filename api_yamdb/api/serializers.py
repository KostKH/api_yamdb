from rest_framework import serializers
from reviews.models import Genre, Categories, Titles, User, UserCode
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from statistics import mean


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

    class Meta:
        model = Titles
        fields = '__all__'

    def get_rating(self, obj):
        return mean(obj.review.score)


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

