# MySQL Master-Slave Replication

## Overview
Implementasi replikasi MySQL untuk high availability dan read scaling.

## Architecture
Master → Slave

## Setup

### Master
- Enable binlog
- Server-id = 1

### Slave
- Server-id = 2
- CHANGE MASTER TO ...

## Replication Flow
1. Write ke master
2. Binlog dikirim ke slave
3. Slave apply relay log

## Failure Handling
- Promote slave menjadi master
- Reconfigure replication

## Testing
- Insert data di master
- Verifikasi di slave

## 📁 Script
Lihat folder `/scripts`
