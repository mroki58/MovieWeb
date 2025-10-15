cmd1 =  """
        MATCH (a:{agent} {{id: $idx}})-[:{role}]->(m:Movie)
        MATCH (g:Genre)-[:IS_GENRE]->(m)
        RETURN m, g.name as genre
        """

def pick_fields(node, fields):
    return {k: v for k, v in dict(node).items() if k in fields}

class ActorDirectorMixin:
    def _find_actors_director_movies(self, idx, agent, role):
        cmd = cmd1.format(agent=agent, role=role)
        fields_to_return = ["id", "title", "year", "rating", "numberOfGrades"]

        with self.driver.session() as session:
            result = session.run(cmd, idx=idx)
            movies = []
            for i, record in enumerate(result):
                movies.append(pick_fields(record['m'], fields_to_return))
                movies[i]['genre'] = record.get('genre')
        return movies