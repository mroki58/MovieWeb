#!/usr/bin/env python3
"""Recalculate and store average ratings and counts for all movies.

This script updates each Movie node with two properties:
- `rating` (average of r.stars from RATED relationships)
- `numberOfGrades` (count of RATED relationships)

Intended to be run periodically (e.g. from cron).
"""
from db.init_db import get_driver


def main():
    driver = get_driver()
    with driver.session() as session:
        result = session.run(
            """
            MATCH (m:Movie)
            OPTIONAL MATCH (u)-[r:RATED]->(m)
            WITH m, avg(r.stars) AS avgRating, count(r) AS cnt
            SET m.rating = avgRating, m.numberOfGrades = cnt
            RETURN count(m) AS updated
            """
        )
        single = result.single()
        updated = single["updated"] if single and "updated" in single else 0
        print(f"Recalculated ratings for {updated} movies")


if __name__ == '__main__':
    main()
