#!/bin/bash

# create volume if it doesn't already exist
exists=`docker volume ls | awk '{print $2}' | grep a2rchi-dev-data`
if [[ $exists != 'a2rchi-dev-data' ]]; then
    docker volume create --name a2rchi-dev-data
fi

# start services
echo "Starting docker compose"
cd A2rchi/deploy/
docker compose -f dev-compose.yaml up -d --build --force-recreate --always-recreate-deps

# secrets files are created by CI pipeline and destroyed here
rm cleo_*.txt
rm imap_*.txt
rm sender_*.txt
rm flask_uploader_app_secret_key.txt
rm uploader_salt.txt
rm openai_api_key.txt
