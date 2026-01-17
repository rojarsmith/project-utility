# Ubuntu

## Upgrade

```bash
# 24.04 LTS Noble

screen -S upgrade

# Old MongoDB
sudo mv /etc/apt/sources.list.d/mongodb-org-4.4.list \
        /etc/apt/sources.list.d/mongodb-org-4.4.list.disabled

sudo apt update && sudo apt upgrade -y && sudo apt dist-upgrade -y
sudo apt autoremove -y
sudo do-release-upgrade
sudo reboot
lsb_release -a
```

