from .types import query, movie, user, mutation
from .movie_resolvers import *
from .user_resolver import *

__all__ = ["query", "movie", "user", "mutation"]