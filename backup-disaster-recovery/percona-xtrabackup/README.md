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
### 1. Database Backup (Source DR)
### 2. Data Synchronization
Mengirimkan hasil backup ke server DRC menggunakan `rsync` untuk efisiensi bandwidth:
```bash
rsync -avz --delete /opt/mysql-dr-sync/data/current_backup/ root@10.205.30.134:/opt/mysql-dr-sync/data/current_backup/

### 3. Restoration & Replication Setup (Target DRC)
Setelah data diterima, dilakukan proses *prepare* dan inisiasi replikasi berdasarkan posisi binlog yang tercatat di `xtrabackup_binlog_info`:
```sql
CHANGE MASTER TO
  MASTER_HOST='10.204.20.134',
  MASTER_LOG_FILE='[file_from_info]',
  MASTER_LOG_POS=[pos_from_info];
START SLAVE;
```[cite: 2]

## Tools
*   **mysqldump / xtrabackup**[cite: 2]
*   **cron jobs** for automation[cite: 2]
*   **rsync** for secure data transport[cite: 2]
*   **TiDB Data Migration / CDC**[cite: 2]

## Results
*   **RPO (Recovery Point Objective):** Mendekati nol dengan bantuan replikasi berkelanjutan[cite: 2].
*   **RTO (Recovery Time Objective):** Pemulihan cepat melalui metode `copy-back` XtraBackup[cite: 2].
*   **Zero Downtime:** Proses backup tidak mengunci tabel produksi[cite: 1, 2].

## Lessons Learned
*   **Backup tanpa uji restorasi = Useless.** Selalu lakukan verifikasi `--prepare` secara berkala[cite: 2].
*   **Automasi adalah kunci.** Mengurangi risiko *human error* dalam prosedur DR yang kritis[cite: 2].

---

### Tips untuk Profil GitHub Anda:
Karena Anda memiliki banyak folder folder cluster (TiDB, ClickHouse, MongoDB), ada baiknya di `README.md` utama (root) Anda menambahkan **Architecture Diagram** sederhana atau tabel navigasi agar pengunjung bisa langsung melihat keahlian Anda di berbagai ekosistem database sekaligus.
