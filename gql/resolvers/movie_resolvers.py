from .types import query, movie
from repositories.MovieRepository import MovieRepo
from repositories.ActorRepository import ActorRepo
from repositories.DirectorRepository import DirectorRepo

@query.field("movie")
def resolve_movie(_, info, **kwargs):
    idx = kwargs.get("id")
    return MovieRepo.find_movie_by_id(idx)

@movie.field("actors")
def resolve_actors_for_movie(obj, info):
    idx = obj.get('id')
    return MovieRepo.find_movie_actors_by_id(idx)

@movie.field("director")
def resolve_director_for_movie(obj, info):
    idx = obj.get('id')
    return MovieRepo.find_movie_director_by_id(idx)

@query.field("actorsMovies")
def resolve_movies_for_actors(_, info, **kwargs):
    idx = kwargs.get('actorId')
    return ActorRepo.find_actors_movies(idx)

@query.field("directorsMovies")
def resolve_movies_for_directors(_, info, **kwargs):
    idx = kwargs.get('directorId')
    return DirectorRepo.find_directors_movies(idx)