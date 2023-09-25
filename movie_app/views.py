from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from movie_app.models import Director, Movie, Review
from movie_app.serializers import DirectorList, MovieList, ReviewList, AverageSerializer, DirectorValidated, MovieValidated, ReviewsValidated


@api_view(['GET', 'POST'])
def directors_name(request):
    if request.method == 'GET':
        directors = Director.objects.annotate(movies_count=Count('movie'))
        serializer = DirectorList(instance=directors, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = DirectorValidated(data=request.data)
        serializer.is_valid(raise_exception=True)
        director = Director.objects.create(
            name = serializer.validated_data.get('name')
        )
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
        serializers = DirectorValidated(data=request.data)
        serializers.is_valid(raise_exception=True)
        data.name = serializers.validated_data.get('name', data.name)
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
        serializers = MovieValidated(data=request.data)
        serializers.is_valid(raise_exception=True)
        post = Movie.objects.create(
            title=serializers.validated_data.get('title'),
            description=serializers.validated_data.get('description'),
            duration=serializers.validated_data.get('duration'),
            director_id=serializers.validated_data.get('director_id'),
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
        serializers = MovieValidated(data=request.data)
        serializers.is_valid(raise_exception=True)

        data.title = serializers.validated_data.get('title', data.title)
        data.description = serializers.validated_data.get('description', data.description)
        data.duration = serializers.validated_data.get('duration', data.duration)
        data.director = serializers.validated_data.get('director', data.director)
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
        serializers = ReviewsValidated(data=request.data)
        serializers.is_valid(raise_exception=True)

        post = Review.objects.create(
            text=serializers.validated_data.get('text'),
            movie_id=serializers.validated_data.get('movie_id'),
            rating=serializers.validated_data.get('rating'),
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
        serializers = ReviewsValidated(data=request.data)
        serializers.is_valid(raise_exception=True)
        review.text = serializers.validated_data.get('text', review.text)
        review.movie = serializers.validated_data.get('movie', review.movie)
        review.rating = serializers.validated_data.get('rating', review.rating)
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
