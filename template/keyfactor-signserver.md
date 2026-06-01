# Keyfactor Signserver

Pass: Ubuntu 24.04

## Install Docker

```bash
sudo apt remove docker docker-engine docker.io containerd runc -y
sudo apt update && sudo apt upgrade -y
sudo apt install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo tee /etc/apt/keyrings/docker.asc > /dev/null

sudo chmod a+r /etc/apt/keyrings/docker.asc

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

sudo systemctl start docker
sudo systemctl enable docker

sudo docker run hello-world

## No need to type sudo

sudo usermod -aG docker $USER
newgrp docker
docker ps
docker compose version

## Change storage

sudo systemctl stop docker
sudo mv /var/lib/docker /mnt/data/docker
sudo ln -s /mnt/data/docker /var/lib/docker
sudo systemctl start docker
```

## Deploy Signserver

```bash
mkdir -p signserver/{backups,secrets}
cd signserver

# DB password
openssl rand -base64 32 > secrets/db_root_password.txt
openssl rand -base64 32 > secrets/db_password.txt
chmod 600 secrets/*.txt

# Generate ManagementCA key and self-signed credentials
openssl req -newkey rsa:4096 \
  -keyout secrets/ManagementCA.key -x509 -days 3650 \
  -out secrets/ManagementCA.crt -nodes \
  -subj "/CN=ManagementCA/O=SignServer/C=TW"

# Generate admin key and CSR
openssl req -newkey rsa:4096 -keyout secrets/admin.key \
  -out secrets/admin.csr -nodes \
  -subj "/CN=admin/O=SignServer/C=TW"

# Issue admin credentials using ManagementCA
openssl x509 -req -in secrets/admin.csr -CA secrets/ManagementCA.crt \
  -CAkey secrets/ManagementCA.key \
  -CAcreateserial -out secrets/admin.crt -days 3650

# Package into p12 and import into the browser, then restart the browser
openssl pkcs12 -export -in secrets/admin.crt -inkey secrets/admin.key \
  -certfile secrets/ManagementCA.crt \
  -out secrets/admin.p12 -passout pass:admin123

# Confirm that admin.crt was signed by ManagementCA.
openssl verify -CAfile secrets/ManagementCA.crt secrets/admin.crt

# Confirm the credentials content in admin.p12
openssl pkcs12 -in secrets/admin.p12 -nokeys -passin pass:admin123 | openssl x509 -noout -subject -issuer

# Confirm the subject of ManagementCA.crt
openssl x509 -in secrets/ManagementCA.crt -noout -subject -issuer

# Quickly check and verify the identity and serial number
openssl x509 -in ./secrets/admin.crt -noout -serial -issuer
serial=5B7D34303331AE2F46D056D1928CF547508B2100
issuer=CN = ManagementCA, O = SignServer, C = TW

## Deploy using Docker Compose

# SignServer docker container not support DATABASE_PASSWORD_FILE
touch .env
echo "DB_PASSWORD=$(cat ./secrets/db_password.txt | tr -d '\r\n')" > .env

touch docker-compose.yml
vi docker-compose.yml
```

`docker-compose.yml`

```yaml
services:
  db:
    image: mariadb:10.11
    container_name: signserver-db
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD_FILE: /run/secrets/db_root_password
      MYSQL_DATABASE: signserver
      MYSQL_USER: signserver
      MYSQL_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_root_password
      - db_password
    volumes:
      - db_data:/var/lib/mysql
    networks:
      - signserver-net
    healthcheck:
      test: ["CMD", "healthcheck.sh", "--connect", "--innodb_initialized"]
      interval: 10s
      timeout: 5s
      retries: 5

  signserver:
    image: keyfactor/signserver-ce:latest
    container_name: signserver
    restart: unless-stopped
    depends_on:
      db:
        condition: service_healthy
    ports:
      - "19080:8080"
      - "19443:8443"
    environment:
      DATABASE_JDBC_URL: jdbc:mariadb://db:3306/signserver
      DATABASE_USER: signserver
      DATABASE_PASSWORD: ${DB_PASSWORD}
      SIGNSERVER_NODEID: node1
    volumes:
      - signserver_data:/opt/signserver/res/signserver
      - signserver_config:/opt/signserver/conf
      - ./secrets/ManagementCA.crt:/mnt/external/secrets/tls/cas/ManagementCA.crt
    networks:
      - signserver-net

# Automatic processing of TLS CA login for Administration Web authentication
  signserver-init:
      image: alpine:latest
      container_name: signserver-init
      restart: "no"
      volumes:
        - ./secrets:/mnt/certs:ro
        - ./init-admin.sh:/init-admin.sh:ro
        - /run/docker.sock:/var/run/docker.sock
      networks:
        - signserver-net
      entrypoint:
        - sh
        - -c
        - |
          apk update && \
          apk add --no-cache curl openssl docker-cli bash && \
          exec sh /init-admin.sh

volumes:
  db_data:
  signserver_data:
  signserver_config:

secrets:
  db_root_password:
    file: ./secrets/db_root_password.txt
  db_password:
    file: ./secrets/db_password.txt

networks:
  signserver-net:
    driver: bridge

```

