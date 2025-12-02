from graphql import GraphQLError

from repositories.MovieRepository import MovieRepo
from repositories.UserRepository import UserRepo
from .types import query, user, mutation
from graphql import GraphQLError

@query.field("searchUsers")
def resolve_users_by_prefix(_, info, **kwargs):
    prefix = kwargs.get('prefix')
    # user repository method is `find_users_by_prefix`
    return UserRepo.find_users_by_prefix(prefix)

@query.field("user")
def resolve_user(_, info, **kwargs):
    idx = kwargs.get('id')
    return UserRepo.find_user_by_id(idx)


@query.field("me")
def resolve_me_query(_, info):
    try:
        viewer = info.context.get('userId')
        if not viewer:
            return None
        return UserRepo.find_user_by_id(viewer)
    except GraphQLError:
        return None

@user.field("me")
def resolve_user_me_field(obj, info, **kwargs):
    # obj is a dict-like user object returned by find_user_by_id
    viewer = info.context.get('userId')
    if not viewer:
        return False
    try:
        return str(obj.get('id')) == str(viewer)
    except Exception:
        return False

@user.field("favoriteGenres")
def resolve_user_favorite_genres(obj, info, **kwargs):
    idx = obj.get('id')
    return UserRepo.find_user_favorite_genres_by_id(idx)

@user.field("friends")
def resolve_user_friends(obj, info, **kwargs):
    idx = obj.get('id')
    return UserRepo.find_user_friends(idx)

@user.field("favoriteMovies")
def resolve_user_favorite_movies(obj, info, **kwargs):
    idx = obj.get('id')
    return UserRepo.find_user_favorite_movies_by_id(idx)


def _friend_or_pending(obj, info, func):
    friend_id = obj.get('id')
    my_id = info.context.get('userId')

    if my_id:
        if friend_id == my_id:
            return False
        friends = func(my_id)
        friends_ids = map(lambda x: x.get('id'), friends)
        if friend_id in friends_ids:
            return True
    return False

@user.field("isFriend")
def resolve_user_is_friend(obj, info, **kwargs):
    return _friend_or_pending(obj, info, UserRepo.find_user_friends)

@user.field("isPendingFromMe")
def resolve_user_is_pending_from_me(obj, info, **kwargs):
    return _friend_or_pending(obj, info, UserRepo.find_friend_request_from_me)

@user.field("isPendingToMe")
def resolve_user_is_pending_to_me(obj, info, **kwargs):
    return _friend_or_pending(obj, info, UserRepo.find_friend_request_to_me)

@user.field("pendingFromMe")
def resolve_pending_from_me(obj, info, **kwargs):
    my_id = info.context.get('userId')
    return UserRepo.find_friend_request_from_me(my_id)

@user.field("pendingToMe")
def resolve_pending_to_me(obj, info, **kwargs):
    my_id = info.context.get('userId')
    return UserRepo.find_friend_request_to_me(my_id)

@user.field("ratings")
def resolve_user_ratings(obj, info, **kwargs):
    idx = obj.get('id')
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
    return True

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

@mutation.field("modifyUserRanking")
def resolve_modify_user_ranking(_, info, places, movies):
    user = info.context.get('userId')
    if user is None:
        raise GraphQLError('Authorization Error')

    if len(places) != len(movies):
        raise GraphQLError(f"Wrong data")

    if len(places) != len(set(places)):
        raise GraphQLError("Duplicate ranking positions are not allowed")

    if any(map(lambda place: place > 5, places)):
        raise GraphQLError(f"Only 5 places are supported")

    # wyrownanie miejsc w liscie
    zipped = list(zip(places, movies))
    zipped = sorted(zipped, key=lambda x: x[0])
    i = 0
    def func(zipped_obj):
        nonlocal i
        i += 1
        return i, zipped_obj[1]
    zipped = list(map(func, zipped))
    try:
        UserRepo.modify_users_ranking(user, zipped)
    except Exception as e:
        raise GraphQLError(f"Ranking update failed: {str(e)}")
    return True

@query.field("rating")
def resolve_user_rate(_, info, **kwargs):
    user = info.context.get('userId')
    try:
        if user is None:
            raise GraphQLError('Authorization Error')
        movie = kwargs.get("movieId")
        return UserRepo.find_movie_stars_by_user_id(user, movie)
    except GraphQLError as e:
        return None