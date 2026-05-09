## setup pmm server
- run docker compose pmm-server <br />
`docker compose up -d`
## Setup Client di Node Database
- MySQL Master (10.204.20.135): <br />
`docker run -d \
  --name pmm-client-master \
  --restart always \
  -e PMM_AGENT_SERVER_ADDRESS=10.204.20.137 \
  -e PMM_AGENT_SERVER_USERNAME=admin \
  -e PMM_AGENT_SERVER_PASSWORD=admin \
  -e PMM_AGENT_SERVER_INSECURE_TLS=1 \
  -e PMM_AGENT_SETUP=1 \
  -e PMM_AGENT_CONFIG_FILE=/usr/local/percona/pmm2/config/pmm-agent.yaml \
  percona/pmm-client:2`
- MySQL Slave (10.204.20.136) <br />
`docker run -d \
  --name pmm-client-slave \
  --restart always \
  -e PMM_AGENT_SERVER_ADDRESS=10.204.20.137 \
  -e PMM_AGENT_SERVER_USERNAME=admin \
  -e PMM_AGENT_SERVER_PASSWORD=admin \
  -e PMM_AGENT_SERVER_INSECURE_TLS=1 \
  -e PMM_AGENT_SETUP=1 \
  -e PMM_AGENT_CONFIG_FILE=/usr/local/percona/pmm2/config/pmm-agent.yaml \
  percona/pmm-client:2`
## Daftarkan MySQL ke PMM Server
- Setelah container client menyala, jalankan perintah ini (sekali saja) di tiap VM untuk mendaftarkan layanan MySQL-nya.
- MySQL Master <br />
`docker exec -it pmm-client-master pmm-admin add mysql \
  --username=root \
  --password=PASSWORD_MYSQL_MASTER \
  --host=10.204.20.135 \
  --port=3306 \
  --query-source=perfschema \
  MySQL-Master-Node`
- MySQL Slave <br />
`docker exec -it pmm-client-slave pmm-admin add mysql \
  --username=root \
  --password=PASSWORD_MYSQL_SLAVE \
  --host=10.204.20.136 \
  --port=3306 \
  --query-source=perfschema \
  MySQL-Slave-Node`
## Keamanan & Verifikasi
- Dashboard PMM: Buka [http://10.204.20.137], login pertama kali dengan admin / admin. Anda akan diminta mengganti password. <br />
<img width="1292" height="950" alt="Screenshot 2026-05-09 174528" src="https://github.com/user-attachments/assets/a2257a7b-803e-43ce-93f7-c2ea09e516c9" />
Dengan setup ini, kita bisa melihat visualisasi Replication Lag antara node 135 dan 136 secara real-time di dashboard PMM. <br />
<img width="1919" height="1025" alt="Screenshot 2026-05-09 182631" src="https://github.com/user-attachments/assets/cc81c391-699a-48e7-a810-2ec5f26042fe" />
sistem sudah berhasil membaca infrastruktur dengan baik. berikut analisa kondisi nya <br />
- Monitored DB Instances: Sudah terbaca 2 MySQL dan 1 PostgreSQL. Ini sesuai dengan setup Master-Slave Anda dan node Patroni. <br />
- Database Query/s (QPS): Tercatat di angka 16.08. Ini menunjukkan traffic database Anda sedang aktif namun masih sangat ringan untuk resource yang ada. <br />
- Database Connection: Ada 10 koneksi aktif. Angka ini normal untuk setup yang menggunakan Connection Pooler <br />
- Disk Space Total: Kapasitas 88.75 GiB terdeteksi, ini adalah total kapasitas disk dari node yang terpasang PMM Client. <br />

<img width="1911" height="957" alt="Screenshot 2026-05-09 183535" src="https://github.com/user-attachments/assets/01a64723-88f3-4cb7-bb33-3f74b5d371ae" />

Analisis Ringkasan Query <br />
- Total QPS (Queries Per Second): Saat ini berada di angka 1.09 QPS. Ini adalah traffic yang sangat rendah, menunjukkan database sedang dalam kondisi idle atau hanya menjalankan query background/monitoring. (dikarenakan database nya masih kosongan)
- Query Time: Rata-rata waktu eksekusi berada di 713.68 μs (mikrodetik). Ini sangat cepat karena mayoritas query yang terlihat adalah query sistem. <br />

<img width="1919" height="973" alt="Screenshot 2026-05-09 184657" src="https://github.com/user-attachments/assets/55eae8fb-1258-486a-8a43-82d3d4a4087f" />

MySQL Replication Summary
- IO Thread Running: Yes (Artinya, Slave berhasil terhubung ke Master dan sedang mendengarkan perubahan data (binlog) secara real-time.)
- SQL Thread Running: Yes (Artinya, Slave berhasil mengeksekusi perintah-perintah yang dikirim dari Master ke database lokalnya.)
- Read Only: Yes  (Artinya Node Slave dalam mode Read Only, mencegah adanya perubahan data yang tidak sengaja dilakukan langsung di Slave yang bisa merusak konsistensi replikasi) <br />
Metrik Performa
- MySQL Replication Lag: 0s (Garis datar pada grafik menunjukkan tidak ada keterlambatan. Data yang ditulis di Master (135) langsung muncul di Slave (136) dalam waktu kurang dari satu detik.)
- Replication Error No: No Data (Artinya Tidak ada error yang terdeteksi. Jika replikasi putus karena masalah jaringan atau data duplikat, kode error akan muncul di sini)





