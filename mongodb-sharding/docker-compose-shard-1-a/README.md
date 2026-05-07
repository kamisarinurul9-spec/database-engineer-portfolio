## Deploy 
- docker compose up -d

## Add member
- rs.initiate({_id:"mongo-shard-1", members:[{_id:0,host:"gcp-ev2mgo1a-p2:27201"},{_id:1,host:"gcp-ev2mgo1b-p2:27201"}]})

## Cek Status
- rs.status()
