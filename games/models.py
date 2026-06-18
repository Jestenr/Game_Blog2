from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg


class Genre(models.Model):

    name = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.name


class Category(models.Model):

    name = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.name


class Game(models.Model):

    title = models.CharField(
        max_length=200
    )

    image = models.ImageField(
        upload_to='games/'
    )

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    release_year = models.IntegerField()

    average_rating = models.FloatField(
        default=0
    )

    def update_rating(self):

        avg = self.review_set.filter(
            approved=True
        ).aggregate(
            Avg('rating')
        )['rating__avg']

        if avg:
            self.average_rating = round(
                avg,
                1
            )
        else:
            self.average_rating = 0

        self.save()

    def __str__(self):
        return self.title


class Review(models.Model):

    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    short_text = models.CharField(
        max_length=300
    )

    full_text = models.TextField()

    rating = models.IntegerField()

    approved = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.game} - {self.author}'

class Comment(models.Model):

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.author.username