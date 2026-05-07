## Deploy 
- docker compose up -d

## Add Shard
- sh.addShard("mongo-shard-1/gcp-ev2mgo1a-p2:27201,gcp-ev2mgo1b-p2:27201")
- sh.addShard("mongo-shard-2/gcp-ev2mgo2a-p2:27201,gcp-ev2mgo2b-p2:27201")

## Cek Status
- sh.status()
