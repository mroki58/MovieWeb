from repositories.UserRepository import UserRepo
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

@query.field("searchMovies")
def resolve_movies_by_prefix(_, info, **kwargs):
    prefix = kwargs.get('prefix')
    return MovieRepo.find_movie_starting_with_prefix(prefix)

@query.field("searchActors")
def resolve_actors_by_prefix(_, info, **kwargs):
    prefix = kwargs.get('prefix')
    return ActorRepo.find_actors_starting_with_prefix(prefix)

@query.field("newMovies")
def resolve_new_movies(_, info, **kwargs):
    limit = kwargs.get('limit')
    return MovieRepo.find_newest_movies(limit)

def resolve_recommended_movies_for_unlogged(info, **kwargs):
    movies = MovieRepo.find_random_movies()
    return movies

def resolve_recommended_movies_for_logged(user_id, info, **kwargs):
    MAX_RECOMMENDATIONS = 30

    raw_genres = UserRepo.find_user_favorite_genres_by_id(user_id)
    user_genres = set()
    for g in raw_genres or []:
        name = None
        try:
            name = g.get('name') if hasattr(g, 'get') else g['name']
        except Exception:
            try:
                name = getattr(g, 'name')
            except Exception:
                name = None
        if name:
            user_genres.add(name)

    selected = []
    selected_ids = set()

    # Znalezienie filmow, ktore znają znajomi
    friends_movies = MovieRepo.find_movies_from_friends(user_id=user_id, exclude_user_id=user_id, limit=(MAX_RECOMMENDATIONS - 10))
    for m in friends_movies:
        mid = m.get('id')
        if mid and mid not in selected_ids:
            selected.append(m)
            selected_ids.add(mid)
            if len(selected) >= MAX_RECOMMENDATIONS:
                break

    # Znalezienie wśród najnowszych filmów takich, które znamy
    if len(selected) < MAX_RECOMMENDATIONS:
        newest = MovieRepo.find_newest_movies_with_cast(limit=100)
        for nm in newest:
            movie = nm.get('movie')
            if not movie:
                continue
            mid = movie.get('id')
            genre = movie.get('genre')
            if mid and mid not in selected_ids and genre and genre in user_genres:
                selected.append(movie)
                selected_ids.add(mid)
                if len(selected) >= MAX_RECOMMENDATIONS:
                    break

    # Randomowe filmy, żeby dopełnić listę
    if len(selected) < MAX_RECOMMENDATIONS:
        pool = MovieRepo.find_random_movies(limit=50)
        for pm in pool:
            mid = pm.get('id')
            if mid and mid not in selected_ids:
                selected.append(pm)
                selected_ids.add(mid)
                if len(selected) >= MAX_RECOMMENDATIONS:
                    break

    import random
    random.shuffle(selected)

    return selected





@query.field("recommendedMovies")
def resolve_recommended_movies(_, info, **kwargs):
    idx = kwargs.get('userId')
    if idx is None:
        movies = resolve_recommended_movies_for_unlogged(info, **kwargs)
    else:
        movies = resolve_recommended_movies_for_logged(idx, info, **kwargs)
    return movies