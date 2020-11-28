#!/bin/sh

if [[ -f /app_from_host/entry.sh ]]; then
    echo "Running code from local mount"
    cd /app_from_host
else
    echo "Running code from image"
    cd /app
fi

env >> /etc/environment
python initialize.py \
&& exec uvicorn main:app --host=0.0.0.0 --port=5000

