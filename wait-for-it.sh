#!/usr/bin/env bash

# Usage: wait-for-it.sh host:port -- command
# Wait for a service to become available before executing a command.

host=$(echo $1 | cut -d':' -f1)
port=$(echo $1 | cut -d':' -f2)
shift 1
cmd="$@"

# Check if nc (netcat) is installed
if ! command -v nc &> /dev/null; then
  echo "Error: nc (netcat) is not installed. Please install it to use wait-for-it.sh."
  exit 1
fi

echo "Waiting for $host:$port to be available..."

while ! nc -z "$host" "$port"; do
  sleep 1
done

echo "$host:$port is available! Executing command: $cmd"
exec $cmd
