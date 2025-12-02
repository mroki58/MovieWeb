#!/usr/bin/env python3
""" skrypt do tworzenia uzytkownikow - nie moglem go utworzyc w cypher, poniewaz uzylem bcrypt do hashowania hasel """
import os
import random
import time
import requests

BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5000')
REGISTER_URL = BASE_URL + '/register'
LOGIN_URL = BASE_URL + '/login'
GRAPHQL_URL = BASE_URL + '/graphql'

NUM_USERS = 6
USERS = [(f"user{i}", f"user{i}@example.com", f"123") for i in range(1, NUM_USERS + 1)]

random.seed(12345)

def graphql(session, query, variables=None):
    payload = {'query': query}
    if variables is not None:
        payload['variables'] = variables
    r = session.post(GRAPHQL_URL, json=payload)
    r.raise_for_status()
    return r.json()


def register_users():
    print('Registering users...')
    for username, email, password in USERS:
        payload = {'username': username, 'password': password, 'email': email}
        r = requests.post(REGISTER_URL, json=payload)
        if r.status_code in (200,201):
            print(f'Registered {username}')
        else:
            print(f'Failed to register {username}: {r.status_code} {r.text}')
        time.sleep(0.05)


def login_sessions():
    sessions = {}
    for username, email, password in USERS:
        s = requests.Session()
        r = s.post(LOGIN_URL, json={'username': username, 'password': password})
        if r.status_code == 200:
            print(f'Logged in {username}')
            sessions[username] = s
        else:
            print(f'Login failed for {username}: {r.status_code} {r.text}')
    return sessions


def fetch_movie_ids():
    # use unauthenticated session
    q = 'query { newMovies(limit: 1000) { id } }'
    r = requests.post(GRAPHQL_URL, json={'query': q})
    r.raise_for_status()
    data = r.json()
    ids = [m['id'] for m in data.get('data', {}).get('newMovies', [])]
    print(f'Found {len(ids)} movies')
    return ids


def build_social_graph(sessions):
    # simple social graph: each user sends a request to the next user
    username_list = [u[0] for u in USERS]
    n = len(username_list)
    for i, uname in enumerate(username_list):
        target = username_list[(i + 1) % n]
        s = sessions.get(uname)
        if not s:
            continue
        try:
            graphql(s, 'mutation($friend:String!){ friendRequest(friend:$friend) }', {'friend': target})
            print(f'Created friend request {uname} -> {target}')
        except Exception as e:
            print('Friend request error', uname, e)
        time.sleep(0.02)

    # Accept every other request (create some mutual friendships)
    for i in range(0, n, 2):
        accepter = username_list[(i + 1) % n]
        requester = username_list[i]
        sa = sessions.get(accepter)
        if not sa:
            continue
        try:
            graphql(sa, 'mutation($friend:String!){ friendRequestAccept(friend:$friend) }', {'friend': requester})
            print(f'{accepter} accepted {requester}')
        except Exception as e:
            print('Accept error', accepter, e)
        time.sleep(0.02)


def create_rankings_and_ratings(sessions, movie_ids):
    for idx, (username, _, _) in enumerate(USERS, start=1):
        s = sessions.get(username)
        if not s:
            continue
        # rankings: ensure every user gets 2..5 ranked movies
        count = random.randint(2,5)
        picks = random.sample(movie_ids, count)
        places = list(range(1, count+1))
        try:
            graphql(s, 'mutation($places:[Int!]!,$movies:[ID!]!){ modifyUserRanking(places:$places,movies:$movies) }', {'places': places, 'movies': picks})
            print(f'{username}: set ranking of {count} movies')
        except Exception as e:
            print('Ranking error for', username, e)

        # ratings: give each user ratings for 8..15 movies (random stars 0..10)
        rated_count = random.randint(8,15)
        rated = random.sample(movie_ids, min(rated_count, len(movie_ids)))
        for mid in rated:
            stars = random.randint(0,10)
            try:
                graphql(s, 'mutation($movieId:ID!,$stars:Int!){ rateMovie(movieId:$movieId,stars:$stars){ stars } }', {'movieId': mid, 'stars': stars})
            except Exception as e:
                print('Rating failed', username, mid, e)
        print(f'{username}: rated {len(rated)} movies')
        time.sleep(0.05)


def main():
    register_users()
    sessions = login_sessions()
    if not sessions:
        print('No sessions, aborting')
        return
    movie_ids = fetch_movie_ids()
    if not movie_ids:
        print('No movies found, aborting')
        return
    build_social_graph(sessions)
    create_rankings_and_ratings(sessions, movie_ids)
    print('Done')


if __name__ == '__main__':
    main()
