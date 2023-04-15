#!/bin/bash
set -e

cd /opt/star-burger/infra

docker compose -f docker-compose.prod.yml down
git fetch
git pull
docker compose -f docker-compose.prod.yml --build up -d

echo star-burged was updated and it will work soon!
