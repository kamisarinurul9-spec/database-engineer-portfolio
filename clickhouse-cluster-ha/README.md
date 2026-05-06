# ClickHouse Cluster High Availability

## Overview
This project demonstrates a distributed ClickHouse cluster for high-performance analytical queries.

## Architecture
- Multiple shards
- Replicated nodes
- Distributed tables

## Features
- High availability cluster
- Distributed query execution
- Fast OLAP queries

## Tech Stack
- ClickHouse Server
- ClickHouse Keeper
- ClickHouse Proxy
- Docker

## Implementation
- Created cluster with shards & replicas
- Configured distributed tables
- Optimized analytical queries

## Results
- Query time reduced from seconds to milliseconds
- Scalable analytical system

## Lessons Learned
- Columnar storage improves performance
- Distributed architecture is key for big data

## Deployment Guide: TiDB Distributed Cluster via Docker Compose
- docker compose up -d
- SELECT * FROM system.clusters;
- CREATE DATABASE db_test ON CLUSTER cluster_1S_2R
