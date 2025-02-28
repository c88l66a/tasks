#!/bin/bash

chown 999:999 postgresql.conf && chmod 770 postgresql.conf
mkdir -p ./pglog && chown 999:999 -R ./pglog && chmod 755 -R ./pglog
docker compose up -d
