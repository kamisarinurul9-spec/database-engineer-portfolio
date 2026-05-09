## Migrasi MySQL ke TiDB
### Menggunakan tools  TiDB Data Migration (DM)
TiDB Data Migration (DM) adalah alat manajemen migrasi data terintegrasi yang dirancang khusus untuk mereplikasi data dari database yang kompatibel dengan MySQL (seperti MySQL, MariaDB, dan Percona Server) ke dalam TiDB
## Komponen Utama TiDB DM 
- DM-master: Otak dari DM. yang mengelola seluruh topologi cluster DM, menyimpan informasi tugas migrasi, dan memantau status replikasi.
- DM-worker: Unit pelaksana. yang berinteraksi langsung dengan database sumber (MySQL) untuk membaca log (binlog) dan menuliskannya ke TiDB. Satu worker biasanya menangani satu instansi database sumber.
- dmctl: Alat baris perintah (CLI) yang  digunakan untuk mengontrol cluster DM, seperti memulai, menghentikan, atau mengecek status migrasi.
## Struktur replikasi dan migrasi (mysql ke TiDB) 
`[ Source DB MySQL ] >> [ DM-Worker (extract & sync) ] >> [ DM-Master (Control Plane) ] >> [ TiDB (Target DB) ]`
## Step Implementasi
- syarat khusus di MySQL harus wajib aktif server-id, binlog dan binlog_format
- nuat user migrasi di MySQL <br \>
  `CREATE USER 'dm_tidb'@'%' IDENTIFIED BY 'Sup4rd1^17';` <br \>
  `GRANT ALL PRIVILEGES ON . TO 'dm_tidb'@'%';`
  `FLUSH PRIVILEGES;`
   
