#!/bin/sh
set -eu
test -x bin/foundation-smoke-service
bin/foundation-smoke-service --check
curl --fail --silent --show-error http://127.0.0.1:8080/health >/dev/null
curl --fail --silent --show-error http://127.0.0.1:9090/-/ready >/dev/null
curl --fail --silent --show-error http://127.0.0.1:3000/api/health >/dev/null
