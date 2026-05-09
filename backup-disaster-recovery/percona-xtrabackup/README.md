## Overview
dokumentasikan strategi backup dan pemulihan bencana (Disaster Recovery) untuk database produksi, dengan fokus utama pada penggunaan Percona XtraBackup untuk sinkronisasi data antar data center.

## Features
- Full & Incremental Backup: Menggunakan XtraBackup
- Point-in-Time Recovery (PITR): Memanfaatkan binlog untuk pemulihan data yang presisi.
- Automated Sync (DR to DRC): Arsitektur pengiriman data otomatis antar server melalui jalur aman.
- Migration & Replication: Prosedur inisiasi replikasi Slave tanpa downtime.

## Disaster Recovery Architecture
Skenario ini mendemonstrasikan perpindahan data dari server DR ke DRC:
- Source Server (DR)    10.204.20.134    Master Database (Production)
- Target Server (DRC)   10.205.30.134    Slave Database (Recovery Center)

## Implementation Steps
   Menjalankan hot backup menggunakan container Docker untuk menjaga isolasi lingkungan:
```[cite: 2]
### 1. Database Backup (Source MySQL DR)
docker run --name xtrabackup --volumes-from MySQL-DR-Prod -v /root/xtrabackup:/backup percona/percona-xtrabackup:2.4 /bin/bash -c "xtrabackup --backup --data-dir=/var/lib/mysql --target-dir=/backup --user=user_mysql --password=password_mysql && xtrabackup --prepare --data-dir=/var/lib/mysql --target-dir=/backup --user=mysql_user --password=password_mysql"

### 2. Data Synchronization
Mengirimkan hasil backup ke server DRC menggunakan `rsync` untuk efisiensi bandwidth:
rsync -avz --delete /root/xtrabackup root@10.205.30.134:/root/

### 3. Restoration & Replication Setup (Target DRC)
Setelah data diterima, lakukan inisiasi replikasi berdasarkan posisi binlog yang tercatat di `xtrabackup_binlog_info`:
- Stop container MySQL DRC
docker stop MySQL-DRC-Prod
- Backup volume MySQL DRC sebelumnya
mv /var/lib/docker/volumes/mysql-drc-prod /var/lib/docker/volumes/mysql-drc-prod.bak
- Pindahkan xtrabackup ke volumes MySQL DRC dan ganti owner nya
mv /root/xtrabackup /root/mysql-drc-prod
mv /root/mysql-drc-prod /var/lib/docker/volumes/
chown -R 1001:1001 /var/lib/docker/volumes/mysql-drc-prod
- Start container MySQL DRC
docker start MySQL-DRC-Prod

```sql
CHANGE MASTER TO
  MASTER_HOST='10.204.20.134',
  MASTER_LOG_FILE='[file_from_info]',
  MASTER_LOG_POS=[pos_from_info];
START SLAVE;
SHOW SLAVE STATUS\G
**Architecture Diagram** sederhana atau tabel navigasi agar pengunjung bisa langsung melihat keahlian Anda di berbagai ekosistem database sekaligus.
