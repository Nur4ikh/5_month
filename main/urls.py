from django.contrib import admin
from django.urls import path
from movie_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/directors/', views.directors_name),
    path('api/v1/directors/<int:id>', views.director),
    path('api/v1/movies/', views.movie),
    path('api/v1/movies/<int:id>', views.movie_detail),
    path('api/v1/reviews/', views.review),
    path('api/v1/reviews/<int:id>', views.review_detial),
    path('api/v1/movies/reviews/', views.movie_reviews),
]
