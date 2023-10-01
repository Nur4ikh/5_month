from django.db.models import Count
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from movie_app.models import Director, Movie, Review
from movie_app.serializers import (
    DirectorList,
    MovieList,
    ReviewList,
    AverageSerializer,
    DirectorValidated,
    MovieValidated,
    ReviewsValidated,
)

class DirectorsListView(ListCreateAPIView):
    queryset = Director.objects.annotate(movies_count=Count('movie'))
    serializer_class = DirectorList

class DirectorDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorList

class MovieListView(ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieList

class MovieDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieList

class ReviewListView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewList

class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewList

@api_view(['GET'])
def movie_reviews(request):
    reviews = Review.objects.all()
    serializer = AverageSerializer(instance=reviews, many=True)
    return Response(serializer.data)

