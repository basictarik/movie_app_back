from rest_framework.decorators import api_view
from rest_framework.response import Response
from movie_list.serializers import ActorSerializer, MovieSerializer
from movie_list.models import Actor, Movie
from rest_framework import status


@api_view(['GET'])
def movie_list(request):
    if request.method == 'GET':
        results, to_show = int(request.GET.get('results')), request.GET.get('to_show')
        movies = Movie.objects.filter(show_type=to_show)
        if len(movies) > results:
            movies = movies[:results]
        serializer = MovieSerializer(movies, many=True)

        return Response(serializer.data)

@api_view(['PATCH'])
def movie_rate(request, pk):
    print(request.data)

    rate = request.data['rate']
    movie = Movie.objects.get(pk=pk)
    no_votes = movie.number_of_votes + 1
    avg_rating = movie.rating

    movie.rating = ((avg_rating * (no_votes - 1)) + rate) / no_votes
    movie.number_of_votes = no_votes
    movie.save(update_fields=['rating', 'number_of_votes'])

    return Response("OK", status=status.HTTP_200_OK)
