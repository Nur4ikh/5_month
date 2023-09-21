from django.db.models import Avg
from rest_framework import serializers
from movie_app.models import Director, Movie, Review

class DirectorList(serializers.ModelSerializer):
    movie_count = serializers.SerializerMethodField()
    class Meta:
        model = Director
        fields = ('id', 'name', 'movie_count')
    def get_movie_count(self, obj):
        return obj.movie.count()


class MovieList(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', 'description', 'duration', 'director_id')


class ReviewList(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('text', 'movie', 'rating')

class AverageSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    movie = serializers.CharField(source='movie.title',)

    class Meta:
        model = Review
        fields = ('movie', 'text', 'average_rating',)

    def get_average_rating(self, obj):
        average_rating = Review.objects.filter(movie=obj.movie).aggregate(avg_rating=Avg('rating'))
        return round(average_rating['avg_rating'], 1) if average_rating['avg_rating'] else 0.0
