from db.init_db import get_driver
from helpers.utils import with_session, pick_fields
from repositories.mixins.PrefixMixin import PrefixMixin

cmd1 =  """
        MATCH (m:Movie {id: $idx})<-[:IS_GENRE]-(g:Genre)
        RETURN m, g.name as genre
        """

cmd2 =  """
        MATCH (a:{agent})-[:{role}]->(m:Movie {{id: $movie_id}})
        RETURN a.id as id, a.fullname as fullname
        """


def _record_to_movie(record, node_key='m', genre_key='genre'):
    node = record.get(node_key)
    if not node:
        return None
    genre = record.get(genre_key)
    return pick_fields(node, ["id", "title", "year", "rating", "numberOfGrades"]) | {"genre": genre}


class MovieRepository(PrefixMixin):
    def __init__(self):
        self.driver = get_driver()

    @with_session
    def find_movie_by_id(self, idx, session=None):
        cmd = cmd1
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

    @with_session
    def _find_movie_actors_director(self, idx, agent, role, session=None):
        cmd = cmd2.format(agent=agent, role=role)
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

    @with_session
    def find_newest_movies(self, limit=10, session=None):
        cmd = """
            MATCH (m:Movie)
            OPTIONAL MATCH (m)<-[:IS_GENRE]-(g:Genre)
            RETURN m, g.name as genre
            ORDER BY m.year DESC
            LIMIT $limit
        """
        result = session.run(cmd, limit=limit)
        movies = []
        for record in result:
            m = _record_to_movie(record)
            if m:
                movies.append(m)
        return movies

    @with_session
    def find_newest_movies_with_cast(self, limit=10, session=None):
        cmd = """
            MATCH (m:Movie)
            OPTIONAL MATCH (m)<-[:IS_GENRE]-(g:Genre)
            WITH m, g
            ORDER BY m.year DESC
            LIMIT $limit
            OPTIONAL MATCH (a:Actor)-[:ACTED_IN]->(m)
            OPTIONAL MATCH (d:Director)-[:DIRECTED]->(m)
            RETURN m, g.name as genre, collect({id: a.id, fullname: a.fullname}) as actors, head(collect({id: d.id, fullname: d.fullname})) as director
        """
        result = session.run(cmd, limit=limit)
        out = []
        for record in result:
            movie_obj = _record_to_movie(record)
            if not movie_obj:
                continue
            actors = record.get('actors') or []
            director = record.get('director')
            out.append({
                'movie': movie_obj,
                'actors': actors,
                'director': director
            })
        return out

    @with_session
    def find_random_movies(self, limit=10, session=None):
        cmd = """
            MATCH (m:Movie)
            OPTIONAL MATCH (m)<-[:IS_GENRE]-(g:Genre)
            RETURN m, g.name as genre
            ORDER BY rand()
            LIMIT $limit
        """
        result = session.run(cmd, limit=limit)
        movies = []
        for record in result:
            m = _record_to_movie(record)
            if m:
                movies.append(m)
        return movies

    @with_session
    def find_movies_from_friends(self, user_id, exclude_user_id=None, limit=30, session=None):
        if exclude_user_id is None:
            exclude_user_id = user_id

        cmd = """
            MATCH (u:User {id:$user})-[:FRIEND]->(f:User)-[r]->(m:Movie)
            WHERE type(r) IN ['RATED','RANKED']
            OPTIONAL MATCH (ex:User {id:$exclude})-[er]->(m)
            WHERE type(er) IN ['RATED','RANKED']
            WITH m, er
            WHERE er IS NULL
            OPTIONAL MATCH (m)<-[:IS_GENRE]-(g:Genre)
            RETURN DISTINCT m, g.name as genre
            LIMIT $limit
        """
        result = session.run(cmd, user=user_id, exclude=exclude_user_id, limit=limit)
        movies = []
        for record in result:
            m = _record_to_movie(record)
            if m:
                movies.append(m)
        return movies


MovieRepo = MovieRepository()