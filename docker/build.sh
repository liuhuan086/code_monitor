#!/usr/bin/env bash
docker login harbor.xxx.com -u xxx -p xxx
docker build -t harbor.xxx.com/prd/yyy:1.0.0 ../
docker push harbor.xxx.com/prd/yyy:1.0.0


