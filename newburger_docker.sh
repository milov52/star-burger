#!/bin/bash
set -e

cd /opt/star-burger/infra

git fetch
git pull
docker compose -f docker-compose.prod.yml --build up -d

echo star-burged was updated and it will work soon!
