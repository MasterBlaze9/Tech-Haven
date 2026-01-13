#!/usr/bin/env bash
set -euo pipefail

# Simple wait-for-it style script using bash /dev/tcp
# Usage: wait-for-it.sh host:port -- optional command to exec after availability

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 host:port [-- command args]"
  exit 2
fi

hostport="$1"
shift || true

IFS=':' read -r host port <<< "$hostport"
if [ -z "$host" ] || [ -z "$port" ]; then
  echo "Invalid host:port: $hostport"
  exit 2
fi

WAIT_TIMEOUT=${WAIT_TIMEOUT:-60}
echo "Waiting for $host:$port (timeout=${WAIT_TIMEOUT}s)"
start_ts=$(date +%s)
while true; do
  if (echo > /dev/tcp/$host/$port) >/dev/null 2>&1; then
    echo "$host:$port is available"
    if [ "$#" -gt 0 ]; then
      exec "$@"
    else
      exit 0
    fi
  fi
  now_ts=$(date +%s)
  elapsed=$((now_ts - start_ts))
  if [ "$elapsed" -ge "$WAIT_TIMEOUT" ]; then
    echo "Timeout after ${WAIT_TIMEOUT}s waiting for $host:$port"
    exit 1
  fi
  sleep 1
done
