from db.init_db import get_driver
from repositories.mixins.PrefixMixin import PrefixMixin

cmd1 =  """
        MATCH (m:Movie {id: $idx})<-[:IS_GENRE]-(g:Genre)
        RETURN m, g.name as genre
        """

cmd2 =  """
        MATCH (a:{agent})-[:{role}]->(m:Movie {{id: $movie_id}})
        RETURN a.id as id, a.fullname as fullname
        """


class MovieRepository(PrefixMixin):
    def __init__(self):
        self.driver = get_driver()

    def find_movie_by_id(self, idx):
        cmd = cmd1
        with self.driver.session() as session:
            result = session.run(
                cmd,
                idx=idx
            )
            single = result.single()
            if not single:
                return None
            genre = single.get('genre')
            record = single.get('m')

        if not record:
            return None

        return {
            "id": record["id"],
            "title": record["title"],
            "year": record["year"],
            "rating": record["rating"],
            "numberOfGrades": record["numberOfGrades"],
            "genre": genre
        }

    def _find_movie_actors_director(self, idx, agent, role):
        cmd = cmd2.format(agent=agent, role=role)
        with self.driver.session() as session:
            result = session.run(
                cmd,
                movie_id=idx
            )
            res = list(result)
        return res

    def find_movie_actors_by_id(self, idx):
        return self._find_movie_actors_director(
            idx,
            agent='Actor',
            role='ACTED_IN'
        )

    def find_movie_director_by_id(self, idx):
        directors = self._find_movie_actors_director(
            idx,
            agent='Director',
            role='DIRECTED'
        )
        return directors[0] if directors else None

    def find_movie_starting_with_prefix(self, prefix):
        return self.find_element_by_prefix(
            element_name='Movie',
            search_name='title',
            prefix=prefix
        )

MovieRepo = MovieRepository()