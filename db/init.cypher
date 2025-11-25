// --- 1. Czyszczenie
MATCH (n) DETACH DELETE n;

// Użytkownik nie ma dwóch n-tych miejsc
CREATE CONSTRAINT unique_user_ranking IF NOT EXISTS
FOR ()-[r:RANKED]-()
REQUIRE (r.position, r.userId) IS UNIQUE;

//tylko jedna krawedź od użytkownika do filmu w rankingu
CREATE CONSTRAINT unique_user_movie_ranking IF NOT EXISTS
FOR ()-[r:RANKED]->()
REQUIRE (r.userId, r.movieId) IS UNIQUE;

// --- 2. Gatunki filmowe
CREATE (:Genre {name: 'COMEDY'});
CREATE (:Genre {name: 'HORROR'});
CREATE (:Genre {name: 'DRAMA'});
CREATE (:Genre {name: 'THRILLER'});
CREATE (:Genre {name: 'ACTION'});
CREATE (:Genre {name: 'SCIFI'});
CREATE (:Genre {name: 'FANTASY'});

// --- 3. Aktorzy
CREATE (a1:Actor {id: '1', fullname: 'Keanu Reeves'});
CREATE (a2:Actor {id: '2', fullname: 'Laurence Fishburne'});
CREATE (a3:Actor {id: '3', fullname: 'Carrie-Anne Moss'});

// --- 4. Reżyserzy
CREATE (d1:Director {id: '1', fullname: 'Lana Wachowski'});
CREATE (d2:Director {id: '2', fullname: 'Lilly Wachowski'});

// --- 5. Filmy
CREATE (m1:Movie {id: '1', title: 'Matrix', year: 1999, rating: 8.7, numberOfGrades: 120});
CREATE (m2:Movie {id: '2', title: 'John Wick', year: 2014, rating: 7.4, numberOfGrades: 65});

// --- 6. Film <-> Aktor
MATCH (m:Movie {id:'1'}), (a:Actor) WHERE a.id IN ['1','2','3']
CREATE (a)-[:ACTED_IN]->(m);

MATCH (m:Movie {id:'2'}), (a:Actor) WHERE a.id = '1'
CREATE (a)-[:ACTED_IN]->(m);

// --- 7. Film <-> Reżyser
MATCH (m:Movie {id:'1'}), (d:Director) WHERE d.id IN ['1','2']
CREATE (d)-[:DIRECTED]->(m);

MATCH (m:Movie {id:'2'}), (d:Director) WHERE d.id = '1'
CREATE (d)-[:DIRECTED]->(m);

// --- 8. Gatunki filmowe
MATCH (m:Movie {id:'1'}), (g:Genre {name:'SCIFI'}) CREATE (g)-[:IS_GENRE]->(m);
MATCH (m:Movie {id:'2'}), (g:Genre {name:'ACTION'}) CREATE (g)-[:IS_GENRE]->(m);

// --- 9. Bazowy użytkownik
// CREATE (u1:User {id:'1', username:'igor'});

// --- 10. Ulubione filmy użytkownika
// MATCH (u:User {id:'1'}), (m:Movie {id:'1'}) CREATE (u)-[:FAVORITE]->(m);
// MATCH (u:User {id:'1'}), (m:Movie {id:'2'}) CREATE (u)-[:FAVORITE]->(m);

// --- 11. Rating użytkownika // bedzie inny
// MATCH (u:User {id:'1'}), (m:Movie {id:'1'}) CREATE (r:Rating {stars:5})-[:OF_MOVIE]->(m)-[:RATED_BY]->(u);
