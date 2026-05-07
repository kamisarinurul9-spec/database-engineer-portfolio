# MongoDB Sharding Cluster

## Overview
This project demonstrates horizontal scaling using MongoDB sharding.

## Architecture
- Config Server
- Shards
- Mongos Router

## Features
- Data partitioning
- Horizontal scaling
- High throughput system

## Tech Stack
- Percona MongoDB
- Docker

## Results
- Improved write scalability
- Balanced data distribution

## Lessons Learned
- Sharding key selection is critical
- Enables horizontal scaling

## Add key & copy file all environment
- openssl rand --base64 756 > key.file
- chown -R 1001:1001 key.file
- chmod 400 key.file
