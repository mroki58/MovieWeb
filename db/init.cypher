MATCH (n) DETACH DELETE n;

CREATE CONSTRAINT unique_user_ranking IF NOT EXISTS
FOR ()-[r:RANKED]-()
REQUIRE (r.position, r.userId) IS UNIQUE;

CREATE CONSTRAINT unique_user_movie_ranking IF NOT EXISTS
FOR ()-[r:RANKED]->()
REQUIRE (r.userId, r.movieId) IS UNIQUE;

CREATE (:Genre {name: 'COMEDY'});
CREATE (:Genre {name: 'HORROR'});
CREATE (:Genre {name: 'DRAMA'});
CREATE (:Genre {name: 'THRILLER'});
CREATE (:Genre {name: 'ACTION'});
CREATE (:Genre {name: 'SCIFI'});
CREATE (:Genre {name: 'FANTASY'});

CREATE (a1:Actor  {id: '1',  fullname: 'Keanu Reeves'});
CREATE (a2:Actor  {id: '2',  fullname: 'Laurence Fishburne'});
CREATE (a3:Actor  {id: '3',  fullname: 'Carrie-Anne Moss'});

CREATE (a4:Actor  {id: '4',  fullname: 'Uma Thurman'});
CREATE (a5:Actor  {id: '5',  fullname: 'John Travolta'});
CREATE (a6:Actor  {id: '6',  fullname: 'Samuel L. Jackson'});
CREATE (a7:Actor  {id: '7',  fullname: 'Harvey Keitel'});
CREATE (a8:Actor  {id: '8',  fullname: 'Tim Roth'});
CREATE (a9:Actor  {id: '9',  fullname: 'Michael Madsen'});
CREATE (a10:Actor {id: '10', fullname: 'Christoph Waltz'});
CREATE (a11:Actor {id: '11', fullname: 'Jamie Foxx'});
CREATE (a12:Actor {id: '12', fullname: 'Leonardo DiCaprio'});
CREATE (a13:Actor {id: '13', fullname: 'Brad Pitt'});
CREATE (a14:Actor {id: '14', fullname: 'Diane Kruger'});

CREATE (a15:Actor {id: '15', fullname: 'Christian Bale'});
CREATE (a16:Actor {id: '16', fullname: 'Heath Ledger'});
CREATE (a17:Actor {id: '17', fullname: 'Joseph Gordon-Levitt'});
CREATE (a18:Actor {id: '18', fullname: 'Tom Hardy'});

CREATE (d1:Director {id: '1', fullname: 'Lana Wachowski'});
CREATE (d2:Director {id: '2', fullname: 'Quentin Tarantino'});
CREATE (d3:Director {id: '3', fullname: 'Christopher Nolan'});
CREATE (d4:Director {id: '4', fullname: 'Chad Stahelski'});


CREATE (m1:Movie {id: '1',  title: 'The Matrix',        year: 1999, rating: 8.7, numberOfGrades: 120});
CREATE (m2:Movie {id: '2',  title: 'John Wick',         year: 2014, rating: 7.4, numberOfGrades: 65});
CREATE (m3:Movie {id: '3',  title: 'Pulp Fiction',      year: 1994, rating: 8.9, numberOfGrades: 200});
CREATE (m4:Movie {id: '4',  title: 'Kill Bill: Vol. 1', year: 2003, rating: 8.1, numberOfGrades: 150});
CREATE (m5:Movie {id: '5',  title: 'Reservoir Dogs',    year: 1992, rating: 8.3, numberOfGrades: 110});
CREATE (m6:Movie {id: '6',  title: 'Django Unchained',  year: 2012, rating: 8.4, numberOfGrades: 180});
CREATE (m7:Movie {id: '7',  title: 'Inglourious Basterds', year: 2009, rating: 8.3, numberOfGrades: 170});
CREATE (m8:Movie {id: '8',  title: 'Inception',         year: 2010, rating: 8.8, numberOfGrades: 220});
CREATE (m9:Movie {id: '9',  title: 'The Dark Knight',   year: 2008, rating: 9.0, numberOfGrades: 250});

