# Ubuntu

## Upgrade

```bash
# 24.04 LTS Noble

screen -S upgrade
sudo apt update && sudo apt upgrade -y && sudo apt dist-upgrade -y
sudo apt autoremove -y
sudo do-release-upgrade
sudo reboot
lsb_release -a
```

