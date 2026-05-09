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
- Dashboard PMM: Buka [http://10.204.20.137], login pertama kali dengan admin / admin. Anda akan diminta mengganti password.
<img width="1292" height="950" alt="Screenshot 2026-05-09 174528" src="https://github.com/user-attachments/assets/a2257a7b-803e-43ce-93f7-c2ea09e516c9" />
Dengan setup ini, kita bisa melihat visualisasi Replication Lag antara node 135 dan 136 secara real-time di dashboard PMM.
<img width="1919" height="1025" alt="Screenshot 2026-05-09 182631" src="https://github.com/user-attachments/assets/cc81c391-699a-48e7-a810-2ec5f26042fe" />


