from rest_framework.decorators import api_view
from rest_framework.response import Response

from movie_app.models import Director, Movie, Review
from movie_app.serializers import DirectorList, MovieList, ReviewMovie


@api_view(['GET'])
def directors_name(request):
    name = Director.objects.all()

    data = DirectorList(instance=name, many=True).data

    return Response(data)

@api_view(['GET'])
def director(request, id):
    name = Director.objects.get(id=id)

    data = DirectorList(instance=name, many=False).data

    return Response(data)

@api_view(['GET'])
def movie(request):
    movie_name = Movie.objects.all()
    movie_list = MovieList(instance=movie_name, many=True).data

    return Response(movie_list)

@api_view(['GET'])
def movie_detail(request, id):
    movie_name = Movie.objects.get(id=id)
    movie_list = MovieList(instance=movie_name, many=False).data

    return Response(movie_list)

@api_view(['GET'])
def review(request):
    review = Review.objects.all()
    movie_review = ReviewMovie(instance=review, many=True).data

    return Response(movie_review)

@api_view(['GET'])
def review_detial(request, id):
    review = Review.objects.get(id=id)
    movie_review = ReviewMovie(instance=review, many=False).data

    return Response(movie_review)