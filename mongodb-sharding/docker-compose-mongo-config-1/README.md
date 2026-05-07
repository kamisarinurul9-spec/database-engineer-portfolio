## Deploy 
- docker compose up -d

## Add member
- rs.initiate({_id:"mongo-master-config", configsvr:true, members: [{_id:0,host:"gcp-ev2mgo1b-p2:27101"},{_id:1,host:"gcp-ev2mgo1b-p2:27101"}]})

## Cek Status
- rs.status()