```bash
touch init-admin.sh
vi init-admin.sh
```

`init-admin.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "==> Waiting for SignServer to fully start..."
until curl -sk https://signserver:8443/signserver/healthcheck/signserverhealth | grep -q "ALLOK"; do
  echo "    Waiting..."
  sleep 10
done
echo "==> SignServer is ready"

echo "==> Reading admin.crt information..."
SERIAL=$(openssl x509 -in /mnt/certs/admin.crt -noout -serial | cut -d= -f2 | tr '[:upper:]' '[:lower:]')
ISSUER_RAW=$(openssl x509 -in /mnt/certs/admin.crt -noout -issuer | sed 's/issuer=//')

# Replace "CN = ManagementCA, O = SignServer, C = TW" to "C=TW, O=SignServer, CN=ManagementCA"
# Remove spaces first, then reverse the order
ISSUER=$(echo "$ISSUER_RAW" | \
  sed 's/ = /=/g' | \
  awk -F', ' '{for(i=NF;i>0;i--) printf "%s%s",$i,(i>1?", ":"")}')

echo "    Serial: $SERIAL"
echo "    Issuer: $ISSUER"

echo "==> Set wsadmins / wsauditors / wsarchiveauditors..."
docker exec signserver /opt/signserver/bin/signserver wsadmins -add -certserialno "$SERIAL" -issuerdn "$ISSUER" 2>/dev/null || true
docker exec signserver /opt/signserver/bin/signserver wsauditors -add -certserialno "$SERIAL" -issuerdn "$ISSUER" 2>/dev/null || true
docker exec signserver /opt/signserver/bin/signserver wsarchiveauditors -add -certserialno "$SERIAL" -issuerdn "$ISSUER" 2>/dev/null || true

echo "==> Complete! Current authorization list:"
docker exec signserver /opt/signserver/bin/signserver wsadmins -list

echo "==> Changing httpserver.external.privhttps in the signserver container to 19443..."

# Using the Linux sed command to precisely match "httpserver.external.privhttps = 443" and replace it
docker exec signserver sed -i 's/httpserver.external.privhttps\s*=\s*443/httpserver.external.privhttps = 19443/g' /opt/signserver/conf/signserver_deploy.properties

echo "==> Restarting Jboss to apply changes..."
# The container must be restarted for SignServer to reread this configuration file.
docker exec signserver $APPSRV_HOME/bin/jboss-cli.sh --connect --command=":reload"


docker exec -it signserver bash
grep -n "https-listener"  /opt/keyfactor/wildfly-35.0.1.Final/standalone/configuration/standalone.xml
571:                <https-listener name="https" socket-binding="https" max-post-size="33554432" allow-encoded-slash="true" ssl-context="httpsSSC" enable-http2="false"/>

docker exec -it signserver sed -i '571s|enable-http2="false"/>|enable-http2="false" certificate-forwarding="true" proxy-address-forwarding="true"/>|' /opt/keyfactor/wildfly-35.0.1.Final/standalone/configuration/standalone.xml

docker exec -it signserver sed -n '571p' /opt/keyfactor/wildfly-35.0.1.Final/standalone/configuration/standalone.xml
```

```bash
docker compose up -d
```

Browser:

https://localhost:19443/signserver

https://localhost:19443/signserver/adminweb/

## Startup

```bash
cat << 'EOF' | sudo tee /etc/systemd/system/signserver-docker.service > /dev/null
[Unit]
Description=SignServer Docker Compose Application Service
Requires=docker.service
After=docker.service network-online.target

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/root/signserver
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable signserver-docker.service
sudo systemctl start signserver-docker.service
sudo systemctl status signserver-docker.service
```

## Reverse Proxy

```bash
sudo vi /etc/nginx/sites-available/signserver.nginx
```

`/etc/nginx/sites-available/signserver.nginx`

