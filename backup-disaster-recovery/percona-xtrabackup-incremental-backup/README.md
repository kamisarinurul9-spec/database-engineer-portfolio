## Incremental Backup
membuat cadangan (backup) harian dan incremental di MySQL dari DC to DRC
menggunakan Percona XtraBackup dan fitur bawaan Binary Logs.

## Strategi Backup Harian (Incremental)
Arsitektur Automasi
1. Server DR: Menjalankan script backup yang mendeteksi hari. Jika hari Minggu, lakukan Full Backup. Jika Senin-Sabtu, lakukan Incremental Backup merujuk pada hari sebelumnya.
2. Transfer: Menggunakan rsync untuk mengirim folder backup ke DRC segera setelah proses backup selesai.
3. Server DRC: Standby menerima data. Proses prepare dan restore bisa dilakukan secara manual atau otomatis saat dibutuhkan
