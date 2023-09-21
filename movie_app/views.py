from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from movie_app.models import Director, Movie, Review
from movie_app.serializers import DirectorList, MovieList, ReviewMovie, AverageSerializer


@api_view(['GET', 'POST'])
def directors_name(request):
    if request.method == 'GET':
        directors = Director.objects.annotate(movies_count=Count('movie'))
        serializer = DirectorList(instance=directors, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        name = request.data.get('name')
        director = Director.objects.create(name=name)
        data = DirectorList(instance=director, many=False).data

        return Response(data, status=201)


@api_view(['GET', 'PUT', 'DELETE'])
def director(request, id):
    try:
        data = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response({'ERROR': 'Ничего не найдено!'}, status=404)

    if request.method == 'GET':
        serializer = DirectorList(instance=data, many=False).data

        return Response(serializer, status=200)
    elif request.method == 'PUT':
        data.name = request.data.get('name', data.name)
        data.save()

        director = DirectorList(instance=data, many=False).data
        return Response(director, status=200)
    elif request.method == 'DELETE':
        data.delete()
        return Response(status=204)



@api_view(['GET', 'POST'])
def movie(request):
    if request.method == 'GET':
        movie_name = Movie.objects.all()
        movie_list = MovieList(instance=movie_name, many=True).data

        return Response(movie_list)
    elif request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('description')
        duration = request.data.get('duration')
        director_id = request.data.get('director_id')
        post = Movie.objects.create(
            title=title,
            description=description,
            duration=duration,
            director_id=director_id,
        )
        data = MovieList(instance=post, many=False).data

        return Response(data, status=201)

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

@api_view(['GET'])
def movie(request):
    movie_name = Movie.objects.all()
    movie_list = MovieList(instance=movie_name, many=True).data

    return Response(movie_list)

@api_view(['GET'])
def movie_reviews(request):
    reviews = Review.objects.all()
    serializer = AverageSerializer(instance=reviews, many=True)
    return Response(serializer.data)
