# Nginx

A copy-paste-oriented reference for common Nginx setups. All domains are normalized to `example.com`-style placeholders — replace before use.

## Contents

- [Location Matching Rules](#location-matching-rules)
- [Simple File Server (Basic Auth + Autoindex)](#simple-file-server-basic-auth--autoindex)
- [Load Balancing](#load-balancing)
- [WebSocket Reverse Proxy](#websocket-reverse-proxy)
- [SSL / HTTPS](#ssl--https)
- [Rate Limiting](#rate-limiting)
- [Static Asset Caching](#static-asset-caching)

---

## Location Matching Rules

Syntax: `location [ = | ~ | ~* | ^~ ] /uri/ { ... }`

**Priority:** `=` (exact) is checked first, then `^~`, then regex rules (`~`, `~*`) in the order they appear in the file, and finally the generic `/` prefix match. Matching stops at the first successful rule, which then handles the request.

| Modifier | Meaning |
|---|---|
| `=` | Exact match |
| `^~` | Prefix match on a literal string; when it matches, regex rules are skipped. Nginx does not URL-decode here, so a request for `/static/20%/aa` can be matched by `^~ /static/ /aa` (note the space) |
| `~` | Case-sensitive regex match |
| `~*` | Case-insensitive regex match |
| `!~` / `!~*` | Case-sensitive / case-insensitive regex **non**-match |
| `/` | Generic prefix match — matches any request (lowest priority) |

Useful variables (e.g. in `log_format` or proxy headers):

| Variable | Meaning |
|---|---|
| `$http_user_agent` | Client user agent (usually the browser) |
| `$http_x_forwarded_for` | Records the real client IP when requests pass through a proxy |
| `$http_referer` | The link the user came from |

### Example: exact match

```nginx
location = /ads.txt {
    try_files /ads.txt =404;
}
```

> Put `if` **inside** `location` — otherwise it may take precedence over the `location` blocks.

---

## Simple File Server (Basic Auth + Autoindex)

Password-protected directory listing with an IP allowlist.

### Setup

```bash
NGINX_CONFIG=simple-file-server
USER_NAME=user001

# Check which user nginx runs as
ps -o user,group,comm -C nginx

# Create a shared group for web files
sudo groupadd webfiles
sudo usermod -aG webfiles ubuntu
sudo usermod -aG webfiles www-data

# Create the docroot; inspect permissions along the path
sudo mkdir /var/www/sfs
sudo namei -l /var/www/html
sudo namei -l /var/www/sfs

# Ownership + permissions (pick one chown)
sudo chown -R root:webfiles /var/www/sfs
# or: sudo chown -R $USER:$USER /var/www/sfs
sudo chmod -R 750 /var/www/sfs

# Create basic-auth credentials (second command prompts for the password)
sudo sh -c "echo -n '$USER_NAME:' >> /etc/nginx/.htpasswd"
sudo sh -c "openssl passwd -apr1 >> /etc/nginx/.htpasswd"
```

### Config

`/etc/nginx/sites-available/simple-file-server`:

```nginx
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /var/www/sfs;
    server_name files.example.com;

    location / {
        auth_basic "You need to login";
        auth_basic_user_file /etc/nginx/.htpasswd;
        autoindex on;
        autoindex_exact_size off;
        autoindex_localtime on;
        allow 122.0.0.0/24;
        deny all;
    }
}
```

### Enable and test

```bash
sudo ln -s /etc/nginx/sites-available/$NGINX_CONFIG /etc/nginx/sites-enabled/
sudo ls /etc/nginx/sites-enabled/

sudo nginx -t
sudo systemctl restart nginx

# Download a file with basic auth
curl -v -u USERNAME:PASSWORD -O http://files.example.com/file.txt
```

### HTTPS with Certbot

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d example.com --email email@example.com
```

---

## Load Balancing

For load balancing + high availability, only the entry node needs SSL.

```nginx
http {
    upstream webserver {
        server 172.16.0.11:80;
        server 172.16.0.12:80;
    }

    server {
        listen 80;

        location / {
            proxy_pass http://webserver;
        }
    }
}
```

---

## WebSocket Reverse Proxy

### How it works

WebSocket runs on ports 80/443 with the `ws://` / `wss://` scheme and upgrades from HTTP/1.1 via a `101 Switching Protocols` handshake. App servers usually speak plain `ws`; to expose them securely over the internet, terminate TLS at Nginx:

```
Client <- WSS -> Nginx (proxy) <- WS -> Application Server
```

The client requests a protocol upgrade with:

```
Upgrade: websocket
Connection: Upgrade
```

The server replies:

```
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: upgrade
```

After the handshake, both sides are peers and exchange WebSocket data frames directly — no further HTTP.

### Config (single hop)

Prerequisite: a domain with a certificate. `/etc/nginx/conf.d/websocket.conf`:

```nginx
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}

upstream websocket {
    server localhost:8282;  # appserver_ip:ws_port
}

server {
    listen 443 ssl;
    server_name example.com;

    location / {
        proxy_pass http://websocket;
        proxy_read_timeout 300s;
        proxy_send_timeout 300s;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
    }

    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
}
```

Notes:

- The two `Upgrade` / `Connection` headers are the **only** difference from a normal HTTP reverse proxy.
- The `map` block forwards `Connection: upgrade` only when the client actually sent an `Upgrade` header — more elegant than forwarding it unconditionally.
- Idle connections close after 60s by default; raise `proxy_read_timeout` and/or have the upstream send periodic ping frames to keep connections alive.

### Timeout parameters

| Directive | Default | Context | Meaning |
|---|---|---|---|
| `proxy_read_timeout` | 60s | http, server, location | Read timeout toward the upstream. Not the time for the whole response — the max interval between two successive **read** operations |
| `proxy_send_timeout` | 60s | http, server, location | Write timeout toward the upstream. Measured between two successive **write** operations; if the upstream receives nothing new within it, Nginx closes the connection |

### Two-tier (double) proxy

Use case: a domain unreachable from some networks (e.g. mobile). A public cloud host forwards to an internal domain (`inner.example.com`) that resolves only inside the network. Only the outermost hop uses `wss`; everything behind it is plain `ws` on port 80.

Public host (TLS termination):

```nginx
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}

server {
    listen 443 ssl;
    server_name example.com;

    location / {
        proxy_pass http://inner.example.com;
        proxy_read_timeout 300s;
        proxy_send_timeout 300s;
        # NOTE: Host header intentionally NOT overridden on this hop
        # proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
    }

    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}
```

Internal / gateway host:

```nginx
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}

upstream websocket {
    server localhost:8282;  # appserver_ip:ws_port
}

server {
    listen 80;
    server_name inner.example.com;

    location / {
        proxy_pass http://websocket;
        proxy_read_timeout 300s;
        proxy_send_timeout 300s;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
    }
}
```

---

## SSL / HTTPS

### Redirect HTTP to HTTPS

```nginx
# 301 redirect on port 80
server {
    listen 80;
    server_name example.com www.example.com;
    return 301 https://www.example.com$request_uri;
}
```

> `return 301 ...$request_uri;` is the recommended modern form. The older style `rewrite ^/(.*)$ https://example.com/$1 permanent;` still appears in many articles but is no longer recommended.

### HTTPS server block

```nginx
server {
    listen 443 ssl;               # 'ssl on;' is deprecated -- use 'listen ... ssl'
    server_name www.example.com;
    root  wwwroot;
    index index.html index.htm;

    ssl_certificate     /usr/ssl/ca.pem;
    ssl_certificate_key /usr/ssl/ca.key;

    ssl_session_timeout 5m;
    ssl_protocols TLSv1.2 TLSv1.3;   # SSLv2/SSLv3/TLSv1.0/1.1 are insecure -- do not enable
    ssl_prefer_server_ciphers on;
    # ssl_ciphers: modern nginx defaults are reasonable; use the Mozilla
    # SSL Configuration Generator if you need a tuned cipher list.

    # Redirect plain-HTTP requests that hit the HTTPS port (nginx code 497)
    error_page 497 https://$host$uri?$args;

    location / {
        # ...
    }
}
```

### PHP / FastCGI behind HTTPS

Some apps (e.g. phpMyAdmin) only see the forwarded port and keep generating `http://` URLs. Fix it by telling FastCGI the connection is HTTPS:

```nginx
location ~ .*\.(php|php5)?$ {
    try_files $uri =404;
    fastcgi_pass  unix:/tmp/php-cgi.sock;
    fastcgi_index index.php;
    fastcgi_param HTTPS on;   # <-- the fix
    include fcgi.conf;
}
```

---

## Rate Limiting

### Concurrent connections + bandwidth (`limit_conn`)

Limit how many simultaneous connections a single IP may hold, and cap per-connection bandwidth.

```nginx
http {
    # Shared-memory zone 'lczten' (10 MB) keyed by client IP.
    # limit_conn_zone replaced the older limit_zone directive.
    # limit_conn_zone is valid in http context only.
    limit_conn_zone $binary_remote_addr zone=lczten:10m;

    server {
        location / {
            # limit_conn is valid in http, server, location
            limit_conn lczten 10;  # max 10 concurrent connections per IP
            limit_rate 50k;        # per-CONNECTION cap: an IP with 2 connections gets 2 x 50k
        }
    }
}
```

### Request frequency (`limit_req`)

Limit how many requests a single IP can make over time — helps mitigate CC-style flood attacks.

How it works:

- `$binary_remote_addr` — key by client IP (per-IP limiting).
- `zone=lrzten:10m` — zone named `lrzten` using up to 10 MB of memory; 1 MB stores ~16,000 IP states, so 10 MB easily covers 100k+ IPs.
- `rate=100r/s` — the rate value must be an integer; for 1 request per 2 seconds write `30r/m`. Nginx converts the rate into a per-request interval: e.g. `100r/m` becomes one request per 600 ms, so 10 requests arriving within 600 ms means only the first is accepted (plus whatever `burst` allows) and the rest are rejected.

```nginx
http {
    # limit_req_zone is valid in http context only.
    # WordPress reference value: rate=100r/s
    limit_req_zone $binary_remote_addr zone=lrzten:10m rate=100r/s;

    server {
        location / {
            # Example with rate=20r/s, burst=5:
            # - If seconds 1-4 each had 19 requests, 25 requests in second 5 are allowed.
            # - But 25 requests in second 1 -> the excess returns 503.
            # nodelay: without it, excess requests within burst are queued and
            # served at the average rate (e.g. 5 of 25 pushed to the next second);
            # with nodelay, all 25 are served immediately in second 1.
            limit_req zone=lrzten burst=5 nodelay;
        }
    }
}
```

---

## Static Asset Caching

### Disable caching (development)

Avoids constantly clearing the cache / hard-refreshing while debugging:

```nginx
location ~ .*\.(css|js|swf|php|htm|html)$ {
    add_header Cache-Control no-store;
    add_header Pragma no-cache;
}
```

### Browser caching with `expires` (production)

For rarely-changing static content (images, JS, CSS), set an expiry so browsers serve from local cache without re-requesting — reduces bandwidth and server load. `Expires` is a response header telling the browser it may use cached data until the expiry time passes.

```nginx
# Images rarely change -> long expiry; shorten it if they update often
location ~ .*\.(gif|jpg|jpeg|png|bmp|swf)$ {
    expires 30d;
}

location ~ .*\.(js|css)$ {
    expires 10d;
}
```
