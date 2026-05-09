## Incremental Backup
membuat cadangan (backup) harian dan incremental di MySQL dari DC to DRC
menggunakan Percona XtraBackup dan fitur bawaan Binary Logs.

## Strategi Backup Harian (Incremental)
Arsitektur Automasi
1. Server DR: Menjalankan script backup yang mendeteksi hari. Jika hari Minggu, lakukan Full Backup. Jika Senin-Sabtu, lakukan Incremental Backup merujuk pada hari sebelumnya.
2. Transfer: Menggunakan rsync untuk mengirim folder backup ke DRC segera setelah proses backup selesai.
3. Server DRC: Standby menerima data. Proses prepare dan restore bisa dilakukan secara manual atau otomatis saat dibutuhkan
supaya script bisa mengirim data secara otomatis, pastikan server DR bisa masuk ke DRC tanpa password:
## Di server DR (10.204.20.130)
- ssh-keygen -t rsa
- ssh-copy-id root@10.205.30.130
### 2. Skrip Automasi Backup (`backup-automation.sh`)
Buat file ini di `/opt/scripts/backup-automation.sh` pada server DR:

```bash
#!/bin/bash

# Konfigurasi
BACKUP_DIR="/root/xtrabackup"
REMOTE_DRC="10.205.30.130"
USER="spenew"
PASS="spenew2018"
DAY=$(date +%a | tr '[:upper:]' '[:lower:]') # mon, tue, wed...
DATE=$(date +%F)

# 1. Tentukan jenis backup
if [ "$DAY" == "sun" ]; then
    TARGET="$BACKUP_DIR/full"
    # Hapus backup lama setiap minggu agar storage tidak penuh
    rm -rf $BACKUP_DIR/full/* $BACKUP_DIR/inc/*
    
    echo "Running Full Backup..."
    docker run --rm --volumes-from MySQL-DR-Prod \
      -v $BACKUP_DIR/full:/backup percona/percona-xtrabackup:2.4 \
      xtrabackup --backup --target-dir=/backup --user=$USER --password=$PASS
else
    # Tentukan basis incremental (jika senin base=full, jika selasa base=mon)
    if [ "$DAY" == "mon" ]; then BASE="$BACKUP_DIR/full"; else 
        PREV_DAY=$(date -d "yesterday" +%a | tr '[:upper:]' '[:lower:]')
        BASE="$BACKUP_DIR/inc/$PREV_DAY"
    fi
    
    TARGET="$BACKUP_DIR/inc/$DAY"
    mkdir -p $TARGET

    echo "Running Incremental Backup for $DAY..."
    docker run --rm --volumes-from MySQL-DR-Prod \
      -v $BACKUP_DIR:/backup percona/percona-xtrabackup:2.4 \
      xtrabackup --backup --target-dir=/backup/inc/$DAY --incremental-basedir=$BASE --user=$USER --password=$PASS
fi

# 2. Sinkronisasi ke DRC
echo "Syncing to DRC..."
rsync -avz --delete $BACKUP_DIR/ root@$REMOTE_DRC:$BACKUP_DIR/

