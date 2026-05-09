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
