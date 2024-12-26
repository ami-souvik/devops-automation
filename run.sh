#!/bin/bash

docker compose down --rmi all --volumes --remove-orphans
sudo docker compose up --build
