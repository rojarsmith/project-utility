# Nginx

## Simple File Server

```bash
NGINX_CONFIG=simple-file-server
USER_NAME=user001

ps -o user,group,comm -C nginx
sudo groupadd webfiles
sudo usermod -aG webfiles ubuntu
sudo usermod -aG webfiles www-data

sudo mkdir /var/www/sfs
sudo namei -l /var/www/html
sudo namei -l /var/www/sfs
sudo chown -R root:webfiles /var/www/sfs
sudo chown -R $USER:$USER /var/www/sfs
sudo chmod -R 750 /var/www/sfs

sudo sh -c "echo -n '$USER_NAME:' >> /etc/nginx/.htpasswd"
sudo sh -c "openssl passwd -apr1 >> /etc/nginx/.htpasswd"

sudo vi /etc/nginx/sites-available/$NGINX_CONFIG

server {
        listen 80 default_server;
        listen [::]:80 default_server;
        
        root /var/www/sfs;

        server_name repo.neuhex.com;

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

sudo ln -s /etc/nginx/sites-available/$NGINX_CONFIG /etc/nginx/sites-enabled/
sudo ls /etc/nginx/sites-enabled/

sudo nginx -t
sudo systemctl restart nginx

curl -v -u USERNAME:PASSW@RD -O http://sfs.neuhex.com/file.txt

sudo apt install -y certbot python3-certbot-nginx

sudo certbot --nginx -d domain.com --email email@domain.com
```

