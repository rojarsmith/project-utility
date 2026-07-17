# Linux

## Certbot Let's Encrypt SSL

```bash
## Pass ubuntu 20.04, Not support ubuntu 14.04

# Manually Renew Certificate
sudo certbot renew

# Check version
certbot --version

# List all installed certificates
sudo certbot certificates

# Query the status of the timer with systemctl.
sudo systemctl status certbot.timer

# Add domain to existing certificate
# Need to specify all of the names, including those already registered.
/opt/certbot/certbot-auto certonly --agree-tos \
--email me@example.com \
--expand -d example.com -d www.example.com

# 參數
renew 更新已經獲取但快過期的所有證書
  --apache 使用Apache插件進行身份認證和安裝
  --standalone 運行一個獨立的網頁服務器用於身份認證
  --nginx 使用Nginx插件進行身份認證和安裝
  --webroot 把身份認證文件放置在服務器的網頁根目錄下
  --manual 使用交互式或腳本鉤子的方式獲取證書

# Options
-w --webroot-path public_html / webroot path.
--webroot 把身份認證文件放置在服務器的網頁根目錄下用於獲取證書。(默認: False)
--no-self-upgrade 讓 certbot-auto 不要自動更新版本
--agree-tos 同意ACME訂閱協議 (默認: 詢問)
--expand 如果請求的證書名字是已經存在的證書名字的子集，那麼這個本地證書會被重置並重命名。(默認: 詢問) 
--force-renewal, --renew-by-default
  如果請求的證書已經存在，無論是否快要到期，更新該證書。
  (通常使用--keep-until-expiring 選項)。
  該選項默認包含了--expand 選項的功能。(默認: False)
  
# IF YOU DO NOT HAVE PORT80 ACCESSIBLE, YOU MUST USE DNS VERIFICATION.

# 如果不想中斷server須使用 webroot （自備 HTTP 伺服器，自行設定 acme-challenge 部分）certbot certonly --webroot
sudo certbot delete --cert-name www.domain.net
```

```nginx
# Nginx
listen 443 ssl; # managed by Certbot
ssl_certificate /etc/letsencrypt/live/domain.com/fullchain.pem; # managed by Certbot
ssl_certificate_key /etc/letsencrypt/live/domain.com/privkey.pem; # managed by Certbot
include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
```

Certbot Standalone Mode to Retrieve Let's Encrypt SSL Certificates on Ubuntu 20.04

```bash
# Install
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:certbot/certbot
sudo apt-get update
sudo apt-get install certbot

# OR

sudo snap install core; sudo snap refresh core
sudo apt remove certbot
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot

sudo ufw allow 443

sudo certbot certonly --standalone -d your_domain1 -d your_domain2

sudo ls /etc/letsencrypt/live/your_domain

# The certbot package we installed takes care of this for us by adding a renew script to /etc/cron.d. # This script runs twice a day and will renew any certificate that’s within thirty days of expiration.

# renew_hook
sudo vi /etc/letsencrypt/renewal/your_domain.conf
# your_domain.conf’>/etc/letsencrypt/renewal/your_domain.conf
# Add on the last line.
renew_hook = systemctl reload your_service or other script

# Dry run to make sure the syntax is ok.
sudo certbot renew --dry-run

# Let's encrypt "too many failed authorizations recently"
rm /etc/letsencrypt/accounts
```

Auto renew

```bash
Debian cerbot 套件包含兩種SSL認證機制：cron和system timer。
Cronjob
你的cronjob應該在這裡  /etc/cron.d/certbot
Certbot timer 應該在這裡/lib/systemd/system/certbot.timer
精確來說，他應該會在這裡執行指令 /lib/systemd/system/certbot.service

# 如果混用多種驗證，可以都用standalone，disable installer.
# Chek /etc/letsencrypt/renewal/*.conf
authenticator = standalone
#installer = nginx

# renew-hook has been deprecated in recent versions of certbot. Plus, debian moved from using cronjobs for automatic renewals to systemd timer if they are available. On the other hand, now certbot supports having hooks in configuration files.
vi /etc/letsencrypt/renewal-hooks/deploy/01-reload-nginx

#! /bin/sh
set -e # Exit the script if an error happens

sudo systemctl restart nginx

# Or
/etc/init.d/nginx configtest
/etc/init.d/nginx reload

# Make the file executable.
chmod +x /etc/letsencrypt/renewal-hooks/deploy/01-reload-nginx

##

# 使用的是standalone方式驗證證書，同時你又時刻執行著自己的nginx伺服器，那麼當驗證的時候就需要關閉nginx服務，這時候就可以使用鉤子來自動化完成這個操
# 將鉤子檔案放到指定目錄 /etc/letsencrypt/renewal-hooks/pre, /etc/letsencrypt/renewal-hooks/deploy, /etc/letsencrypt/renewal-hooks/post，那麼這三個資料夾裡的檔案會按照，pre，deply，post型別的鉤子執行。

# 此方法會令伺服器中斷。
vi /etc/letsencrypt/renewal-hooks/pre/01-stop-nginx

sudo systemctl stop nginx

chmod +x /etc/letsencrypt/renewal-hooks/pre/01-stop-nginx

vi /etc/letsencrypt/renewal-hooks/post/01-restart-nginx

chmod +x /etc/letsencrypt/renewal-hooks/post/01-restart-nginx

certbot renew --quiet --no-self-upgrade --nginx
```

