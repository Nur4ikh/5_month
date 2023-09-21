from django.db import models

class Director(models.Model):
    name = models.CharField(max_length=50, null=True)

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField()
    director_id = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='movie')

    def __str__(self) -> str:
        return f'Movie: {self.title}'
class Review(models.Model):
    STARS_CHOICES = ((i, i * '*') for i in range(1, 6))
    text = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=STARS_CHOICES, null=True)

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


