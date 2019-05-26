from rest_framework import serializers
from movie_list.models import Actor, Movie
from django.contrib.auth.models import User
from rest_framework import validators


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('first_name', 'second_name')


class MovieSerializer(serializers.ModelSerializer):
    cast = ActorSerializer(read_only=True, many=True)

    class Meta:
        model = Movie
        fields = ('id', 'name', 'release_date', 'description', 'rating', 'number_of_votes', 'cast', 'cover_image')
