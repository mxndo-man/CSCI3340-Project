#!/usr/bin/env bash

# Make executable once: chmod +x ./scripts/start.sh
# Usage: ./scripts/start.sh {up|down|restart|reset|logs}
#
#   up       Build images and start all containers (migrations run automatically
#            via the one-shot "migrate" service in compose.yaml).
#   down     Stop the containers (data is kept).
#   restart  Stop and start the containers again (data is kept).
#   reset    Remove containers AND the database volume, then start fresh.
#   logs     Follow the logs of all containers.

set -euo pipefail

# Run from the project root, not from ./scripts
SCRIPT_PATH=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "$SCRIPT_PATH/.."

if [[ ! -f .env ]]; then
  echo ".env is not present. Create one from .env.example: cp .env.example .env" >&2
  exit 1
fi

usage() {
  echo "Usage: $0 {up|down|restart|reset|logs}"
  exit 1
}

up() {
  echo "Validating compose.yaml..."
  docker compose config --quiet

  echo "Building and starting containers, waiting for healthchecks..."
  docker compose up -d --build --wait

  echo "Container status:"
  docker compose ps
}

if [[ $# -lt 1 ]]; then
  usage
fi

case "$1" in
  up)
    up
    ;;
  down)
    echo "Stopping containers..."
    docker compose stop
    docker compose ps
    ;;
  restart)
    echo "Restarting containers..."
    docker compose down
    up
    ;;
  reset)
    read -r -p "This deletes the database volume. Continue? [y/N] " answer
    if [[ "$answer" =~ ^[Yy]$ ]]; then
      docker compose down -v
      up
    else
      echo "Cancelled."
    fi
    ;;
  logs)
    docker compose logs -f
    ;;
  *)
    usage
    ;;
esac
