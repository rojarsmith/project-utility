# PostgreSQL

## Install

Support PostgreSQL 18.x, Ubuntu 24.04

```bash
# noble (24.04, LTS)
sudo apt install -y curl
sudo install -d /usr/share/postgresql-common/pgdg
sudo curl -o /usr/share/postgresql-common/pgdg/apt.postgresql.org.asc --fail https://www.postgresql.org/media/keys/ACCC4CF8.asc

. /etc/os-release
sudo sh -c "echo 'deb [signed-by=/usr/share/postgresql-common/pgdg/apt.postgresql.org.asc] https://apt.postgresql.org/pub/repos/apt $VERSION_CODENAME-pgdg main' > /etc/apt/sources.list.d/pgdg.list"

sudo apt update
sudo apt install postgresql-18

tail /var/log/postgresql/postgresql-18-main.log
```

## Remote Access

Full control:

```bash
sudo -u postgres psql
sudo -u postgres psql -c "SHOW config_file;"

sudo vi /etc/postgresql/18/main/postgresql.conf

listen_addresses = '*'
port = 5432

sudo -u postgres psql -c "SHOW hba_file;"
sudo vi /etc/postgresql/18/main/pg_hba.conf

host    all             all             192.168.0.0/16         md5

systemctl status postgresql

sudo -i -u postgres
psql

CREATE ROLE dbeaver_admin WITH LOGIN PASSWORD 'Passw@rd' SUPERUSER CREATEDB CREATEROLE REPLICATION BYPASSRLS;

psql -h localhost -U dbeaver_admin -d postgres
```

### Oracle Cloud

1. VCN

Networking -> Virtual cloud networks -> VCN -> Add Ingress Rules

Destination Port Range 5432

2. IP Table

```bash
sudo iptables -L -n -v
sudo apt-get install iptables-persistent
sudo iptables -I INPUT 5 -p tcp --dport 5432 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
```

## SSL

```markdown
Certbot renew
       ↓
Deploy-hook trigger
       ↓
systemctl reload postgresql
       ↓
PostgreSQL use new CA without pause
```

psql A 10800 132.226.123.125 Disable Proxy

Cloudflare

Create Custom Token
Zone DNS Edit
Include All zones

```bash
sudo apt install certbot letsencrypt python3-certbot-dns-cloudflare
mkdir ~/.secrets
vi ~/.secrets/cloudflare.ini

dns_cloudflare_api_token = <API_TOKEN>

chmod 0700 ~/.secrets/
chmod 0400 ~/.secrets/cloudflare.ini

sudo certbot certonly \
--dns-cloudflare \
--dns-cloudflare-credentials ~/.secrets/cloudflare.ini \
-d domain.com \
--preferred-challenges dns-01 \
--dns-cloudflare-propagation-seconds 60 \
--email user@gmail.com

FC_CA="/etc/letsencrypt/live/$(ls /etc/letsencrypt/live | grep -v README | head -n 1)/fullchain.pem"
PV_KE="/etc/letsencrypt/live/$(ls /etc/letsencrypt/live | grep -v README | head -n 1)/fullchain.pem"

sudo vi /etc/postgresql/18/main/postgresql.conf

ssl = on
ssl_cert_file = '/etc/letsencrypt/live/db.example.com/fullchain.pem'
ssl_key_file = '/etc/letsencrypt/live/db.example.com/privkey.pem'
ssl_prefer_server_ciphers = on
ssl_ciphers = 'HIGH:MEDIUM:+3DES:!aNULL'

sudo chown postgres:postgres /etc/letsencrypt/live/db.example.com/privkey.pem
sudo chmod 600 /etc/letsencrypt/live/db.example.com/privkey.pem

sudo chown postgres:postgres $FC_CA
sudo chmod 600 $FC_CA
sudo namei -l /etc/letsencrypt/live/psql.neuhex.com/fullchain.pem f: /etc/letsencrypt/live/psql.neuhex.com/fullchain.pem
sudo -u postgres cat /etc/letsencrypt/live/psql.neuhex.com/fullchain.pem
sudo -u postgres cat "$FC_CA" > /dev/null
sudo chown postgres:postgres /etc/letsencrypt/archive

sudo vi /etc/letsencrypt/renewal-hooks/deploy/reload-postgresql.sh

#!/bin/bash
# When certbot renews the certificate, reload PostgreSQL (no downtime)
/usr/bin/systemctl reload postgresql

sudo chmod +x /etc/letsencrypt/renewal-hooks/deploy/reload-postgresql.sh

sudo certbot renew --dry-run
sudo certbot renew --dry-run -v

# Dry run: skipping deploy hook command: /etc/letsencrypt/renewal-hooks/deploy/reload-postgresql.sh

# DBeaver using SSL: Driver properties -> sslmode: require

SHOW ssl;
SHOW ssl_cert_file;
SHOW ssl_key_file;
```

