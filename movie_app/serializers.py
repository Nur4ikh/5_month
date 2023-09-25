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

class DirectorValidated(serializers.Serializer):
    name = serializers.CharField(max_length=100)

class MovieValidated(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=200)
    duration = serializers.IntegerField()
    director_id = serializers.IntegerField()

    def validate_director_id(self, value: list):
        try:
            Director.objects.get(id=value)
        except Director.DoesNotExist as e:
            raise serializers.ValidationError(str(e))

class ReviewsValidated(serializers.Serializer):
    text = serializers.CharField(max_length=200)
    movie_id = serializers.IntegerField()
    rating = serializers.IntegerField()

    def validate_movie_id(self, value: list):
        try:
            Movie.objects.get(id=value)
        except Movie.DoesNotExist as e:
            raise serializers.ValidationError(str(e))
        return value
