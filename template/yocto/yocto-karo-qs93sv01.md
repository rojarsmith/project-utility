# KARO QS93-SV01

Core Board: QS93-5210

Dual ARM Cortex-A55, 1.7 GHz 
ARM Cortex-M33, 250 MHz
 ARM Ethos U-65 microNPU
1GB LPDDR4
2MB NOR Flash
4GB eMMC

```bash
# Device name
ip link show

# DHCP
dhcpcd eth0
ip addr show eth0
ping google.com
```

## Build and flash quick guide

Yocto Mickledore

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
repo init -u https://github.com/karo-electronics/karo-nxp-bsp -b mickledore
repo init -u https://github.com/karo-electronics/karo-nxp-bsp -b refs/tags/KARO-2024-08-02
#-----choice end
repo sync

# Setup Build Directory
KARO_BASEBOARD=qsbase93
DISTRO=karo-minimal MACHINE=qs93-5210 source karo-setup-release.sh -b build-qs93-5210 # Not support nodejs
KARO_BASEBOARD=qsbase93
DISTRO=karo-xwayland MACHINE=qs93-5210 source karo-setup-release.sh -b build-qs93-5210

# Return
source setup-environment build-qs93-5210

# Enable sstate cache
echo SSTATE_MIRRORS = \"file://.* http://sstate.karo-electronics.de/mickledore/PATH\" >> conf/local.conf

#-----choice begin
bitbake karo-image-minimal
bitbake karo-image-weston
#-----choice end

# Change Jump to download mode and restart board, no need power off.
# Set `NXP Semiconductors OO Blank 93` to VM.
# Set `NXP Semiconductors USB download gadget` to VM.
# Flash the module
#-----choice begin
pushd tmp/deploy/images/qs93-5210/karo-image-minimal
pushd tmp/deploy/images/qs93-5210/karo-image-weston
#-----choice end
wget https://github.com/nxp-imx/mfgtools/releases/download/uuu_1.5.141/uuu
chmod a+x uuu
sudo ./uuu -v
```

## SDK

```bash
bitbake meta-toolchain

# ~/karo-nxp-bsp/build-qs93-5210/tmp/deploy
./sdk/karo-xwayland-glibc-x86_64-meta-toolchain-cortexa55-qs93-5210-toolchain-6.1-mickledore.sh -d /opt/

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

## Packages

```bash
# Disable for write
# EXTRA_IMAGE_FEATURES += "read-only-rootfs"

# rt-tests: cyclictest
IMAGE_INSTALL:append = " \
    htop \
    rt-tests \
    openssh openssh-sftp-server \
    opkg \
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

## Electron

Ubuntu 22.04 need 24GB RAM, 16GB can't compile nodejs.

```bash
ps aux | grep Xwayland

echo $DISPLAY

electron main.js --no-sandbox --disable-gpu --headless

# electron exited with signal SIGSEGV
# Device not have LVDS display
```

## Display

```bash
## U-BOOT >
# Check .dtb, remove prefix `imx93-`
ext4ls mmc 0:1 /
#-----choice begin
setenv overlays_qsbase93 ${overlays_qsbase93} karo-lvds-panel karo-panel-tm101jvhg32tm101jvhg32
setenv overlays_qsbase93 ${overlays_qsbase93} lvds-panel panel-
tm101jvhg32tm101jvhg32
#-----choice end
saveenv
reset

printenv overlays_qsbase93
# overlays_qsbase93=karo-gpu qs93-eqos-lan8710 qs93-fec-lan8710 lvds-panel panel-tm101jvhg32
# overlays_qsbase93=karo-gpu qs93-eqos-lan8710 qs93-fec-lan8710 karo-lvds-panel karo-panel-tm101jvhg32

setenv overlays_qsbase93 ""
saveenv

setenv fdt_file imx93-qs93-5210.dtb
saveenv

env default -a
saveenv

mmc list
mmc dev 0:1
mmc dev
ext4ls mmc 0:1 /
##

bitbake -c cleansstate virtual/kernel
bitbake virtual/kernel

ls tmp/deploy/images/qs93-5210/*.dtb
```

