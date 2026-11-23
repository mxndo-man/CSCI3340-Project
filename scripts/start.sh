#!/usr/bin/env bash

# Example chmod +x ./scripts/start.sh
# Usage: ./scripts/start.sh  
# ./start.sh will have four modes to use.
# HOW TO USE EXAMPLE
# ./start.sh up: will start up the containers.
# ./start.sh down: will shut down the containers.
# ./start.sh restart: will restart on the containers.
# ./start.sh logs: will show the logs to the containers.

set -euo pipefail

#This ensures that we are in the ./app and not in ./foo/bar/scripts
SCRIPT_PATH=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "$SCRIPT_PATH/.."

if [[ ! -f .env ]]; then 
  echo ".env is not present. Create one with .env.example, or update">&2
  exit 1
fi

usage(){
  echo "Usage: $0 {up|down|restart|logs}"
  exit 1
}

if [ $# -lt 1 ]; then
  usage
fi 

case "$1" in 
  up)
    echo "Configure Docker"
    docker compose config --quiet 

    echo "Starting containers and waiting for healthchecks..."
    docker compose up -d --build --wait

    echo "Running migrations..."
    docker compose exec -T app python manage.py migrate
    
    echo "Checking status"
    docker compose ps 
    ;;
  down)
    echo "Stopping containers"
    docker compose stop
    docker compose ps 
    ;;
  restart)
    ;;
  logs)
    echo "Checking logs on the user"
    docker compose logs -f 
    ;;
  *)
    usage
    ;;
esac

