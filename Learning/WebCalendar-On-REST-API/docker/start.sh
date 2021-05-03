#!/bin/bash
app="webcldapi.test"
docker build -t ${app} .
docker run -d -p 80:80 \
  --name=${app} \
  -v $PWD:/www ${app}