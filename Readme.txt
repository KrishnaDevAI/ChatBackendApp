******** Redis *********
-- This command Stop the Redis

sudo service redis-server stop

--Check command Redis is Runing or no --

redis-cli ping

********** Docker command *********

docker build -t django-app .
docker run -p 8000:8000 django-app
docker ps
docker images
docker stop <container>

---- If Docker Already Runing and if you need to remove use this run command below
docker rm -f my-redis

---- Docker Through Run Redis command
docker run --name my-redis -p 6379:6379 -d redis


********** Celery command

celery -A ChatApp worker --loglevel=info --pool=solo



*************************** To run all services at once use ***************************

docker-compose up --build