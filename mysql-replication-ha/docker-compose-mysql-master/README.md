## Deploy
- docker-compose up -d

## Create User Replicated
- CREATE USER 'replication'@'%' IDENTIFIED WITH mysql_native_password BY 'r3pl1C4t0R_1';
- GRANT REPLICATION SLAVE ON *.* TO 'replication'@'%';
- FLUSH PRIVILEGES;
