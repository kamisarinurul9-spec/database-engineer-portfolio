## Overview
dokumentasikan strategi backup dan pemulihan bencana (Disaster Recovery) untuk database produksi, dengan fokus utama pada penggunaan Percona XtraBackup untuk sinkronisasi data antar data center.

## Features
- Full & Incremental Backup: Menggunakan XtraBackup
- Point-in-Time Recovery (PITR): Memanfaatkan binlog untuk pemulihan data yang presisi.
- Automated Sync (DR to DRC): Arsitektur pengiriman data otomatis antar server melalui jalur aman.
- Migration & Replication: Prosedur inisiasi replikasi Slave tanpa downtime.