```nginx
server {
    listen 80;
    server_name signserver.bitdove.net;

    location ^~ /.well-known/acme-challenge/ {
        root /var/www/letsencrypt;
        allow all;
        default_type "text/plain";
        try_files $uri =404;
    }

    location = / {
        return 301 /signserver/;
    }

    location /signserver/ {
        proxy_pass http://127.0.0.1:19080/signserver/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    server_name signserver.bitdove.net;

    ssl_certificate /etc/letsencrypt/live/signserver.bitdove.net/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/signserver.bitdove.net/privkey.pem;

    ssl_client_certificate /root/signserver/secrets/ManagementCA.crt;
    ssl_verify_client optional_no_ca;
    ssl_verify_depth 2;

    location /test-cert {
        return 200 "verify=$ssl_client_verify cert=$ssl_client_escaped_cert";
        add_header Content-Type text/plain;
    }

    location /signserver/adminweb/ {
        return 301 https://139.162.197.165:19443/signserver/adminweb/;
    }

    location = / {
        return 301 /signserver/;
    }

    location /signserver/ {
        proxy_pass https://127.0.0.1:19443/signserver/;

        proxy_ssl_verify off;
        proxy_ssl_session_reuse on;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_set_header SSL_CLIENT_CERT $ssl_client_escaped_cert;
        proxy_set_header SSL_CLIENT_S_DN $ssl_client_s_dn;
        proxy_set_header SSL_CLIENT_I_DN $ssl_client_i_dn;
        proxy_set_header SSL_CLIENT_VERIFY $ssl_client_verify;
    }

    listen 443 ssl http2;
}

```

```bash
# Enable the configuration and reload Nginx

sudo ln -s /etc/nginx/sites-available/signserver /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

sudo certbot \
    certonly \
    --webroot \
    --webroot-path /var/www/letsencrypt \
    --agree-tos \
    --email service@bitdove.net \
    -d signserver.bitdove.net
```

## Demo

### Signing and Verification

```bash
### Config CryptoTokenP12 (1) ACTIVE > CMSSigner (2) ACTIVE

## Server

docker exec signserver /opt/keyfactor/signserver/bin/signserver setproperties /opt/keyfactor/signserver/doc/sample-configs/keystore-crypto.properties

docker exec signserver /opt/keyfactor/signserver/bin/signserver setproperty 1 KEYSTOREPASSWORD foo123

docker exec signserver /opt/keyfactor/signserver/bin/signserver reload 1

docker exec signserver /opt/keyfactor/signserver/bin/signserver setproperties /opt/keyfactor/signserver/doc/sample-configs/cmssigner.properties

## Client

curl -o img1.svg "https://signserver.bitdove.net/signserver/jakarta.faces.resource/images/logo.svg.xhtml?ln=community"

curl -k -X POST \
    -H "Content-Type: application/octet-stream" \
    --data-binary @./img1.svg \
    "https://signserver.bitdove.net/signserver/process?workerName=CMSSigner" \
    -o ./img1.svg.p7m

openssl cms -verify -inform DER -in ./img1.svg.p7m -noverify > /dev/null

openssl cms -verify -inform DER -in ./img1.svg.p7m -noverify -out ./restored_img1.svg

## Corrupting img1.svg.p7m and Failing Verification

cp ./img1.svg.p7m ./corrupted_img1.svg.p7m

printf "\x00\x00\x00\x00" | dd of=./corrupted_img1.svg.p7m bs=1 count=4 conv=notrunc 2>/dev/null

openssl cms -verify -inform DER -in ./corrupted_img1.svg.p7m -noverify > /dev/null

echo "Verification Exit Code (Expected non-zero): $?"

openssl cms -verify -inform DER -in ./corrupted_img1.svg.p7m -noverify -out ./failed_restored_img1.svg
```

### IoT Firmware Detached Signing

