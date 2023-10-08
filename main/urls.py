from django.urls import path, include
from django.contrib import admin
from movie_app.views import (
    DirectorsListView,
    DirectorDetailView,
    MovieListView,
    MovieDetailView,
    ReviewListView,
    ReviewDetailView,
    movie_reviews,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/directors/', DirectorsListView.as_view(), name='directors-list'),
    path('api/v1/directors/<int:pk>/', DirectorDetailView.as_view(), name='director-detail'),
    path('api/v1/movies/', MovieListView.as_view(), name='movies-list'),
    path('api/v1/movies/<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
    path('api/v1/reviews/', ReviewListView.as_view(), name='reviews-list'),
    path('api/v1/reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('api/v1/movie-reviews/', movie_reviews, name='movie-reviews'),
    path('api/v1/users/', include('users.urls')),
]
