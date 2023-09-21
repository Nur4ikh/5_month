from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from movie_app.models import Director, Movie, Review
from movie_app.serializers import DirectorList, MovieList, ReviewList, AverageSerializer


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

@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail(request, id):
    try:
        data = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response({'ERROR': 'Ничего не найдено!'}, status=404)

    if request.method == 'GET':
        serializer = MovieList(instance=data, many=False).data

        return Response(serializer, status=200)
    elif request.method == 'PUT':
        data.title = request.data.get('title', data.title)
        data.description = request.data.get('description', data.description)
        data.duration = request.data.get('duration', data.duration)
        data.director = request.data.get('director', data.director)
        data.save()

        movi_edit = MovieList(instance=data, many=False).data
        return Response(movi_edit, status=200)
    elif request.method == 'DELETE':
        data.delete()
        return Response(status=204)

@api_view(['GET','POST'])
def review(request):
    if request.method == 'GET':
        review = Review.objects.all()
        movie_review = ReviewList(instance=review, many=True).data

        return Response(movie_review)
    elif request.method == 'POST':
        text = request.data.get('text')
        movie = request.data.get('movie')
        rating = request.data.get('rating')

        post = Review.objects.create(
            text=text,
            movie=movie,
            rating=rating,
        )

        data = ReviewList(instance=post, many=False).data
        return Response(data, status=201)

@api_view(['GET','PUT','DELETE'])
def review_detial(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response({'ERROR': 'Ничего не найдено!'}, status=404)
    if request.method == 'GET':
        movie_review = ReviewList(instance=review, many=False).data
        return Response(movie_review)
    elif request.method == 'PUT':
        review.text = request.data.get('text', review.text)
        review.movie = request.data.get('movie', review.movie)
        review.rating = request.data.get('rating', review.rating)
        review.save()

        review_edit = ReviewList(instance=review, many=False).data
        return Response(review_edit, status=200)

    elif request.method == 'DELETE':
        review.delete()
        return Response(status=204)
@api_view(['GET'])
def movie_reviews(request):
    reviews = Review.objects.all()
    serializer = AverageSerializer(instance=reviews, many=True)
    return Response(serializer.data)
