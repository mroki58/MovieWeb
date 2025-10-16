from db.init_db import get_driver
from repositories.mixins import MovieQueryMixin
from repositories.mixins.PrefixMixin import PrefixMixin


class ActorRepository(MovieQueryMixin, PrefixMixin):
    def __init__(self, driver):
        self.driver = driver

    def find_actors_movies(self, actor_id):
        return self._find_actors_director_movies(
            actor_id,
            agent="Actor",
            role="ACTED_IN",
        )

    def find_actors_by_prefix(self, prefix):
        return self.find_element_by_prefix(
            element_name="Actor",
            search_name="fullname",
            prefix=prefix,
        )

ActorRepo = ActorRepository(get_driver())