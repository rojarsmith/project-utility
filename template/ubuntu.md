# Ubuntu

## Auto Update

```bash
sudo dpkg-reconfigure unattended-upgrades
```

## Upgrade

```bash
# 24.04 LTS Noble

screen -S upgrade

# Old MongoDB
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 656408E390CFB1F5
sudo mv /etc/apt/sources.list.d/mongodb-org-4.4.list \
        /etc/apt/sources.list.d/mongodb-org-4.4.list.disabled

sudo apt update && sudo apt upgrade -y && sudo apt dist-upgrade -y
sudo apt autoremove -y
sudo do-release-upgrade
sudo reboot
lsb_release -a
```

