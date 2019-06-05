from django.db import models


class Actor(models.Model):
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=100)
    release_date = models.DateField(auto_now_add=True, blank=True)
    description = models.TextField(default="Description")
    rating = models.FloatField(default=0)
    number_of_votes = models.IntegerField(default=0)
    actors_string = models.TextField(default='')
    cast = models.ManyToManyField(Actor)
    show_type = models.CharField(max_length=100, default='Movie')
    cover_image = models.ImageField(upload_to='images', default='no-image.jpg')

    class Meta:
        ordering = ('-rating',)

    def __str__(self):
        return self.name
