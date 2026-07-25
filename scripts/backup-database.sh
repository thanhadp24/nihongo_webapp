#!/usr/bin/env bash
set -euo pipefail

TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
mkdir -p backups
docker compose exec -T mysql mysqldump -uroot -p"${MYSQL_ROOT_PASSWORD:-root_password}" "${MYSQL_DATABASE:-nihongo_webapp}" | gzip > "backups/nihongo_webapp_${TIMESTAMP}.sql.gz"

