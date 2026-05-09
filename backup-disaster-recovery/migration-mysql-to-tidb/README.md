## Migrasi MySQL ke TiDB
### Menggunakan tools  TiDB Data Migration (DM)
TiDB Data Migration (DM) adalah alat manajemen migrasi data terintegrasi yang dirancang khusus untuk mereplikasi data dari database yang kompatibel dengan MySQL (seperti MySQL, MariaDB, dan Percona Server) ke dalam TiDB
## Komponen Utama TiDB DM 
- DM-master: Otak dari DM. yang mengelola seluruh topologi cluster DM, menyimpan informasi tugas migrasi, dan memantau status replikasi.
- DM-worker: Unit pelaksana. yang berinteraksi langsung dengan database sumber (MySQL) untuk membaca log (binlog) dan menuliskannya ke TiDB. Satu worker biasanya menangani satu instansi database sumber.
- dmctl: Alat baris perintah (CLI) yang  digunakan untuk mengontrol cluster DM, seperti memulai, menghentikan, atau mengecek status migrasi.
## Struktur replikasi dan migrasi (mysql ke TiDB) 
`[ Source DB MySQL ] >> [ DM-Worker (extract & sync) ] >> [ DM-Master (Control Plane) ] >> [ TiDB (Target DB) ]`
