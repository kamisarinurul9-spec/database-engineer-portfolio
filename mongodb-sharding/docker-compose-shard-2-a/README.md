## Deploy 
- docker compose up -d

## Add member
- rs.initiate({_id:"mongo-shard-2", members:[{_id:0,host:"gcp-ev2mgo2a-p2:27201"},{_id:1,host:"gcp-ev2mgo2b-p2:27201"}]})

## Cek Status
- rs.status()
