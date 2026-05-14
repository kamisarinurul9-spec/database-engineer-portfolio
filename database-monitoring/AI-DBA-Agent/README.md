# AI Database Agent with LangChain, LangGraph & Llama 3.3

![Database Engineering](https://img.shields.io/badge/Focus-Database%20Engineering-blue)
![Percona](https://img.shields.io/badge/DB-Percona%20MySQL-orange)
![Python](https://img.shields.io/badge/Language-Python-yellow)

## Deskripsi
**AI-DBA-Agent** adalah asisten cerdas berbasis AI yang dirancang untuk mengelola dan memantau infrastruktur database MySQL (Master-Slave) secara otomatis. Menggunakan **LangGraph** untuk alur kerja (workflow) dan **Llama 3.1 (via Groq)** sebagai otak analisisnya, agen ini mampu memahami perintah bahasa alami untuk melakukan tugas administrasi database dan analisis data secara real-time.

dijalankan di atas lingkungan **Docker** untuk memastikan portabilitas dan konsistensi environment.

## 🛠 Struktur Proyek

```
ai-dba-agent/
│
├── app.py              # Logika utama (LangGraph Workflow, Router, & Nodes)
├── requirements.txt    # Daftar dependensi Python
├── .env                # Konfigurasi environment (IP, User, Password, API Key)
├── Dockerfile          # Instruksi build container
└── logs/               # Direktori untuk file log (opsional)
```
## Fitur Utama
Sistem ini terbagi menjadi beberapa peran spesifik (Nodes) untuk memastikan akurasi data:
- Audit Skema: Menampilkan daftar tabel secara real-time.
- User Audit: Memeriksa daftar user database dan hak akses (privileges) yang mereka miliki.
- Data Retrieval: Mengambil record data terbaru dari tabel.
- AI Summary: Memberikan ringkasan cerdas (maksimal 5 kalimat) mengenai isi data, mendeteksi pola, atau anomali menggunakan LLM.
- Replication Monitor: Mengecek status replikasi (Slave IO/SQL) dan seconds behind master.
- Performance Tracking: Deteksi Slow Query (> 3 detik) dan audit user online (processlist).
- AI Optimization: Memberikan rekomendasi teknis untuk optimasi database.

## Run Via Docker 
- Build Image
`docker build -t ai-dba-agent .`
- Run Container
`docker run -it --env-file .env ai-dba-agent`
