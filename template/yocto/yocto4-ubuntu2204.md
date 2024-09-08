# yocto4-ubuntu2204

## qemuarm64

```bash
export Y_MACHINE=qemuarm64

sudo apt update

sudo apt install gawk wget git diffstat unzip texinfo gcc build-essential chrpath socat cpio python3 python3-pip python3-pexpect xz-utils debianutils iputils-ping python3-git python3-jinja2 libegl1-mesa libsdl1.2-dev pylint xterm python3-subunit mesa-common-dev zstd liblz4-tool

mkdir yocto
cd yocto

git clone git://git.yoctoproject.org/poky
pushd poky
git checkout tags/yocto-4.0.18 -b yocto-4.0.18-local
popd

git clone -b kirkstone https://github.com/openembedded/meta-openembedded

git clone -b v6.2.9-lts https://code.qt.io/yocto/meta-qt6

source poky/oe-init-build-env build-qemu-arm64

bitbake-layers add-layer ../meta-openembedded/meta-oe
bitbake-layers add-layer ../meta-openembedded/meta-python
bitbake-layers add-layer ../meta-qt6

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

