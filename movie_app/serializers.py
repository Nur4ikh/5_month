from rest_framework import serializers
from movie_app.models import Director, Movie, Review

class DirectorList(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ('id', 'name')


class MovieList(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class ReviewMovie(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"