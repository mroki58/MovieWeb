from helpers.utils import pick_fields
cmd1 =  """
        MATCH (a:{agent} {{id: $idx}})-[:{role}]->(m:Movie)
        MATCH (g:Genre)-[:IS_GENRE]->(m)
        RETURN m, g.name as genre
        """

class ActorDirectorMixin:
    fields_to_return = ["id", "title", "year", "rating", "numberOfGrades"]

    def _find_actors_director_movies(self, idx, agent, role):
        cmd = cmd1.format(agent=agent, role=role)

        with self.driver.session() as session:
            result = session.run(cmd, idx=idx)
            movies = []
            for i, record in enumerate(result):
                movies.append(pick_fields(record['m'], ActorDirectorMixin.fields_to_return))
                movies[i]['genre'] = record.get('genre')
        return movies