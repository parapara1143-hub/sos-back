#!/usr/bin/env bash
set -e
DATE=$(date +%Y%m%d_%H%M%S)
PGURL=${DATABASE_URL:-"postgresql://sos:sos@localhost:5432/sosdb"}
pg_dump "$PGURL" > "backup_${DATE}.sql"
echo "Backup gerado: backup_${DATE}.sql"
