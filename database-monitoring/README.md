# Database Monitoring Stack

Repository ini berisi konfigurasi sistem monitoring database terpusat yang dirancang untuk mengelola lingkungan database skala besar dan terdistribusi. Fokus utama dari proyek ini adalah memberikan visibilitas penuh terhadap performa, keamanan, dan kesehatan cluster database.

## Fitur Utama
* **Multi-Engine Monitoring**: Dukungan penuh untuk pemantauan Percona MySQL, MongoDB, ClickHouse, dan PostgreSQL.
* **PMM Integration**: Implementasi **Percona Monitoring and Management (PMM)** untuk analisis query mendalam (Query Analytics) dan metrik sistem secara real-time.
* **Distributed Systems Support**: Monitoring khusus untuk ketersediaan tinggi pada TiDB Cluster dan MongoDB Sharding.
* **Infrastructure Metrics**: Melacak utilisasi resource (CPU, Memory, Disk I/O) pada lingkungan Ubuntu 22.04 LTS.

## Tech Stack & Tools
* **Monitoring Platforms**: 
    * **PMM (Percona Monitoring and Management)**: Digunakan untuk visualisasi performa MySQL dan MongoDB.
    * **Prometheus & Grafana**: Digunakan untuk monitoring kustom pada sistem terdistribusi (TiDB/ClickHouse).
    * **CheckMK**: Digunakan untuk monitoring kesehatan sistem, mengidentifikasi kemacetan (bottleneck), serta memberikan peringatan dini (alerting) untuk mencegah kegagalan sistem.
* **Database Supported**: 
    * Percona MySQL, MongoDB, ClickHouse, PostgreSQL, TiDB.
* **Infrastructure**: 
    * OS: Linux.
    * Containerization: Docker & Docker Compose.

## Struktur Repositori
```text
database-monitoring/
├── pmm-client/          # Konfigurasi PMM Client & Client Deployment scripts
├── grafana-dashboards/  # Template JSON untuk dashboard kustom
├── prometheus-configs/  # Scrape configurations & alerting rules
├── checkmk-agent/       # mengumpulkan data pemantauan terperinci secara aktif dari host (server/perangkat) untuk dikirim ke server Checkmk
└── exporters/           # Dockerized exporters (Node, MySQL, MongoDB exporters)
