# KARO QS93-SV01

Core Board: QS93-5210

Dual ARM Cortex-A55, 1.7 GHz 
ARM Cortex-M33, 250 MHz
 ARM Ethos U-65 microNPU
1GB LPDDR4
2MB NOR Flash
4GB eMMC

Boot time: ~20 seconds

ATTENTION

DO NOT disconnect USB-C poser supply while USB-UART (micro USB) is connected

micro USB: Silicon Labs CP210x USB to UART Bridge (COMx)

## Device Side Commands

```bash
# NIC name
ip link show

# DHCP
dhcpcd eth0
ip addr show eth0
ping google.com
```

## Build and flash quick guide

Yocto, Support Ubuntu 22.04

```bash
sudo apt update
sudo apt install curl
sudo apt install gawk wget git diffstat unzip texinfo gcc build-essential chrpath socat cpio \
python3 python3-pip python3-pexpect xz-utils debianutils iputils-ping python3-git \
python3-jinja2 \
libegl1-mesa libsdl1.2-dev python3-subunit mesa-common-dev zstd liblz4-tool file locales
sudo locale-gen en_US.UTF-8
sudo apt install python-is-python3

git config --global user.name "Rojar Smith"
git config --global user.email "rojarsmith@gmail.com"

mkdir -p bin
curl https://storage.googleapis.com/git-repo-downloads/repo > bin/repo
chmod a+x bin/repo
echo 'export PATH=~/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

mkdir karo-nxp-bsp;cd karo-nxp-bsp
#-----choice begin
# Scarthgap
repo init -u https://github.com/karo-electronics/karo-nxp-bsp -b refs/tags/KARO-2025-01-29
# mickledore
repo init -u https://github.com/karo-electronics/karo-nxp-bsp -b mickledore
repo init -u https://github.com/karo-electronics/karo-nxp-bsp -b refs/tags/KARO-2024-08-02
#-----choice end
repo sync

# Setup Build Directory
#-----choice begin
KARO_BASEBOARD=qsbase93
DISTRO=karo-xwayland MACHINE=qs93-5210 source karo-setup-release.sh -b build-qs93-5210
# Not support nodejs
KARO_BASEBOARD=qsbase93
DISTRO=karo-minimal MACHINE=qs93-5210 source karo-setup-release.sh -b build-qs93-5210
#-----choice end

# Enable sstate cache
#-----choice begin
echo SSTATE_MIRRORS = \"file://.* http://sstate.karo-electronics.de/scarthgap/PATH\" >> conf/local.conf
echo SSTATE_MIRRORS = \"file://.* http://sstate.karo-electronics.de/mickledore/PATH\" >> conf/local.conf
#-----choice end

# Add packages

#-----choice begin
bitbake karo-image-weston
bitbake karo-image-minimal
#-----choice end

# Disable `Local Security Authority protection` to use unsigned drivers in the Windows.

# First time change the jump to H position(download mode)
# Jump L －＋＋
# Restart board, no need power off. No need debug micro USB at this time.
# Set `NXP Semiconductors OO Blank 93` to VM.
# Set `NXP Semiconductors USB download gadget` to VM.
# Flash the module
#-----choice begin
pushd tmp/deploy/images/qs93-5210/karo-image-weston
pushd tmp/deploy/images/qs93-5210/karo-image-minimal
#-----choice end
wget https://github.com/nxp-imx/mfgtools/releases/download/uuu_1.5.182/uuu
chmod a+x uuu
sudo ./uuu -v

# Change the jump to L and reset
# Jump L ＋＋－

# Return to environment
cd ~/karo-nxp-bsp
source setup-environment build-qs93-5210
```

## SDK

```bash
bitbake meta-toolchain

# ~/karo-nxp-bsp/build-qs93-5210/tmp/deploy
pushd tmp/deploy
#-----choice begin
./sdk/karo-xwayland-glibc-x86_64-meta-toolchain-cortexa55-qs93-5210-toolchain-6.6-scarthgap.sh -d /opt/
./sdk/karo-xwayland-glibc-x86_64-meta-toolchain-cortexa55-qs93-5210-toolchain-6.1-mickledore.sh -d /opt/
#-----choice end

source /opt/environment-setup-cortexa55-poky-linux
echo $CC
# aarch64-poky-linux-gcc -mcpu=cortex-a55 -march=armv8.2-a+crypto -mbranch-protection=standard -fstack-protector-strong -O2 -D_FORTIFY_SOURCE=2 -Wformat -Wformat-security -Werror=format-security --sysroot=/opt/sysroots/cortexa55-poky-linux

$CC helloWorld.c -o hello
```

## CoreMark

