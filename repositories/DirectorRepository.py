from db.init_db import get_driver
from repositories.mixins import ActorDirectorMixin

class DirectorRepository(ActorDirectorMixin):
    def __init__(self, driver):
        self.driver = driver

    def find_directors_movies(self, actor_id):
        return self._find_actors_director_movies(
            actor_id,
            agent="Director",
            role="DIRECTED",
        )

    def find_directors_by_prefix(self, prefix):
        return self.find_element_by_prefix(
            element_name="Director",
            search_name="fullname",
            prefix=prefix,
        )


DirectorRepo = DirectorRepository(get_driver())