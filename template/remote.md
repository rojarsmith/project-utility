# Remote

## VNC

### RealVNC

Support Ubuntu 24.04

```bash
sudo apt install openssh-server

# confirm x11
echo $XDG_SESSION_TYPE

sudo dpkg -i VNC-Server-6.11.0-Linux-x64.deb
# WaylandEnable=false
sudo vi /etc/gdm3/custom.conf

sudo vnclicense -add $REALVNC_KEY

sudo vncinitconfig -install-defaults

# Start or stop the service with
sudo systemctl start vncserver-x11-serviced.service
# Mark or unmark the service to be started at boot time with:
sudo systemctl enable vncserver-x11-serviced.service
```

