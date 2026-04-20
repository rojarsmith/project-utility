# Project Utility

## Git

### git-clone-alot.bat

Batch clone all GIT repositories in git-clone-alot.txt to the upper directory.

### git-pull-alot.bat

Search and batch pull all GIT projects on upper-level directory.

### project-list.bat

List the directory names of all GIT projects in the previous level

## Frontend Debug

chrome --incognito --headless --remote-debugging-port=9222
C:/Users/dev/Desktop/GoogleChromePortable64/GoogleChromePortable.exe --private-window

## VMware

Create a linked ubuntu vm for test.

```shell
vmws-lab-ubu.bat templateDir "D:\vmubu2404sv" outputRoot "D:" vmName "vmubu2404sv1"

ping -4 vmubu2404sv1
```

Preinstall

```bash
sudo apt install -y open-vm-tools
sudo systemctl enable --now open-vm-tools
# Ping host name
sudo apt install avahi-daemon -y
sudo systemctl enable avahi-daemon
sudo systemctl start avahi-daemon
```