```bash
mkdir ~/coremark;cd ~/coremark
git clone https://github.com/eembc/coremark.git
mkdir coremark/karo_qs93sv01_linux
cp coremark/linux/* coremark/karo_qs93sv01_linux
mkdir coremark/karo_qs93sv01_linux/posix
cp coremark/posix/* coremark/karo_qs93sv01_linux/posix


sudo apt-cache search aarch64
# If not work, use SDK
sudo apt-get install -y gcc-aarch64-linux-gnu
# SDK:
# /opt/sysroots/x86_64-pokysdk-linux/usr/bin/aarch64-poky-linux/aarch64-poky-linux-gcc
which aarch64-poky-linux-gcc

cd coremark
gedit Makefile &

# Remove space between LOAD and OUTFILE in Makefile
$(LOAD)$(OUTFILE)

# Compile CoreMark and make coremark.exe
# ~/coremark/coremark
make PORT_DIR=karo_qs93sv01_linux

# Make *.exe executable if not already the case
chmod +x coremark.exe

# Copy CoreMark executable onto the board:
# scp coremark.exe root@<IP@>:/usr/local/
scp coremark.exe root@192.168.237.164:/usr/local/

# To run CoreMark on the board, 7 is single core
cd /usr/local
./usr/local/coremark.exe 0x0 0x0 0x66 0 7 1 2000 > run.log
```

`run.log`

```ini
2K performance run parameters for coremark.
CoreMark Size    : 666
Total ticks      : 17687
Total time (secs): 17.687000
Iterations/Sec   : 6219.257081
Iterations       : 110000
Compiler version : GCC12.3.0
Compiler flags   : -O2 -DPERFORMANCE_RUN=1  -lrt
Memory location  : Please put data memory location here
                        (e.g. code in flash, data on heap etc)
seedcrc          : 0xe9f5
[0]crclist       : 0xe714
[0]crcmatrix     : 0x1fd7
[0]crcstate      : 0x8e3a
[0]crcfinal      : 0x33ff
Correct operation validated. See README.md for run and reporting rules.
CoreMark 1.0 : 6219.257081 / GCC12.3.0 -O2 -DPERFORMANCE_RUN=1  -lrt / Heap
```

`core_portme.h`

```c
#define MULTITHREAD 1
```

## Conf

`local.conf`

```bash
# Disable for write
# EXTRA_IMAGE_FEATURES += "read-only-rootfs"
```

### Packages

`local.conf`

```bash
# rt-tests: cyclictest
# evtest: test driver event
IMAGE_INSTALL:append = " \
    htop \
    rt-tests \
    openssh openssh-sftp-server \
    opkg \
    evtest \
"

# Electron
IMAGE_INSTALL:append = " \
    git \
    nodejs \
    nodejs-npm \
    cups \
    libxscrnsaver \
    nss \
"
```

## U-Boot

```bash
# U-Boot >
# (Re-)boot the board and “Hit any key to stop autoboot” to get to the U-Boot command line interface
fastboot usb 0
# Add `USB download gadget`

mmc list
mmc dev 0:1
mmc dev
ext4ls mmc 0:1 /
```

## Display

```bash
## U-BOOT >
# Check .dtb, remove prefix `imx93-`
ext4ls mmc 0:1 /
setenv overlays_qsbase93 ${overlays_qsbase93} karo-lvds-panel karo-panel-tm101jvhg32tm101jvhg32
saveenv
reset

printenv overlays_qsbase93
# default: overlays_qsbase93=karo-gpu qs93-eqos-lan8710 qs93-fec-lan8710
# TM101JVHG32: overlays_qsbase93=karo-gpu qs93-eqos-lan8710 qs93-fec-lan8710 karo-lvds-panel karo-panel-tm101jvhg32

# clear
setenv overlays_qsbase93 ""
saveenv

env default -a
saveenv

## Yocto >
ls /run/user/1000/

export XDG_RUNTIME_DIR=/run/user/1000
export WAYLAND_DISPLAY=wayland-1

electron --no-sandbox --disable-gpu --ozone-platform=wayland .

ls /tmp/.X11-unix/
# X0
```

### Rebuild kernel dtb

```bash
bitbake -c cleansstate virtual/kernel
bitbake virtual/kernel

ls tmp/deploy/images/qs93-5210/*.dtb
```

## Touch

```bash
root@qs93-5210:~# dmesg | grep -i touch
# [    0.082563] usbcore: registered new interface driver usbtouchscreen
# [    0.725105] hid-multitouch 0003:222A:0001.0001: input: USB HID v1.10 Device [ILITEK ILITEK-TP] on usb-ci_hdrc.1-1/input0

# Error
dmesg | grep -i touch
# [    0.082505] usbcore: registered new interface driver usbtouchscreen
lsusb
# Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub

ls /dev/input/
# by-id  by-path  event0  event1  touchscreen0

# evtest-1.35-2-aarch64.pkg.tar.xz
```

## Electron

Ubuntu 22.04 need 24GB RAM, 16GB can't compile nodejs.

```bash
ps aux | grep Xwayland

echo $DISPLAY

electron main.js --no-sandbox --disable-gpu --headless

# electron exited with signal SIGSEGV
# Device not have LVDS display
```

