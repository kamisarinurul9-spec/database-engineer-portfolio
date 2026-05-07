# PostgreSQL High Availability Cluster with Patroni & Consul

## Overview
Proyek ini mengimplementasikan arsitektur database PostgreSQL yang memiliki ketahanan tinggi (High Availability) menggunakan **Patroni** sebagai template manajemen cluster dan **Consul** sebagai Distributed Configuration Store (DCS). Arsitektur ini menjamin *zero downtime* dan *automatic failover* untuk kebutuhan aplikasi kritis.

## Architecture
Desain ini menggunakan topologi tiga node PostgreSQL dengan mekanisme *streaming replication*:
- **Leader Node**: Menangani trafik baca dan tulis (Read/Write).
- **Replica Nodes**: Sinkronisasi data secara real-time dan siap mengambil alih peran Leader jika terjadi kegagalan.
- **Gateway Node**: Menggunakan **HAProxy** dan **PgBouncer** untuk manajemen koneksi dan routing trafik otomatis ke node yang sehat.

# Features
- **Automatic Failover**: Transisi otomatis peran Leader dalam hitungan detik tanpa intervensi manual.
- **Connection Pooling**: Efisiensi penggunaan resource database menggunakan PgBouncer.
- **DCS Integration**: Konsistensi konfigurasi cluster yang disimpan secara terdistribusi di Consul.
- **Custom Security Policy**: Konfigurasi `pg_hba.conf` yang diatur secara permanen melalui Patroni configuration untuk akses internal yang aman dan cepat.

## Tech Stack
- **Database**: PostgreSQL 16 (Spilo image by Zalando)
- **Cluster Manager**: Patroni
- **Service Discovery/DCS**: Consul
- **Load Balancer**: HAProxy
- **Connection Pooler**: PgBouncer
- **Environment**: Docker & Docker Compose

## Implementation
1.  **Orchestration**: Deploy cluster menggunakan Docker Compose dengan volume persistent untuk keamanan data.
2.  **Config Injection**: Mengintegrasikan aturan `pg_hba` langsung ke dalam variabel environment `PATRONI_CONFIGURATION` untuk memastikan persistensi setting setelah container restart.
3.  **Health Check**: Implementasi REST API Patroni untuk membantu HAProxy menentukan node Master/Leader secara akurat.
4.  **Verification**: Melakukan pengujian failover dan verifikasi replikasi melalui `pg_stat_replication`.

## Results
- **Seamless Failover**: Sistem tetap dapat diakses meskipun salah satu node database dimatikan secara mendadak.
- **High Efficiency**: Manajemen koneksi yang lebih baik, mencegah error `too many clients` pada aplikasi.
- **Synchronized Data**: Replikasi antar node berjalan dengan *zero lag* (0 MB lag).

## Lessons Learned
- **DCS-Driven Configuration**: Konfigurasi via Patroni/Consul jauh lebih handal dibandingkan mengedit file `.conf` secara manual di dalam container.
- **Layered Infrastructure**: Memisahkan load balancer (HAProxy) dari database meningkatkan skalabilitas sistem secara keseluruhan.
