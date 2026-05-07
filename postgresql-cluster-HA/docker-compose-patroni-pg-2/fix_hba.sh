#!/bin/bash
# Menghapus baris reject dan menambah trust setiap kali kontainer mulai
sed -i '/hostnossl all.*all.*reject/d' /home/postgres/pgdata/pgroot/data/pg_hba.conf
if ! grep -q 'host all all 0.0.0.0/0 trust' /home/postgres/pgdata/pgroot/data/pg_hba.conf; then
    sed -i '1ihost all all 0.0.0.0/0 trust' /home/postgres/pgdata/pgroot/data/pg_hba.conf
fi
