# TestRLT


## Dependencies

Для запуска по инструкции потребуется Docker, python



## Setup




## Start



```shell
docker run --name mongo -d -e MONGO_INITDB_ROOT_USERNAME=mongo -e MONGO_INITDB_ROOT_PASSWORD=mongo -p 27017:27017 mongo:latest
docker cp ./dump mongo:/data/dump
docker exec -it mongo mongorestore -u mongo -p mongo --authenticationDatabase admin -d sample /data/dump
```

```shell
docker run -d --name mongo-express -e ME_CONFIG_MONGODB_ADMINUSERNAME=mongo -e ME_CONFIG_MONGODB_ADMINPASSWORD=mongo -e ME_CONFIG_MONGODB_SERVER=mongo --link mongo:mongo -p 8081:8081 mongo-express:latest
```

`
mongodb://mongo:mongo@localhost:27017
`