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

@user.field("friends")
def resolve_user_friends(obj, info, **kwargs):
    idx = obj.get('id')
    return UserRepo.find_user_friends_by_id(idx)

@user.field("favoriteMovies")
def resolve_user_favorite_movies(obj, info, **kwargs):
    idx = obj.get('id')
    return UserRepo.find_user_favorite_movies_by_id(idx)

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

@mutation.field("deleteRating")
def resolve_delete_rating(_, info, **kwargs):
    user = info.context.get('userId')
    if user is None:
        raise GraphQLError('Authorization Error')
    movie = kwargs.get("movieId")

    UserRepo.unrate_movie(user, movie)

@mutation.field("friendRequest")
def resolve_user_friend_request(_, info, **kwargs):
    user = info.context.get('userId')
    if user is None:
        raise GraphQLError('Authorization Error')

    friend = kwargs.get("friend")
    try:
        UserRepo.send_friend_request( user, friend)
    except ValueError:
        raise GraphQLError(f"Invalid friends name: {friend}")

    return True

@mutation.field("friendRequestAccept")
def resolve_accept_friend_request(_, info, **kwargs):
    user = info.context.get('userId')
    if user is None:
        raise GraphQLError('Authorization Error')

    friend = kwargs.get("friend")
    try:
        UserRepo.delete_friend_request(user, friend)
        UserRepo.accept_friend_request(user, friend)
    except:
        raise GraphQLError(f"Invalid friends name: {friend}")

    return True

@mutation.field("friendRequestReject")
def resolve_reject_friend_request(_, info, **kwargs):
    user = info.context.get('userId')
    if user is None:
        raise GraphQLError('Authorization Error')

    friend = kwargs.get("friend")
    if friend:
        UserRepo.delete_friend_request(user, friend)

    return True

@mutation.field("deleteFriend")
def resolve_delete_friend(_, info, **kwargs):
    user = info.context.get('userId')
    if user is None:
        raise GraphQLError('Authorization Error')

    friend = kwargs.get("friend")
    if friend:
        UserRepo.delete_friend(user, friend)

    return True

@query.field("friendRequestFromMe")
def resolve_friend_request_from_me(_, info):
    user = info.context.get('userId')
    if user is None:
        raise GraphQLError('Authorization Error')

    return UserRepo.find_friend_request_from_me(user)

@query.field("friendRequestToMe")
def resolve_friend_request_to_me(_, info):
    user = info.context.get('userId')
    if user is None:
        raise GraphQLError('Authorization Error')

    return UserRepo.find_friend_request_to_me(user)

@mutation.field("modifyUserRanking")
def resolve_modify_user_ranking(_, info, places, movies):
    user = info.context.get('userId')
    if user is None:
        raise GraphQLError('Authorization Error')

    if len(places) != len(movies):
        raise GraphQLError(f"Wrong data")

    if len(places) != len(set(places)):
        raise GraphQLError("Duplicate ranking positions are not allowed")

    if any(lambda place: place > 5, places):
        raise GraphQLError(f"Only 5 places are supported")

    # lastPlace = UserRepo.GetUserRankingLastPlace(user)
    # if any(lambda place: lastPlace + 1 < place, places):
    #     raise GraphQLError(f"Wrong place")

    zipped = list(zip(places, movies))
    try:
        UserRepo.modify_users_ranking(user, zipped)
    except Exception as e:
        raise GraphQLError(f"Ranking update failed: {str(e)}")
    return True

