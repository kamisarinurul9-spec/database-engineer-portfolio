## Migrasi MySQL ke TiDB
### Menggunakan tools  TiDB Data Migration (DM)
TiDB Data Migration (DM) adalah alat manajemen migrasi data terintegrasi yang dirancang khusus untuk mereplikasi data dari database yang kompatibel dengan MySQL (seperti MySQL, MariaDB, dan Percona Server) ke dalam TiDB
## Komponen Utama TiDB DM 
- DM-master: Otak dari DM. yang mengelola seluruh topologi cluster DM, menyimpan informasi tugas migrasi, dan memantau status replikasi.
- DM-worker: Unit pelaksana. yang berinteraksi langsung dengan database sumber (MySQL) untuk membaca log (binlog) dan menuliskannya ke TiDB. Satu worker biasanya menangani satu instansi database sumber.
- dmctl: Alat baris perintah (CLI) yang  digunakan untuk mengontrol cluster DM, seperti memulai, menghentikan, atau mengecek status migrasi.
## Struktur replikasi dan migrasi (mysql ke TiDB) 
<img width="386" height="444" alt="Screenshot 2026-05-05 212827" src="https://github.com/user-attachments/assets/65182770-7fc3-4c15-a646-e9415abef9d6" />

## Step Implementasi
- syarat khusus di MySQL harus wajib aktif server-id, binlog dan binlog_format
- buat user migrasi di MySQL <br />
  `CREATE USER 'dm_tidb'@'%' IDENTIFIED BY 'Sup4rd1^17';` <br />
  `GRANT ALL PRIVILEGES ON . TO 'dm_tidb'@'%';` <br />
  `FLUSH PRIVILEGES;` <br />
## Buat  TiDB DM di  (VM 10.204.20.150) 
<img width="1502" height="159" alt="Screenshot 2026-05-05 214127" src="https://github.com/user-attachments/assets/782c6566-6e25-40f9-b5f3-b01a8137818e" />
Verifikasi koneksi antar komponen <br />
`docker exec -it dm-master /dmctl --master-addr 10.204.20.150:8261 list-member` <br />
<img width="877" height="803" alt="Screenshot 2026-05-05 214649" src="https://github.com/user-attachments/assets/bb9ad5fe-e287-46dc-b15c-06aa90ec4042" />

