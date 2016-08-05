#!/bin/bash
set -e
# input: tcp_addr, tcp_port
wait_tcp_dependency()
{
    local tcp_addr=$1;
    local tcp_port=$2;
    local testing_url="tcp://${tcp_addr}:${tcp_port}"

    # assign fd automatically
    # refer to http://stackoverflow.com/questions/8295908/how-to-use-a-variable-to-indicate-a-file-descriptor-in-bash
    while ! exec {id}<>/dev/tcp/${tcp_addr}/${tcp_port}; do
        echo "$(date) - trying to connect to ${testing_url}"
        sleep 1
    done
}

echo "connecting to redis ..."
wait_tcp_dependency ${REDIS_HOST} ${REDIS_PORT} 

echo "runing site ..."
/usr/local/bin/gunicorn --access-logfile=/logs/gunicorn.access.log  --error-logfile=/logs/gunicorn.error.log -w4 -b0.0.0.0:9000 webapp:app 

