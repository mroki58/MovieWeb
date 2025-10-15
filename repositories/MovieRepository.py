from db.init_db import get_driver

cmd1 =  """
        MATCH (m:Movie {id: $idx})<-[:IS_GENRE]-(g:Genre)
        RETURN m, g.name as genre
        """

cmd2 =  """
        MATCH (a:{agent})-[:{role}]->(m:Movie {{id: $movie_id}})
        RETURN a.id as id, a.fullname as fullname
        """


class MovieRepository:
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
            genre = single.get('genre')
            record = single.get('m')

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
            print(cmd)
            res = list(result)
            print(res)
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


MovieRepo = MovieRepository()