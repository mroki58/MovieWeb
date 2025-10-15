from ariadne import make_executable_schema, load_schema_from_path
from gql.resolvers import query, movie, user, mutation

type_defs = load_schema_from_path("gql/schema.graphql")

schema = make_executable_schema(
    type_defs,
    query,
    movie,
    user,
    mutation,
)
