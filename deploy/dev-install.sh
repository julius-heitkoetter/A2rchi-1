#!/bin/bash

echo "Going into A2rchi directory"
cd A2rchi
echo "Starting docker compose"
cd deploy
docker-compose rm -f
docker-compose pull
docker compose up -d --build --no-cache

# secrets files are created by CI pipeline and destroyed here
rm cleo_url.txt
rm cleo_user.txt
rm cleo_pw.txt
rm cleo_project.txt
rm openai_api_key.txt
