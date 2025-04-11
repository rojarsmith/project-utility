# Environment

## Software Developer

### Ubuntu 24.04

```bash
sudo apt update;
sudo apt dist-upgrade;
sudo apt install -y open-vm-tools-desktop \
git curl tree meld;
sudo snap install code --classic;
sudo apt autoremove;sudo apt autoclean;

# Docker
sudo apt install -y ca-certificates gnupg;
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg;
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null;
sudo apt update;
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin;
```

