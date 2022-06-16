#!/bin/bash
#wget https://github.com/compose/transporter/releases/download/v0.5.2/transporter-0.5.2-linux-amd64
#sudo mv transporter-*-linux-amd64 /usr/local/bin/transporter
#chmod +x /usr/local/bin/transporter
# curl -XDELETE 'http://localhost:9200/_all'
export MONGODB_URI='mongodb://localhost/car'
export ELASTICSEARCH_URI='http://localhost:9200/car_elastic'
# transporter run pipeline.js
