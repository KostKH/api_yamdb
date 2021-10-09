from rest_framework import serializers
from reviews.models import Genre, Categories, Titles


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = '__all__'


class TitlesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Titles
        fields = '__all__'

