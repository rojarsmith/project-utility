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

## TigerVNC

```bash
sudo apt install -y xfce4 xfce4-goodies xorg dbus-x11 x11-xserver-utils
sudo apt install -y tigervnc-standalone-server tigervnc-common

VNC_PASSWORD="Passw@rd"
mkdir -p ~/.vnc
echo "${VNC_PASSWORD}" | vncpasswd -f > ~/.vnc/passwd
chmod 600 ~/.vnc/passwd
vncserver :1
vncserver -kill :1

sudo tee ~/.vnc/xstartup > /dev/null <<EOF
#!/bin/sh
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
exec startxfce4
EOF

chmod u+x ~/.vnc/xstartup

sudo tee ~/.vnc/config > /dev/null <<EOF
geometry=1280x720
dpi=96
EOF

sudo apt install -y locales
sudo dpkg-reconfigure locales # All locales

# Default language
sudo tee ~/.bashrc > /dev/null <<EOF
export LANG=en_US.UTF8
EOF

# Chinese font
sudo apt install -y fonts-wqy-zenhei xfonts-wqy

# Firefox
sudo apt install -y firefox
# For desktop, fix cannot open display:1.0
xhost +

grep -qxF 'alias firefox="XAUTHORITY=$HOME/.Xauthority firefox"' ~/.bashrc || echo 'alias firefox="XAUTHORITY=$HOME/.Xauthority firefox"' >> ~/.bashrc
source ~/.bashrc

grep -qxF 'export XAUTHORITY=$HOME/.Xauthority' ~/.xprofile || echo 'export XAUTHORITY=$HOME/.Xauthority' >> ~/.xprofile
grep -qxF 'export DISPLAY=:1' ~/.xprofile || echo 'export DISPLAY=:1' >> ~/.xprofile
grep -qxF 'xhost +' ~/.xprofile || echo 'xhost +' >> ~/.xprofile

sed -i '/^unset DBUS_SESSION_BUS_ADDRESS/a \
if [ -f "$HOME/.xprofile" ]; then\n  . "$HOME/.xprofile"\nfi\n' ~/.vnc/xstartup

sudo tee /etc/systemd/system/vncserver@:1.service > /dev/null <<EOF
[Unit]
Description=Start TigerVNC server at startup :1
After=syslog.target network.target

[Service]
Type=forking
User=${USER}
PAMName=login
PIDFile=/home/${USER}/.vnc/%H:1.pid
ExecStartPre=-/usr/bin/vncserver -kill :1
ExecStart=/usr/bin/vncserver :1
ExecStop=/usr/bin/vncserver -kill :1

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable vncserver@:1.service
sudo systemctl start vncserver@:1.service

# Copy ssh-tunnel-template.bat and config
# Run ssh-tunnel.bat
# Run VNC Viewer
```

