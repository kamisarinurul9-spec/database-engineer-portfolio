## Deploy
- docker-compose up -d

## Cek Distribus Query Rule
docker exec -it proxysql-service mysql -u admin -padmin -h 127.0.0.1 -P 6032 --prompt='ProxySQLAdmin> '
## Cek DB Backend (Master & SLave)
- SELECT hostgroup_id, hostname, port, status, weight  FROM mysql_servers;
## Cek Rule Query
- SELECT rule_id, active, match_digest, destination_hostgroup, apply  FROM mysql_query_rules;
