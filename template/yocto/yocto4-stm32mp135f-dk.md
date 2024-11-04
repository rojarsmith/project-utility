# Yocto 4 with STM32MP135F-DK

MPU: Arm Cortex‑A7 32-bit
RAM: 0.5 GB DDR3L, 16 bits, 533 MHz
Boot: Support `-optee.tsv`, not support `-trusted.tsv`

## Ubuntu 22.04

```bash
sudo apt update
sudo apt dist-upgrade
sudo apt install -y git curl bc build-essential chrpath cpio diffstat gawk python-is-python3 python3-git python3-jinja2 python3-subunit texinfo wget gdisk libssl-dev gcc-arm-linux-gnueabihf lz4
sudo locale-gen en_US.UTF-8

git config --global user.email "rojarsmith@gmail.com"
git config --global user.name "RojarSmith"

mkdir stm32mp && cd stm32mp

mkdir -p bin
curl https://storage.googleapis.com/git-repo-downloads/repo > bin/repo
chmod a+x bin/repo
echo 'export PATH=~/stm32mp/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

mkdir yocto
pushd yocto
git clone git://git.yoctoproject.org/poky.git
pushd poky
git checkout -t origin/kirkstone -b kirkstone-local
git branch
popd

git clone -b kirkstone http://cgit.openembedded.org/meta-openembedded
git clone -b kirkstone https://github.com/STMicroelectronics/meta-st-stm32mp

source poky/oe-init-build-env build-stm32mp1

bitbake-layers add-layer ../meta-openembedded/meta-oe
bitbake-layers add-layer ../meta-openembedded/meta-python
bitbake-layers add-layer ../meta-st-stm32mp

vi conf/local.conf
# local.conf begin #
MACHINE ?= "stm32mp1"

# rt-tests: cyclictest
IMAGE_INSTALL:append = " \
    htop \
    rt-tests \
"
# local.conf end #

# ERROR: linux-stm32mp is unavailable:  
# linux-stm32mp was skipped: incompatible with machine qemuarm (not in COMPATIBLE_MACHINE)
devtool modify linux-stm32mp

bitbake core-image-minimal

# for MACHINE ?= "qemuarm"
# user: root
# shutdown: exit, ctrl-a, x
runqemu qemuarm nographic

cyclictest --mlockall -t -a --priority=99 --interval=200 --distance=0 -l 1000 taskset -c 1 cyclictest -p 99 -i 1000 -H 200 -D 900

tmp/deploy/images/stm32mp1/scripts/create_sdcard_from_flashlayout.sh tmp/deploy/images/stm32mp1/flashlayout_core-image-minimal/optee/FlashLayout_sdcard_stm32mp135f-dk-optee.tsv

# sd care location: /dev/sdc, /dev/sdb
sudo dd if=tmp/deploy/images/stm32mp1/FlashLayout_sdcard_stm32mp135f-dk-optee.raw of=/dev/sdc bs=8M status=progress conv=fdatasync
```

