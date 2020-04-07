#!/bin/bash

set -e

cd "$(dirname "${BASH_SOURCE[0]}")/.."

docker build -t vaknin/bubbles .

cd "deploy"
docker-compose up