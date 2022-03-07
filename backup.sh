#!/bin/bash

curl -G --data-urlencode "query=BACKUP database;" \
  http://localhost:9000/exec

echo "[Console] backup questdb database"
