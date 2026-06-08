# Keycloak

## Quick Command

```bash
podman run -d -p 127.0.0.1:8050:8080 -e KC_BOOTSTRAP_ADMIN_USERNAME=admin -e KC_BOOTSTRAP_ADMIN_PASSWORD=admin --name keycloak quay.io/keycloak/keycloak:26.5.0 start-dev
```

## Install

Production

- Switch to a production ready database such as PostgreSQL.
- Configure SSL with your own certificates.
- Switch the admin password to a more secure password.

```bash
# Add 80, 8080, 443
sudo apt install openjdk-21-jdk
sudo apt install zip
sudo mkdir -p /opt/keycloak
cd /opt/keycloak
sudo wget https://github.com/keycloak/keycloak/releases/download/26.5.0/keycloak-26.5.0.zip
sudo unzip keycloak-26.5.0.zip -d /opt/keycloak
sudo rm keycloak-26.5.0.zip

cd /opt/keycloak/keycloak-26.5.0

# Do again after update
sudo iptables -I INPUT 5 -p tcp --dport 80 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
sudo iptables -I INPUT 5 -p tcp --dport 443 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
sudo iptables -I INPUT 5 -p tcp --dport 8080 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
sudo iptables -I INPUT 5 -p tcp --dport 8443 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
sudo netfilter-persistent save

sudo vi /opt/keycloak/keycloak-26.5.0/conf/keycloak.conf

db=postgres
db-username=keycloak
db-password=POSTGRESSQL_DATABASE_PASSWORD
db-url=jdbc:postgresql://domain.com/keycloak
https-certificate-file=/etc/letsencrypt/live/keycloak.mydomain.com/fullchain.pem
https-certificate-key-file=/etc/letsencrypt/live/keycloak.mydomain.com/privkey.pem
https-port=8443
hostname=keycloak.mydomain.com

cd /opt/keycloak/keycloak-26.5.0
sudo bin/kc.sh build
sudo -E bin/kc.sh bootstrap-admin user
sudo -E bin/kc.sh start

https://domain.com:8443/admin/master/console/

sudo vi /etc/systemd/system/keycloak.service

# /etc/systemd/system/keycloak.service
[Unit]
Description=Keycloak Server
After=syslog.target network.target mysql.service
Before=httpd.service

[Service]
User=keycloak
Group=keycloak
SuccessExitStatus=0 143
ExecStart=!/opt/keycloak/keycloak-26.5.0/bin/kc.sh start

[Install]
WantedBy=multi-user.target

sudo systemctl daemon-reload
sudo systemctl enable keycloak
sudo shutdown -r now
sudo systemctl status keycloak
```

## DB

```sql
CREATE USER keycloak WITH PASSWORD 'Passw@rd';

CREATE DATABASE keycloak
    WITH
    OWNER = keycloak
    ENCODING = 'UTF8';

GRANT ALL PRIVILEGES ON DATABASE keycloak TO keycloak;
```

## SSL

```bash
sudo apt-get install certbot
# Oracle Cloud
sudo iptables -I INPUT 5 -p tcp --dport 80 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT

DOMAIN=domain.com
EMAIL=gmail.com

sudo certbot certonly --standalone --preferred-challenges http -d $DOMAIN --email $EMAIL --dry-run
sudo certbot certonly --standalone --preferred-challenges http -d $DOMAIN --email $EMAIL

FC_CA=/etc/letsencrypt/live/domain.com/fullchain.pem
PRV_KEY=/etc/letsencrypt/live/domain.com/privkey.pem

sudo systemctl list-units --type timer
sudo systemctl enable certbot.timer

cd /etc/letsencrypt/renewal-hooks/pre
sudo vi pre-hook.sh
```

## Account Console

http://localhost:8050/realms/myrealm/account



