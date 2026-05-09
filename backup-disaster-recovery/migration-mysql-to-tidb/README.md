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

Hasil list-member menunjukkan bahwa infrastruktur TiDB Data Migration (DM) sudah berjalan dengan sempurna. <br />
- Master (master1): Sudah aktif sebagai Leader di IP 10.204.20.150:8261.
- Worker (worker1): Sudah terdaftar dengan status "stage": "free". Ini berarti Worker siap menerima tugas namun belum dihubungkan ke sumber database manapun. <br />
langkah selanjutnya untuk memulai migrasi dari MySQL Source DB DeVA (10.204.20.134) ke TiDB (10.204.20.131). <br />
1. Daftarkan source MySQL (Source DB DeVA) dan Buat file bernama source.yaml di dm-master 
  <img width="687" height="309" alt="Screenshot 2026-05-05 215917" src="https://github.com/user-attachments/assets/22384030-e622-40da-ab1f-ef65f2762320" />
  
Run untuk mendaftarkan source <br />
`docker exec -it dm-master /dmctl --master-addr 10.204.20.150:8261 operate-source create source.yaml`

<img width="1182" height="315" alt="Screenshot 2026-05-05 220736" src="https://github.com/user-attachments/assets/ed74741e-ea65-440b-9c4e-5fed013820bd" />
source berhasil dibuat!, Output tersebut menunjukkan bahwa TiDB Data Manager (DM) sudah berhasil mendaftarkan sumber data MySQL Anda dengan ID mysql-production dan sudah diikat (bound) ke worker1. <br />

2. Buat Task Migrasi (Full + Incremental) Buat file bernama task.yaml. File ini menentukan apa yang akan dipindah dan ke mana tujuannya. <br />
<img width="628" height="800" alt="Screenshot 2026-05-05 222001" src="https://github.com/user-attachments/assets/0e43c2ee-de92-45ad-baa7-d001223d92b6" />

Jalankan task <br />
`docker exec -it dm-master /dmctl --master-addr 10.204.20.150:8261 start-task task.yaml `
<img width="1588" height="792" alt="Screenshot 2026-05-05 222932" src="https://github.com/user-attachments/assets/efe2eda6-28a0-4cf7-9caa-3f732cd119fc" />

<img width="1901" height="867" alt="Screenshot 2026-05-05 223119" src="https://github.com/user-attachments/assets/72902ca8-2265-4521-b803-8a026fc5d9eb" />

- Hasilnya ada memang banyak Warning (peringatan). tapi jangan khawatir, pesan tersebut hanyalah Warning, bukan Error yang menghentikan proses. Status ringkasan disini menunjukkan "passed": true 

- Penyebab utamanya adalah TiDB secara default menerima (parse) sintaks FOREIGN KEY dari MySQL agar tidak error saat pembuatan tabel, tetapi tidak memberlakukan (ignore) batasan integritasnya secara ketat seperti MySQL tradisional. 

Mengapa Ini Terjadi? 
- TiDB adalah database terdistribusi. Memberlakukan Foreign Key lintas node (TiKV) secara ketat akan memberikan dampak performa yang sangat besar pada operasi tulis. Karena itu, TiDB menyarankan pengecekan integritas data dilakukan di level aplikasi. 

3. Monitoring Proses Migrasi <br />
Ini bagian paling krusialnya. Gunakan perintah ini untuk melihat progress-nya. <br />
`docker exec -it dm-master /dmctl --master-addr 10.204.20.150:8261 query-status migrasi_utama_mysql`
<img width="1202" height="796" alt="Screenshot 2026-05-05 230803" src="https://github.com/user-attachments/assets/51215c94-73c7-4687-a32a-a40566cdcde3" />

<img width="832" height="332" alt="Screenshot 2026-05-05 230910" src="https://github.com/user-attachments/assets/85a36dfa-7c8c-48c5-be59-c25633000362" />

Berdasarkan hasil query-status tersebut, berikut adalah poin-poin penting yang menandakan keberhasilan replikasi <br />
Analisis Status Replikasi : <br />
- Stage: Running & Unit: Sync: Proses full dump dan load data awal telah selesai 100%. Sekarang DM sedang berada dalam fase replikasi binlog secara real-time.
- Synced: true: Ini adalah indikator paling krusial. Artinya, data di Cluster TiDB (10.204.20.131) saat ini sudah sama persis dengan data di MySQL DeVA sumber (VM 10.204.20.134).
- SecondsBehindMaster: 0: Tidak ada jeda (lag) waktu antara sumber dan target. Setiap ada perubahan data di MySQL, TiDB akan langsung terupdate dalam hitungan milidetik.
- Master vs Syncer Binlog: Keduanya berada di posisi yang sama (mysql-bin.000004, 30236305). Ini mengonfirmasi bahwa tidak ada data yang tertinggal di antrean.
4. Verifikasi Data di TiDB <br />
masuk ke database TiDB  di VM 10.204.20.131 dan jalankan pengecekan cepat untuk memastikan database dan tabel sudah muncul: <br />
`MySQL -u root -p -h 10.204.20.131 -P 4000` <br /> 
`SHOW DATABASES;` <br />
`USE deva_switcher_prod;` <br />
`SHOW TABLES;` <br />
`SELECT COUNT(*) FROM deva_client;` <br />
<img width="1510" height="801" alt="Screenshot 2026-05-05 232054" src="https://github.com/user-attachments/assets/2ec8c91e-8d92-4395-92ce-19d0c4d8698e" />

<img width="425" height="806" alt="Screenshot 2026-05-05 232155" src="https://github.com/user-attachments/assets/d4d6f00a-2765-492c-8dbb-778ab29674ed" />  

<img width="350" height="376" alt="Screenshot 2026-05-05 232218" src="https://github.com/user-attachments/assets/38c187e3-5740-48bb-bed9-907a5c51885d" />  








  
