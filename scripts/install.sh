#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."


function main {
    python -m virtualenv .env --prompt "[bubbles] "
    find .env -name site-packages -exec bash -c 'echo "../../../../" > {}/self.pth' \;
    .env/bin/pip install -U pip
    .env/bin/pip install -r requirements.txt
    .env/bin/python -m grpc.tools.protoc -I=bubbles/protobuf --python_out=bubbles/protobuf bubbles.proto
}


main "$@"
