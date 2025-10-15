import uuid

from db.init_db import get_driver
from helpers.utils import pick_fields
from repositories.mixins.PrefixMixin import PrefixMixin


class UserRepository(PrefixMixin):
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
    def find_users_id_password_by_username(self, username):
        with self.driver.session() as session:
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

    def is_user_registered(self, username):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (u:User {username:$username}) RETURN u",
                username=username
            )
            if result.single():
                return True
        return False

    def register_user(self, **kwargs):
        username = kwargs.get("username")
        password = kwargs.get("password")
        email = kwargs.get("email")
        idx = str(uuid.uuid4())

        with self.driver.session() as session:
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

    def add_interests_for_user(self, idx, interests):
        with self.driver.session() as session:
            session.run(
                """
                MATCH (u:User {id:$idx})
                UNWIND $interests AS interest_name
                MATCH (g:Genre {name: interest_name})
                MERGE (u)-[:HAS_INTEREST]->(g)
                """,
                id=idx,
                interests=interests
            )
        return True

    def find_user_favorite_genres_by_id(self, idx):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (u:User {id:$idx}) -[:HAS_INTEREST]->(g)
                RETURN collect(g) AS genres
                """
            )
            record = result.single()
        genres = record["genres"] if record else []
        return genres

    def find_ratings_by_user_id(self, idx):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (u:User {id: $idx})-[r:RATED]->(m:Movie)
                RETURN r.stars AS stars, m.id AS movie_id
                """,
                idx=idx
            )
            res = list(result)
        return res

    def rate_movie(self, user, movie, stars):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (u: User {id: $user})
                MATCH (m: Movie {id: $movie})
                MERGE (u)-[r:RATED {stars: $stars}]->(m) 
                """,
                user=user,
                movie=movie,
                stars=stars
            )

UserRepo = UserRepository(get_driver())