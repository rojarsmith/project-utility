# yocto4-ubuntu2204

## qemuarm64

Passed: Ubuntu 22.04

```bash
export Y_MACHINE=qemuarm64

sudo apt update

sudo apt install gawk wget git diffstat unzip texinfo gcc build-essential chrpath socat cpio python3 python3-pip python3-pexpect xz-utils debianutils iputils-ping python3-git python3-jinja2 libegl1-mesa libsdl1.2-dev pylint xterm python3-subunit mesa-common-dev zstd liblz4-tool

mkdir yocto
cd yocto

git clone git://git.yoctoproject.org/poky
pushd poky
git checkout tags/yocto-4.0.20 -b yocto-4.0.20-local
# Host distribution "ubuntu-22.04" has not been validated
# git checkout -t origin/hardknott -b my-hardknott
popd

git clone -b kirkstone https://github.com/openembedded/meta-openembedded

# 5.3.2 is last LGPL v2.1
git clone -b kirkstone https://github.com/meta-qt5/meta-qt5
git clone -b v6.2.9-lts https://code.qt.io/yocto/meta-qt6

source poky/oe-init-build-env build-qemu-arm64

bitbake-layers add-layer ../meta-openembedded/meta-oe
bitbake-layers add-layer ../meta-openembedded/meta-python
bitbake-layers add-layer ../meta-qt6
# GTK4
bitbake-layers add-layer ../meta-openembedded/meta-python
bitbake-layers add-layer ../meta-openembedded/meta-networking
bitbake-layers add-layer ../meta-openembedded/meta-gnome

# local.conf
IMAGE_INSTALL:append = " gtk4 gtk4-demo"

sed -i '/qemuarm64/s/^#//g' conf/local.conf

bitbake core-image-minimal

# core-image-minimal-qemuarm64.ext4
# login: root
runqemu $Y_MACHINE nographic core-image-minimal ext4

# > Linux qemuarm64 5.15.150-yocto-standard
uname -a

bitbake core-image-full-cmdline
ls tmp/deploy/images/$Y_MACHINE

runqemu $Y_MACHINE nographic core-image-full-cmdline ext4

bitbake core-image-sato

runqemu $Y_MACHINE

dmesg
dmesg | grep qt
```

QEMU on Windows

```shell
"C:\Program Files\qemu\qemu-system-aarch64" -device virtio-net-pci,netdev=net0,mac=52:54:00:12:34:02 -netdev user,id=net0 -drive id=disk0,file=core-image-sato-qemuarm64-20240925025858.rootfs.ext4,if=none,format=raw -device virtio-blk-pci,drive=disk0 -device qemu-xhci -device usb-tablet -device usb-kbd -machine virt -cpu cortex-a57 -smp 1 -m 1024 -serial mon:vc -serial null -display sdl,show-cursor=on -device virtio-gpu-pci -kernel Image--5.15.157+git0+7cdb56640a_aeb63de105-r0-qemuarm64-20240925025858.bin -append "root=/dev/vda rw mem=1024M ip=192.168.7.2::192.168.7.1:255.255.255.0::eth0:off:8.8.8.8"
```

