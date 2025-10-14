#!/bin/bash

if [ "$(docker ps -q -f name=neo4j-db)" ]; then
    echo "Kontener neo4j-db działa, zatrzymuję go..."
    docker compose stop
fi

docker compose up -d

echo "Czekam na Neo4j..."
until docker exec neo4j-db cypher-shell -u neo4j -p udhuhsdfuhs126hifds "RETURN 1;" &> /dev/null
do
  sleep 2
done

echo "Ładowanie init.cypher"
docker exec -i neo4j-db cypher-shell -u neo4j -p udhuhsdfuhs126hifds < ./neo4j/init.cypher

echo "Gotowe!"