MATCH (m:Movie {id:'1'}), (a:Actor)
WHERE a.id IN ['1','2','3']
CREATE (a)-[:ACTED_IN]->(m);

MATCH (m:Movie {id:'2'}), (a:Actor)
WHERE a.id = '1'
CREATE (a)-[:ACTED_IN]->(m);

MATCH (m:Movie {id:'3'}), (a:Actor)
WHERE a.id IN ['5','6','7']
CREATE (a)-[:ACTED_IN]->(m);

MATCH (m:Movie {id:'4'}), (a:Actor)
WHERE a.id IN ['4','7','9']
CREATE (a)-[:ACTED_IN]->(m);

MATCH (m:Movie {id:'5'}), (a:Actor)
WHERE a.id IN ['7','8','9']
CREATE (a)-[:ACTED_IN]->(m);

MATCH (m:Movie {id:'6'}), (a:Actor)
WHERE a.id IN ['10','11','12']
CREATE (a)-[:ACTED_IN]->(m);

MATCH (m:Movie {id:'7'}), (a:Actor)
WHERE a.id IN ['10','13','14']
CREATE (a)-[:ACTED_IN]->(m);

MATCH (m:Movie {id:'8'}), (a:Actor)
WHERE a.id IN ['12','15','17','18']
CREATE (a)-[:ACTED_IN]->(m);

MATCH (m:Movie {id:'9'}), (a:Actor)
WHERE a.id IN ['15','16','18']
CREATE (a)-[:ACTED_IN]->(m);

MATCH (m:Movie {id:'1'}),  (d:Director {id:'1'}) CREATE (d)-[:DIRECTED]->(m);
MATCH (m:Movie {id:'2'}),  (d:Director {id:'4'}) CREATE (d)-[:DIRECTED]->(m);

MATCH (m:Movie {id:'3'}),  (d:Director {id:'2'}) CREATE (d)-[:DIRECTED]->(m);
MATCH (m:Movie {id:'4'}),  (d:Director {id:'2'}) CREATE (d)-[:DIRECTED]->(m);
MATCH (m:Movie {id:'5'}),  (d:Director {id:'2'}) CREATE (d)-[:DIRECTED]->(m);
MATCH (m:Movie {id:'6'}),  (d:Director {id:'2'}) CREATE (d)-[:DIRECTED]->(m);
MATCH (m:Movie {id:'7'}),  (d:Director {id:'2'}) CREATE (d)-[:DIRECTED]->(m);

MATCH (m:Movie {id:'8'}),  (d:Director {id:'3'}) CREATE (d)-[:DIRECTED]->(m);
MATCH (m:Movie {id:'9'}),  (d:Director {id:'3'}) CREATE (d)-[:DIRECTED]->(m);

MATCH (m:Movie {id:'1'}), (g:Genre {name:'SCIFI'})
CREATE (g)-[:IS_GENRE]->(m);

MATCH (m:Movie {id:'2'}), (g:Genre {name:'ACTION'})
CREATE (g)-[:IS_GENRE]->(m);

MATCH (m:Movie {id:'3'}), (g:Genre {name:'DRAMA'})
CREATE (g)-[:IS_GENRE]->(m);

MATCH (m:Movie {id:'4'}), (g:Genre {name:'ACTION'})
CREATE (g)-[:IS_GENRE]->(m);

MATCH (m:Movie {id:'5'}), (g:Genre {name:'THRILLER'})
CREATE (g)-[:IS_GENRE]->(m);

MATCH (m:Movie {id:'6'}), (g:Genre {name:'DRAMA'})
CREATE (g)-[:IS_GENRE]->(m);

MATCH (m:Movie {id:'7'}), (g:Genre {name:'ACTION'})
CREATE (g)-[:IS_GENRE]->(m);

MATCH (m:Movie {id:'8'}), (g:Genre {name:'SCIFI'})
CREATE (g)-[:IS_GENRE]->(m);

MATCH (m:Movie {id:'9'}), (g:Genre {name:'ACTION'})
CREATE (g)-[:IS_GENRE]->(m);
