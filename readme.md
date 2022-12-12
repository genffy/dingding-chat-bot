# dingding chat bot
## Install 
```
pip install -r requirements.txt
```

## Start
### nohup
```
nohup python server.py >> logs/app.log &
```

### docker
#### docker start
```shell
docker run -p 8080:8080 dingding-chat-bot
```

#### docker build
```shell
docker build -t dingding-chat-bot .
```