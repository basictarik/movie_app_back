from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from movie_list.serializers import ActorSerializer, MovieSerializer, CreateUserSerializer
from movie_list.models import Actor, Movie
from rest_framework import status
from django.db.models import Q
from oauth2_provider.decorators import protected_resource
from rest_framework.permissions import AllowAny, IsAuthenticated

import requests


@api_view(['GET'])
@permission_classes([AllowAny])
def movie_list(request):
    if request.method == 'GET':
        results, to_show = int(request.GET.get('results')), request.GET.get('to_show')
        if request.GET.get('search_bar_text') is not None:
            search_key = request.GET.get('search_bar_text')
            movies = Movie.objects.filter(
                Q(show_type=to_show) & Q(name__icontains=str(search_key)) | Q(description__icontains=str(search_key)) |
                Q(actors_string__icontains=str(search_key)))
        else:
            movies = Movie.objects.filter(show_type=to_show)

        if len(movies) > results:
            movies = movies[:results]
        serializer = MovieSerializer(movies, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
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


CLIENT_ID = 'd6Kc707gOkh0cUJmsSH7XSSGWBX9RBAiUed2jNBX'
CLIENT_SECRET = 'f0Tm5U4hWOF1LmtlzUtYux7RANOiBidXo4Cq0wXWp1q9ldfxAYEyNRvGNyEnJsXdmVesZGo8pkKiZtiqhUO5tlGRo8PBDTQj0tKLAzjMma7vRI4p4BZXzvTg6KMa5gbV'


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = CreateUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        r = requests.post('http://127.0.0.1:8000/o/token/',
                          data={
                              'grant_type': 'password',
                              'username': request.data['username'],
                              'password': request.data['password'],
                          },
                          )
        print(r.json())
        return Response(r.json())
    return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    r = requests.post(
        'http://127.0.0.1:8000/o/token/',
        data={
            'grant_type': 'password',
            'username': request.data['username'],
            'password': request.data['password'],
            'client_id': CLIENT_ID,
        },
    )
    print(r)
    return Response(r.json())


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    r = requests.post(
        'http://127.0.0.1:8000/o/token/',
        data={
            'grant_type': 'refresh_token',
            'refresh_token': request.data['refresh_token'],
            'client_id': CLIENT_ID,
        },
    )
    return Response(r.json())


@api_view(['POST'])
@permission_classes([AllowAny])
def revoke_token(request):
    r = requests.post(
        'http://127.0.0.1:8000/o/token/',
        data={
            'token': request.data['token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    if r.status_code == requests.codes.ok:
        return Response({'message': 'token revoked'}, r.status_code)
    return Response(r.json(), r.status_code)
