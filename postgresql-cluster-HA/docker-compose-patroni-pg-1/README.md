## Deploy
- chmod +x fix_hba.sh
- docker compose up -d

## Cek Status,  Role & Topologi Cluster
- docker exec -it patroni_pg_131 patronictl -c /run/postgres.yml list

## Cek Konektivitas via PgBouncer 
- docker exec -it patroni_pg_131 psql -h 10.204.20.134 -p 6432 -U postgres postgres #SESUAIKAN IP & AUTH

## Validasi Load Balancing
- SELECT * FROM pg_stat_replication