```bash
### Server, environment inheritance in the previous demo

## It is important to note that any data manipulation may affect whether the verification passes.

docker exec signserver sed -i 's/DETACHEDSIGNATURE=FALSE/DETACHEDSIGNATURE=TRUE/g' /opt/keyfactor/signserver/doc/sample-configs/cmssigner.properties

docker exec signserver /opt/keyfactor/signserver/bin/signserver setproperty 2 DETACHEDSIGNATURE TRUE

docker exec signserver /opt/keyfactor/signserver/bin/signserver reload 2

zip update.zip img1.svg

curl -k -X POST \
    -H "Content-Type: application/octet-stream" \
    --data-binary @./update.zip \
    "https://signserver.bitdove.net/signserver/process?workerName=CMSSigner" \
    -o ./update.zip.p7s

export DEVICE_ID="IOT_8899"
mkdir -p ./$DEVICE_ID/secure_storage

docker cp signserver:/opt/keyfactor/signserver/res/test/dss10/dss10_keystore.p12 ./$DEVICE_ID/secure_storage/

openssl pkcs12 -in ./$DEVICE_ID/secure_storage/dss10_keystore.p12 -clcerts -nokeys -passin pass:foo123 -out ./$DEVICE_ID/secure_storage/root_verify.pem -legacy

openssl pkcs12 -in ./$DEVICE_ID/secure_storage/dss10_keystore.p12 -nokeys -passin pass:foo123 -out ./$DEVICE_ID/secure_storage/root_verify.pem -legacy

openssl x509 -in ./$DEVICE_ID/secure_storage/root_verify.pem -text -noout

openssl cms -verify -binary -inform DER \
  -in ./update.zip.p7s \
  -content ./update.zip \
  -certfile ./$DEVICE_ID/secure_storage/root_verify.pem \
  -noverify \
  -out /dev/null

## Client

# Download update.zip.p7s, IOT_8899

export DEVICE_ID="IOT_8899"
cp ./update.zip ./update.zip.p7s ./$DEVICE_ID/
pushd ./$DEVICE_ID/

# Perform decoupled verification (-content specifies the original compressed archive to be signed)
openssl cms -verify -binary -inform DER \
-in ./update.zip.p7s \
-content ./update.zip \
-certfile ./$DEVICE_ID/secure_storage/root_verify.pem \
-noverify \
-out /dev/null

cp img1.svg hacked_img1.svg
echo "<svg>MALICIOUS_CODE_HERE</svg>" > img1.svg
zip -u update.zip img1.svg
```

## Maintenance

