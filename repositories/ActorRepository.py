from db.init_db import get_driver
from repositories.mixins import ActorDirectorMixin

class ActorRepository(ActorDirectorMixin):
    def __init__(self, driver):
        self.driver = driver

    def find_actors_movies(self, actor_id):
        return self._find_actors_director_movies(
            actor_id,
            agent="Actor",
            role="ACTED_IN",
        )

ActorRepo = ActorRepository(get_driver())