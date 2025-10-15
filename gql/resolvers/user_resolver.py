from graphql import GraphQLError

from repositories.MovieRepository import MovieRepo
from repositories.UserRepository import UserRepo
from .types import query, user, mutation

@query.field("searchUsers")
def resolve_users_by_prefix(_, info, **kwargs):
    prefix = kwargs.get('prefix')
    return UserRepo.find_users_starting_with_prefix(prefix)

@query.field("user")
def resolve_user(_, info, **kwargs):
    idx = kwargs.get('id')
    return UserRepo.find_user_by_id(idx)

@user.field("favoriteGenres")
def resolve_user_favorite_genres(obj, info, **kwargs):
    idx = obj.get('id')
    return UserRepo.find_user_favorite_genres_by_id(idx)

@query.field("ratings")
def resolve_user_ratings(_, info, **kwargs):
    idx = kwargs.get('userId')
    ans = UserRepo.find_ratings_by_user_id(idx)
    result = []
    for record in ans:
        movie_id = record["movie_id"]
        movie = MovieRepo.find_movie_by_id(movie_id)
        result.append(
            {
                "stars": record["stars"],
                "movie": movie,
            }
        )
    return result

@mutation.field("rateMovie")
def resolve_user_rate_movie(_, info, **kwargs):
    user = info.context.get('userId')
    if user is None:
        raise GraphQLError('Authorization Error')
    movie = kwargs.get("movieId")
    stars = kwargs.get("stars")

    print(movie, stars, user)

    possible_stars = set(i for i in range(11))
    if stars not in possible_stars:
        raise GraphQLError(f"Invalid stars: {stars}")

    if UserRepo.find_user_by_id(user) is None:
        raise GraphQLError(f"Invalid userId: {user}")

    movie1 = MovieRepo.find_movie_by_id(movie)
    if movie1 is None:
        raise GraphQLError(f"Invalid movieId: {movie}")

    UserRepo.rate_movie(user, movie, stars)
    return {
        "stars": stars,
        "movie": movie1
    }