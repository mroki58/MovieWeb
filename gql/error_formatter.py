from ariadne import format_error
from neo4j import exceptions as neo4j_exceptions

def custom_error_formatter(error, debug):
    original_error = getattr(error, 'original_error', None)

    if isinstance(original_error, neo4j_exceptions.ServiceUnavailable):
        return {
            "message": "Database is unavailable",
            "code": "DB_UNAVAILABLE"
        }

    if isinstance(original_error, neo4j_exceptions.ClientError):
            return {
                "message": "Neo4j query error",
                "code": "QUERY_ERROR"
            }

    return format_error(error, debug)
