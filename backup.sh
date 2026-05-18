#!/bin/bash
BACKUP_DIR="/var/www/hash-identifier/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup PostgreSQL
sudo -u postgres pg_dump hashdb > $BACKUP_DIR/hashdb_$TIMESTAMP.sql

# Backup environment files
cp /var/www/hash-identifier/backend/.env $BACKUP_DIR/env_$TIMESTAMP.bak 2>/dev/null

# Compress backups
tar -czf $BACKUP_DIR/backup_$TIMESTAMP.tar.gz -C $BACKUP_DIR *.sql *.bak 2>/dev/null

# Remove old backups (keep 7 days)
find $BACKUP_DIR -name "backup_*.tar.gz" -mtime +7 -delete

echo "Backup completed: backup_$TIMESTAMP.tar.gz"
