## Overview
dokumentasikan strategi backup dan pemulihan bencana (Disaster Recovery) untuk database produksi, dengan fokus utama pada penggunaan Percona XtraBackup untuk sinkronisasi data antar data center.

## Features
- Full & Incremental Backup: Menggunakan XtraBackup
- Point-in-Time Recovery (PITR): Memanfaatkan binlog untuk pemulihan data yang presisi.
- Automated Sync (DR to DRC): Arsitektur pengiriman data otomatis antar server melalui jalur aman.
- Migration & Replication: Prosedur inisiasi replikasi Slave tanpa downtime.

## Disaster Recovery Architecture
Skenario ini mendemonstrasikan perpindahan data dari server DR ke DRC:
"Source Server (DR)    10.204.20.134    Master Database (Production)"
"Target Server (DRC)   10.205.30.134    Slave Database (Recovery Center)"

## Implementation Steps
1. Database Backup (Source DR)