```bash
# ACME
sudo mkdir -p /var/www/letsencrypt/.well-known/acme-challenge

location ^~ /.well-known/acme-challenge/ {
   default_type "text/plain";
   root /var/www/letsencrypt;
}

certbot \
certonly \
--webroot \
--webroot-path /var/www/letsencrypt \
--agree-tos \
--email YOUR@EMAIL.COM \
--domains example.com sub1.example.com
--domains 不支援的話換成數個-d elecdove.com 
```

## autoconf



將configure.ac裡所需要的M4宏複製到文件夾中

aclocal

通過configure.ac生成configure腳本

autoconf

autohead

創建build-aux文件夾

mkdir build-aux

創建GNU要求的說明文件

touch NEWS README AUTHORS ChangeLog

通過Makefile.am生成Makefile.in模板

automake --add-missing --copy

./configure

make



## Tomcat



```bash
tomcat在lib目錄下加載自定義的文件夾存放jar包

但是tomcat是無法識別這個ext目錄裡面的文件的，此時需要修改tomcat配置文件${catalina.home}/conf/catalina.properties中的 common.loader值，加上${catalina.home}/lib/ext/*.jar，完成此步驟後，項目啟動便可以使用到lib/ext裡面的jar包了

Install


sudo tar xzvf apache-tomcat-9*tar.gz -C /opt/tomcat --strip-components=1
```

## Logwatch

日志分析工具 Logwatch能够对Linux 的日志文件进行分析，并自动发送mail给相关处理人员，可定制需求 Logwatch的mail功能是借助宿主系统自带的mail server发邮件的，系统需安装mail server , 如sendmail，postfix,Qmail等，具体配置不叙述

## Tree

```bash
sudo apt-get install tree

# 顏色顯示
tree -C

# 顯示文件全路徑
tree -f

# 只顯示2層
tree -L 2

# 只顯示文件目錄和*.pl的perl文件。
tree -P *.pl

# 顯示目錄後面的\；顯示可執行文件*；功能類似ls -F
tree -F

tree –help
```

## crontab

修改crontab後是不需要restart的
crontab -e  #root跟其他人分開設定

10 mins:

```bash
*/10 * * * * /bin/do
```



```bash
# odd days (to be able to keep logs one day for debug purposes):
0 3 * * 1,3,5 truncate -s 0 /root/.forever/*.log
```



sudo crontab -e

systemctl status certbot.timer
cat /lib/systemd/system/certbot.service

0 0 1 */2 * /usr/bin/certbot renew --quiet --no-self-upgrade
35 2 * * 1 sudo systemctl reload nginx
30 2 * * 1 /usr/local/sbin/certbot-auto renew >> /var/log/le-renew.log

0 0 1 */2 * /usr/bin/certbot renew --quiet --no-self-upgrade --nginx
0 0 1 */2 * /usr/bin/certbot renew --quiet --no-self-upgrade --nginx





```bash
# ┌───────────── 分鐘   (0 - 59)
# │ ┌─────────── 小時   (0 - 23)
# │ │ ┌───────── 日     (1 - 31)
# │ │ │ ┌─────── 月     (1 - 12)
# │ │ │ │ ┌───── 星期幾 (0 - 7，0 是週日，6 是週六，7 也是週日)
# │ │ │ │ │
# * * * * * /path/to/command
```

```bash
@reboot	每次重新開機之後，執行一次。
@yearly	每年執行一次，亦即 0 0 1 1 *。
@annually	每年執行一次，亦即 0 0 1 1 *。
@monthly	每月執行一次，亦即 0 0 1 * *。
@weekly	每週執行一次，亦即 0 0 * * 0。
@daily	每天執行一次，亦即 0 0 * * *。
@hourly	每小時執行一次，亦即 0 * * * *。
```

