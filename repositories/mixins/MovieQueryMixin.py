from helpers.utils import pick_fields, with_session
cmd1 =  """
        MATCH (a:{agent} {{id: $idx}})-[:{role}]->(m:Movie)
        MATCH (g:Genre)-[:IS_GENRE]->(m)
        RETURN m, g.name as genre
        """

cmd2 =  """
        MATCH (u:User {id: $idx})
        MATCH (u)-[r:RANKED]->(m:Movie)
        MATCH (m)<-[:IS_GENRE]-(g:Genre)
        RETURN m, g.name as genre, r.position as position
        ORDER BY r.position
        """

cmd3 =  """
        MATCH (m:Movie)<-[IS_GENRE]-(g:Genre)
        RETURN m, g.name as genre
        ORDER BY m.year
        LIMIT=$limit
        """

class MovieQueryMixin:
    fields_to_return = ["id", "title", "year", "rating", "numberOfGrades"]

    @with_session
    def _do_query_with_movie(self, cmd, session=None, **kwargs):
        result = session.run(cmd, **kwargs)
        movies = []
        for i, record in enumerate(result):
            movies.append(pick_fields(record['m'], MovieQueryMixin.fields_to_return))
            movies[i]['genre'] = record.get('genre')
        return movies

    def _find_actors_director_movies(self, idx, agent, role):
        cmd = cmd1.format(agent=agent, role=role)
        return self._do_query_with_movie(cmd, session=None, idx=idx)

    @with_session
    def _find_user_favorite_movies(self, idx, session=None):
        cmd = cmd2
        result = session.run(cmd, idx=idx)
        movies = []
        for record in result:
            movie_obj = pick_fields(record['m'], MovieQueryMixin.fields_to_return)
            movie_obj['genre'] = record.get('genre')
            movies.append({
                'position': record.get('position'),
                'movie': movie_obj
            })
        return movies

    def _find_newest_movies(self, limit):
        cmd = cmd3
        return self._do_query_with_movie(cmd, session=None,limit=limit)