```bash
# ============================================================
# 1. Docker service lifecycle
# ============================================================

docker compose ps
docker compose up -d --force-recreate

docker compose logs -f signserver
docker compose logs -f signserver-init

docker logs signserver 2>&1 | grep "ERROR"
docker logs signserver-db | grep -i "denied"

docker compose down
docker compose down -v


# ============================================================
# 2. Enter SignServer container
# ============================================================

docker exec -it signserver bash
cd /opt/signserver

docker exec signserver /opt/keyfactor/signserver/bin/signserver getstatus complete all
docker exec signserver /opt/keyfactor/signserver/bin/signserver getstatus brief 1


# ============================================================
# 3. Health check
# ============================================================

curl -sk https://localhost/signserver/healthcheck/signserverhealth && echo ""

curl -sk https://signserver.bitdove.net/signserver/healthcheck/signserverhealth

curl -sk \
  --cert-type P12 \
  --cert ~/admin.p12:admin123 \
  https://signserver.bitdove.net/signserver/healthcheck/signserverhealth

curl -sk \
  --cert-type P12 \
  --cert ~/admin.p12:admin123 \
  https://139.162.197.165:19443/signserver/rest/v1/workers


# ============================================================
# 4. Web admin credentials
# ============================================================

openssl pkcs12 -in secrets/admin.p12 \
  -nokeys \
  -passin pass:admin123 \
| openssl x509 -noout -serial

docker exec -it signserver bash

/opt/signserver/bin/signserver wsadmins -add \
  -certserialno 5B7D34303331AE2F46D056D1928CF547508B2100 \
  -issuerdn "CN=ManagementCA, O=SignServer, C=TW"

/opt/signserver/bin/signserver wsadmins -add \
  -cert /mnt/external/secrets/tls/cas/ManagementCA.crt

/opt/signserver/bin/signserver wsadmins -list

docker exec -it signserver /opt/signserver/bin/signserver wsadmins -list

bin/signserver wsadmins -remove \
  -certserialno 5b7d34303331ae2f46d056d1928cf547508b2100 \
  -issuerdn "CN=ManagementCA, O=SignServer, C=TW"


# ============================================================
# 5. Database checks
# ============================================================

docker exec signserver-db cat /run/secrets/db_root_password
docker exec signserver-db cat /run/secrets/db_password

cat ./secrets/db_root_password.txt
cat ./secrets/db_password.txt

docker exec signserver env | grep DATABASE_PASSWORD

docker exec -it signserver timeout 3 bash -c '</dev/tcp/db/3306' \
  && echo "Network connection successful" \
  || echo "Network connection failed"

docker exec -it signserver-db \
  mysql -u signserver -p"$(cat ./secrets/db_password.txt)" \
  -e "SHOW DATABASES;"

docker exec -it signserver-db \
  mysql -u root -p"$(cat ./secrets/db_root_password.txt)" \
  -e "SELECT user, host FROM mysql.user; SHOW GRANTS FOR 'signserver'@'%';"

docker exec -i signserver-db \
  mysql -u root -p"$(cat ./secrets/db_root_password.txt)" <<EOF
DROP USER IF EXISTS 'signserver'@'%';
CREATE USER 'signserver'@'%' IDENTIFIED BY '${DB_PASS}';
GRANT ALL PRIVILEGES ON signserver.* TO 'signserver'@'%';
FLUSH PRIVILEGES;
SHOW GRANTS FOR 'signserver'@'%';
EOF


# ============================================================
# 6. Locate sample configs and keystores
# ============================================================

docker exec signserver find / -name "*r.properties*" 2>/dev/null

# Common result:
# /opt/keyfactor/signserver/doc/sample-configs/cmssigner.properties

docker exec signserver find / -name "*.p12*" 2>/dev/null

# Common result:
# /opt/keyfactor/signserver/res/test/dss10/dss10_keystore.p12


# ============================================================
# 7. Import sample SignServer properties
# ============================================================

docker exec signserver \
  /opt/keyfactor/signserver/bin/signserver setproperties \
  /opt/keyfactor/signserver/doc/sample-configs/cmssigner.properties

docker exec signserver \
  /opt/keyfactor/signserver/bin/signserver setproperties \
  doc/sample-configs/keystore-crypto.properties


# ============================================================
# 8. Configure existing dss10 keystore worker
# ============================================================

docker exec signserver \
  /opt/keyfactor/signserver/bin/signserver setproperty 1 KEYSTOREPATH \
  /opt/keyfactor/signserver/res/test/dss10/dss10_keystore.p12

docker exec signserver \
  /opt/keyfactor/signserver/bin/signserver setproperty 1 KEYSTOREPASSWORD foo123

docker exec signserver \
  /opt/keyfactor/signserver/bin/signserver setproperty 1 DEFAULTKEY "ts00003"

docker exec signserver \
  /opt/keyfactor/signserver/bin/signserver setproperty 1 PIN foo123

docker exec signserver \
  /opt/keyfactor/signserver/bin/signserver reload 1

docker exec signserver \
  /opt/keyfactor/signserver/bin/signserver activatecryptotoken 1 foo123

docker exec signserver \
  /opt/keyfactor/signserver/bin/signserver getstatus brief 1


# ============================================================
# 9. Create CryptoToken and CMSSigner manually
# ============================================================

docker exec -it signserver bash
cd /opt/signserver

bin/signserver setproperty CryptoTokenP12 KEYSTOREPATH /opt/signserver/res/signserver/demo-token.p12
bin/signserver setproperty CryptoTokenP12 KEYSTORETYPE PKCS12
bin/signserver setproperty CryptoTokenP12 KEYSTOREPASSWORD foo123
bin/signserver setproperty CryptoTokenP12 IMPLEMENTATION_CLASS org.signserver.server.cryptotokens.P12CryptoToken
bin/signserver reload CryptoTokenP12

bin/signserver generatekey CryptoTokenP12 \
  -alias signkey001 \
  -keyalg RSA \
  -keyspec 2048

bin/signserver setproperty CMSSigner IMPLEMENTATION_CLASS org.signserver.module.cmssigner.CMSSigner
bin/signserver setproperty CMSSigner TYPE PROCESSABLE
bin/signserver setproperty CMSSigner CRYPTOTOKEN CryptoTokenP12
bin/signserver setproperty CMSSigner DEFAULTKEY signkey001
bin/signserver setproperty CMSSigner AUTHTYPE NOAUTH
bin/signserver reload CMSSigner


# ============================================================
# 10. Create CMSSigner worker by properties
# ============================================================

docker exec -i signserver sh -c "cat > /tmp/cms.properties && /opt/keyfactor/signserver/bin/signserver setproperties /tmp/cms.properties" << 'EOF'
WORKER2.TYPE=PROCESSABLE
WORKER2.IMPLEMENTATION_CLASS=org.signserver.module.cmssigner.CMSSigner
WORKER2.NAME=CMSSigner
WORKER2.AUTHTYPE=NOAUTH
WORKER2.CRYPTOTOKEN=CryptoTokenP12
WORKER2.DEFAULTKEY=signer00001
WORKER2.DETACHEDSIGNATURE=FALSE
WORKER2.DISABLEKEYUSAGECOUNTER=true
WORKER2.ACCEPTANYPOLICY=true
WORKER2.ACCEPTED_HASH_DIGEST_ALGORITHMS=SHA-256,SHA-384,SHA-512
EOF

docker exec signserver \
  /opt/keyfactor/signserver/bin/signserver uploadsignercertificate 2 signer00001

docker exec signserver \
  /opt/keyfactor/signserver/bin/signserver reload 2


# ============================================================
# 11. Sign files with CMSSigner
# ============================================================

curl -k -X POST \
  -H "Content-Type: application/octet-stream" \
  --data-binary @/home/srv/service/signserver/a1.jpeg \
  "https://localhost/signserver/process?workerName=CMSSigner" \
  -o ~/service/signserver/a1.jpeg.p7m

curl -k -X POST \
  -H "Content-Type: application/octet-stream" \
  --data-binary @/home/srv/service/signserver/update.zip \
  "https://localhost/signserver/process?workerName=CMSSigner" \
  -o ~/service/signserver/update.zip.p7m


# ============================================================
# 12. Verify CMS signatures with OpenSSL
# ============================================================

openssl cms -verify \
  -inform DER \
  -in ~/service/signserver/a1.jpeg.p7m \
  -noverify \
  -out ~/service/signserver/out.jpeg

openssl cms -verify \
  -inform DER \
  -in ~/service/signserver/a1.jpeg.p7m \
  -noverify \
  > /dev/null

openssl cms -verify \
  -inform DER \
  -in ~/service/signserver/a1.jpeg.p7m \
  -noverify \
  -signer /tmp/signer_info.pem

openssl x509 -in /tmp/signer_info.pem -text -noout

openssl cms -verify \
  -binary \
  -inform DER \
  -in ./update.zip.p7s \
  -content ./update.zip \
  -certfile ./$DEVICE_ID/secure_storage/root_verify.pem \
  -noverify \
  -out /dev/null


# ============================================================
# 13. Tamper test
# ============================================================

cp ~/service/signserver/a1.jpeg.p7m \
   ~/service/signserver/hacked_a1.jpeg.p7m

sed -i 's/A/B/g' ~/service/signserver/hacked_a1.jpeg.p7m

openssl cms -verify \
  -inform DER \
  -in ~/service/signserver/hacked_a1.jpeg.p7m \
  -noverify \
  -out ~/service/signserver/failed_out.jpeg

openssl cms -verify \
  -inform DER \
  -in ~/service/signserver/hacked_a1.jpeg.p7m \
  -noverify \
  > /dev/null


# ============================================================
# 14. Backup and restore scripts
# ============================================================

chmod +x backup.sh
chmod +x restore.sh


# ============================================================
# 15. Create simple PoC worker properties
# ============================================================

cat << 'EOF' | tr -d '\r' > poc.properties
WORKER7.NAME=ImageFingerprintSigner
WORKER7.TYPE=PROCESSABLE
WORKER7.IMPLEMENTATION_CLASS=org.signserver.server.cryptosigners.MessageDigestSigner
EOF


# ============================================================
# 16. WildFly / JBoss maintenance
# ============================================================

cat /opt/signserver/conf/signserver_deploy.properties

$APPSRV_HOME/bin/jboss-cli.sh --connect --command=":reload"

$APPSRV_HOME/bin/jboss-cli.sh \
  --connect \
  --command=":read-attribute(name=server-state)"


# ============================================================
# 17. Simulate nginx client certificate headers
# ============================================================

curl -sk https://127.0.0.1:19443/signserver/adminweb/ \
  -H "SSL_CLIENT_VERIFY: SUCCESS" \
  -H "SSL_CLIENT_CERT: $(cat ~/signserver/secrets/admin.crt | python3 -c 'import sys,urllib.parse; print(urllib.parse.quote(sys.stdin.read()))')" \
| grep -i "logged\|auth\|error" | head -5


# ============================================================
# 18. Other endpoint tests
# ============================================================

curl -X POST \
  -H "Content-Type: application/octet-stream" \
  --data-binary @/home/srv/service/signserver/img1.jpg \
  "https://bitdove.net" \
  -o ~/service/signserver/img1.jpg.p7m
```

## BUG

Only the URL of the Administration Web page https://localhost:19443/signserver/ (https://localhost/signserver/adminweb/) was missing the port. After manually adding it, all the connection ports in the interface were correct.





