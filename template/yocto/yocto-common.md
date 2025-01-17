# Yocto Common

```bash
tar -xvf git-2.47.1-1-aarch64.pkg.tar
# usr/bin
sudo cp -r usr /

# Check number of CPU cores
cat /sys/devices/system/cpu/online

# Disable
echo 0 | sudo tee /sys/devices/system/cpu/cpu1/online

# CPU performance
perf stat -a --per-core sleep 5

# Check display
echo $WAYLAND_DISPLAY

# Check weston
ps aux | grep weston

electron --no-sandbox --disable-gpu --ozone-platform=wayland .
```

## RS485

```bash
dmesg | grep tty
ls /dev/tty*
udevadm info --query=all --name=/dev/ttyS0
udevadm info --query=all --name=/dev/ttyUSB0
minicom -D /dev/ttyS0 -b 115200
```

## NET

```bash
iperf3 -c <server-ip> -u -b 10M
iperf3 -c <server-ip> -b 1G

ethtool eth0

# Wi-Fi
iwconfig

netperf
tcpdump
```

## Package

nInvaders
Console game.



