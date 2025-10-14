from ariadne import QueryType

query = QueryType()

@query.field("movie")
def resolve_movie(_, info, **kwargs):
    driver = info.context.get('driver')
    idx = kwargs.get('id')




# @query.field("myRatings")
# def resolve_my_ratings(_, info):
#     from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
#     try:
#         verify_jwt_in_request()
#         user = get_jwt_identity()
#     except:
#         raise Exception("Not authenticated")
#
#     driver = info.context["driver"]
#     with driver.session() as session:
#         result = session.run(
#             """
#             MATCH (u:User {username:$username})-[r:RATED]->(m:Movie)
#             RETURN m.title AS title, r.rating AS rating
#             """,
#             username=user
#         )
#         return [{"title": record["title"], "rating": record["rating"]} for record in result]
