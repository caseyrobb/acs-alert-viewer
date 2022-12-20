#!/bin/bash
#
# Local testing with Podman

if [[ -z "$(podman pod ls | grep acs-alerts)" ]]; then
  printf "Creating pod..."
  podman pod create --name acs-alerts -p 5000:5000
  printf "OK\n"
  printf "Starting Redis..."
  podman run --name redis -dt --pod acs-alerts docker.io/redislabs/rejson
  REDISTATUS=$(podman ps --format json | jq -r '.[] | select(.Names[0] == "redis") | .State')
  until [[ "${REDISTATUS}" == "running" ]]; do
    sleep 1
    REDISTATUS=$(podman ps --format json | jq -r '.[] | select(.Names[0] == "redis") | .State')
  done
  printf "OK\n"
  
  printf "Starting acs-alert-viewer..."
  podman run --name acs-alert-viewer -dt --pod acs-alerts quay.io/carobb/acs-alert-viewer
  printf "OK\n\n"
  
  printf "\tNavigate to http://127.0.0.1:5000/\n\n"
else
  podman pod start acs-alerts 
  printf "\n\tNavigate to http://127.0.0.1:5000/\n\n"
fi
