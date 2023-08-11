while ! nc -z psql_movies 5432; do sleep 5; echo 'psql not ready yet'; done; 
while ! nc -z redis_movies 6379; do sleep 5; echo 'redis not ready yet'; done; 
while ! nc -z es_movies 9200; do sleep 5; echo 'elasticsearch not ready yet'; done; 

while [[ "$(curl -s -o /dev/null -w ''%{http_code}'' es_movies:9200)" != "200" ]]; do sleep 5; done;

curl -XPUT http://es_movies:9200/movies -H 'Content-Type: application/json' -d @movies.json

python run.py

