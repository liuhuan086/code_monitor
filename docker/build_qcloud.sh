#!/usr/bin/env bash
docker login xxx.tencentyun.com/redarmy/yyy -u xxx -p xxx
docker build -t xxx.tencentyun.com/redarmy/yyy:prd ../
docker push xxx.tencentyun.com/redarmy/yyy:prd

docker build -f ../DockerfileCelery -t xxx.tencentyun.com/redarmy/yyy-celery:prd ../
docker push xxx.tencentyun.com/redarmy/yyy-celery:prd
