import uuid

from db.init_db import get_driver
from helpers.utils import pick_fields, with_session
from repositories.mixins import MovieQueryMixin
from repositories.mixins import PrefixMixin



class UserRepository(PrefixMixin, MovieQueryMixin):
    fields_to_return = ["id", "username", "email"]

    def __init__(self, driver):
        self.driver = driver

    def find_users_by_prefix(self, prefix):
        result = self.find_element_by_prefix(
            element_name="User",
            search_name="username",
            prefix=prefix
        )

        users = []
        for record in result:
            users.append(pick_fields(record, UserRepository.fields_to_return))
        return result

    def find_user_by_id(self, idx):
        result = self.find_element_by_prefix(
            element_name="User",
            search_name="id",
            prefix=idx
        )

        users = []
        for record in result:
            users.append(pick_fields(record, UserRepository.fields_to_return))

        return users[0] if users else None

    # try-catch do tych czterech bo nie korzystamy z nich w graphql
    @with_session
    def find_users_id_password_by_username(self, username, session=None):
        result = session.run(
            """
            MATCH (u:User {username:$username}) 
            RETURN u.password AS password, u.id AS id
            """,
            username=username
        )
        record = result.single()
        if record:
            hashed_pw = record["password"].encode("utf-8")
            idx = record["id"]

        return hashed_pw, idx

    @with_session
    def is_user_registered(self, username, session=None):
        result = session.run(
            "MATCH (u:User {username:$username}) RETURN u",
            username=username
        )
        if result.single():
            return True
        return False

    @with_session
    def register_user(self, session=None,**kwargs):
        username = kwargs.get("username")
        password = kwargs.get("password")
        email = kwargs.get("email")
        idx = str(uuid.uuid4())
        session.run(
            """
            CREATE (u:User {
                id:$id,
                username:$username,
                password:$password,
                email:$email
            })
            """,
            id=idx,
            username=username,
            password=password,
            email=email
        )

        return idx

    @with_session
    def add_interests_for_user(self, idx, interests, session=None):
        session.run(
            """
            MATCH (u:User {id:$idx})
            UNWIND $interests AS interest_name
            MATCH (g:Genre {name: interest_name})
            MERGE (u)-[:HAS_INTEREST]->(g)
            """,
            idx=idx,
            interests=interests
        )
        return True

    @with_session
    def find_user_favorite_genres_by_id(self, idx, session=None):
        result = session.run(
            """
            MATCH (u:User {id:$idx}) -[:HAS_INTEREST]->(g)
            RETURN collect(g) AS genres
            """,
            idx=idx
        )
        record = result.single()
        genres = record["genres"] if record else []
        return genres

    @with_session
    def find_ratings_by_user_id(self, idx, session=None):
        result = session.run(
            """
            MATCH (u:User {id: $idx})-[r:RATED]->(m:Movie)
            RETURN r.stars AS stars, m.id AS movie_id
            """,
            idx=idx
        )
        res = list(result)
        return res

    @with_session
    def rate_movie(self, user, movie, stars, session=None):
        session.run(
            """
            MATCH (u: User {id: $user})
            MATCH (m: Movie {id: $movie})
            MERGE (u)-[r:RATED {stars: $stars}]->(m) 
            """,
            user=user,
            movie=movie,
            stars=stars
        )
    @with_session
    def unrate_movie(self, user, movie, session=None):
        session.run(
            """
            MATCH (u:User {id: $user})-[r:RATED]->(m:Movie)
            WHERE m.id = $movie
            DELETE r
            """,
            user=user,
            movie=movie
        )

    @with_session
    def send_friend_request(self, me, friend, session=None):
        result = session.run(
            """
            MATCH (u:User {id: $me})
            MATCH (f:User {username: $friend})
            WHERE u IS NOT NULL AND f IS NOT NULL
            MERGE (u)-[:FRIEND_REQUEST]->(f)
            RETURN u, f
            """,
            me=me,
            friend=friend
        )
        record = result.single()
        if not record:
            raise ValueError("Nie znaleziono użytkownika lub znajomego")

    @with_session
    def accept_friend_request(self, me, friend, session=None):
        result = session.run(
            """
            MATCH (u:User {id: $me})
            MATCH (f: User {username: $friend})
            WHERE u IS NOT NULL AND f IS NOT NULL
            MERGE (u)-[:FRIEND]->(f)
            MERGE (f)-[:FRIEND]->(u)
            RETURN u, f
            """,
            me=me,
            friend=friend
        )
        record = result.single()
        if not record:
            raise ValueError("Nie znaleziono użytkownika lub znajomego")

    @with_session
    def delete_friend_request(self, me, friend, session=None):
        session.run(
            """
            MATCH (u:User {id: $me})<-[r:FRIEND_REQUEST]-(f: User {username: $friend})
            DELETE r
            """,
            me=me,
            friend=friend,
        )
    @with_session
    def delete_friend(self, me, friend, session=None):
        session.run(
            """
            MATCH (u:User {id: $me})-[r1:FRIEND]->(f: User {username: $friend})
            MATCH (f)-[r2:FRIEND]->(u)
            DELETE r1, r2
            """,
            me=me,
            friend=friend,
        )

    @with_session
    def find_friend(self, me, session=None):

        result = session.run(
            """
            MATCH (u:User {id: $me})-[r1:FRIEND]->(f: User {username: $friend})
            RETURN collect(f.username) as friends
            """
        )

        record = result.single()
        friends = record["friends"] if record else []
        return friends


    @with_session
    def find_friend_requests(self, me, direction='from', session=None):
        cmd = ''
        if direction == 'from':
            cmd += 'MATCH (u:User {id: $me})-[r:FRIEND_REQUEST]->(f:User)'
        elif direction == 'to':
            cmd += 'MATCH (f:User)-[r:FRIEND_REQUEST]->(u:User {id: $me})'

        cmd +=  '''
                RETURN collect({id: f.id, username: f.username}) as friends
                '''

        result = session.run(
            cmd,
            me=me,
        )
        record = result.single()
        usernames = record['friends'] if record else []

        return usernames

    def find_friend_request_from_me(self, me):
        return self.find_friend_requests(
            me=me,
            direction='from'
        )

    def find_friend_request_to_me(self, me):
        return self.find_friend_requests(
            me=me,
            direction='to'
        )

    @with_session
    def modify_users_ranking(self, user, zipped, session=None):
        from neo4j.exceptions import ConstraintError
        from graphql import GraphQLError
        try:
            session.run(
                """
                MATCH (u:User {id: $user})
                UNWIND $zipped AS pair
                WITH u, pair[0] AS position, pair[1] AS movieId
                MATCH (m:Movie {id: movieId})
                OPTIONAL MATCH (u)-[r:RANKED]->(m)
                DELETE r
                MERGE (u)-[:RANKED {position: position}]->(m)
                """,
                user=user,
                zipped=zipped
            )
        except ConstraintError:
            raise GraphQLError("Duplicate ranking positions detected")

    def find_user_friends(self, idx):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (u:User {id: $id})
                MATCH (u)-[r:FRIEND]->(f:User)
                RETURN f
                """
            )
            result = [record['f'] for record in result]
        users = []
        for record in result:
            users.append(pick_fields(record, UserRepository.fields_to_return))
        return users

    @with_session
    def find_user_favorite_movies_by_id(self, idx, session=None):
        return self._find_user_favorite_movies(
            idx=idx,
            session=session
        )


UserRepo = UserRepository(get_driver())