# Yocto 4 with STM32MP135F-DK

MPU: Arm Cortex‑A7 32-bit
RAM: 0.5 GB(4-Gbit) DDR3L, 16 bits, 533 MHz
Boot: Support `-optee.tsv`, not support `-trusted.tsv`

```
openstlinux-6.1-yocto-mickledore-mpu-v24.06.26 (Mickledore) is the new version delivered with the STM32MPU-ecosystem-v5.1.0 release. This software set consists of the following components:

Build process
OpenEmbedded v4.2.4 (Mickledore) - Updated
GCC version v12.3.0 - Updated
Embedded software components
Linux kernel v6.1-stm32mp-r2 (v6.1.82) - Updated
TF-A v2.8-stm32mp-r2 - Updated
U-Boot v2022.10-stm32mp-r2 - Updated
OP-TEE 3.19.0-stm32mp-r2 - Updated
External DT 5.0-stm32mp-r1 - New
OpenOCD version v0.12.0 - Updated
Applicative components
Weston version v11.0.1 - Updated
Wayland version 1.21.0 - Updated
GStreamer version v1.22.6 - Updated
GCnano version v6.4.15 - Updated
```

## Ubuntu 22.04

Common

```bash
sudo apt update
sudo apt dist-upgrade
sudo apt install git curl
git config --global user.email "rojarsmith@gmail.com"
git config --global user.name "RojarSmith"
sudo sed -i -e 's/set compatible/set nocompatible/' /etc/vim/vimrc.tiny

mkdir stm32mpws
echo 'export STM32MPWS=~/stm32mpws' >> ~/.bashrc
source ~/.bashrc
pushd $STM32MPWS

mkdir -p bin
curl https://storage.googleapis.com/git-repo-downloads/repo > bin/repo
chmod a+x bin/repo
echo 'export PATH=~/stm32mpws/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

STM32MP1-Ecosystem-v5.1.0

```bash
mkdir $HOME/STM32MPU_workspace
cd $HOME/STM32MPU_workspace

mkdir $HOME/STM32MPU_workspace/STM32MPU-Tools
mkdir $HOME/STM32MPU_workspace/STM32MPU-Tools/STM32CubeProgrammer-2.17.0
mkdir $HOME/STM32MPU_workspace/tmp
pushd $HOME/STM32MPU_workspace/tmp
unzip en.stm32cubeprg-lin-v2-17-0.zip
export PATH=~/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin:$PATH

pushd ~/STMicroelectronics/STM32Cube/STM32CubeProgrammer/Drivers/rules
sudo cp *.* /etc/udev/rules.d
popd

STM32_Programmer_CLI --h
popd

mkdir Starter-Package
pushd Starter-Package

tar -xvf en.FLASH-stm32mp1-openstlinux-6.1-yocto-mickledore-mpu-v24.06.26.tar.gz

# STM32CubeProgrammer with SDCARD slow & display maybe not work
# Binaries Path
/home/dev/STM32MPU_workspace/Starter-Package/stm32mp1-openstlinux-6.1-yocto-mickledore-mpu-v24.06.26/images/stm32mp1

# ~/STM32MPU_workspace/Starter-Package
stm32mp1-openstlinux-6.1-yocto-mickledore-mpu-v24.06.26/images/stm32mp1/scripts/create_sdcard_from_flashlayout.sh stm32mp1-openstlinux-6.1-yocto-mickledore-mpu-v24.06.26/images/stm32mp1/flashlayout_st-image-weston/optee/FlashLayout_sdcard_stm32mp135f-dk-optee.tsv

sudo dd if=stm32mp1-openstlinux-6.1-yocto-mickledore-mpu-v24.06.26/images/stm32mp1/FlashLayout_sdcard_stm32mp135f-dk-optee.raw of=/dev/sdb bs=8M status=progress conv=fdatasync

popd

# Board $>

# Printing distribution specific information
cat /etc/build

-----------------------
Build Configuration:  |
-----------------------
BB_VERSION = 2.4.0
BUILD_SYS = x86_64-linux
NATIVELSBSTRING = universal
TARGET_SYS = arm-ostl-linux-gnueabi
MACHINE = stm32mp1
DISTRO = openstlinux-weston
DISTRO_VERSION = 4.2.4-openstlinux-6.1-yocto-mickledore-mpu-v24.06.26
TUNE_FEATURES = arm vfp cortexa7 neon vfpv4 thumb callconvention-hard
TARGET_FPU = hard
MANIFESTVERSION = ostl-v5.1_rc3-2-ge7eebad74713d2c60cdae9ad43adb1581f4e0edf
DISTRO_CODENAME = mickledore
ACCEPT_EULA_stm32mp1 = 1
GCCVERSION = 12.%
PREFERRED_PROVIDER_virtual/kernel = linux-stm32mp
-----------------------
Layer Revisions:      |
-----------------------
meta-python       = v5.1.xml:aa5e8edabbc414d8ec1b2ad63c8743c7baf99626
meta-oe           = v5.1.xml:aa5e8edabbc414d8ec1b2ad63c8743c7baf99626
meta-gnome        = v5.1.xml:aa5e8edabbc414d8ec1b2ad63c8743c7baf99626
meta-multimedia   = v5.1.xml:aa5e8edabbc414d8ec1b2ad63c8743c7baf99626
meta-networking   = v5.1.xml:aa5e8edabbc414d8ec1b2ad63c8743c7baf99626
meta-webserver    = v5.1.xml:aa5e8edabbc414d8ec1b2ad63c8743c7baf99626
meta-st-stm32mp   = v5.1.xml:c6c94a55b0002dd10a7d129a6ff7eeb10b0bee93
meta-st-openstlinux = v5.1.xml:ab43d854cb735a2175e836d35b6f963db05d68f1
meta              = v5.1.xml:23b5141400b2c676c806df3308f023f7c04e34e0

# Packages required by OpenEmbedded/Yocto
sudo apt-get install gawk wget git git-lfs diffstat unzip texinfo gcc-multilib  chrpath socat cpio python3 python3-pip python3-pexpect xz-utils debianutils iputils-ping python3-git python3-jinja2 libegl1-mesa libsdl1.2-dev pylint xterm bsdmainutils libssl-dev libgmp-dev libmpc-dev lz4 zstd

# Developer Package
sudo apt-get install build-essential libncurses-dev libncurses5 libyaml-dev libssl-dev

sudo apt install python-is-python3

sudo apt-get install coreutils bsdmainutils sed curl bc lrzsz corkscrew cvs subversion mercurial nfs-common nfs-kernel-server libarchive-zip-perl dos2unix texi2html libxml2-utils

echo 'options mmc_block perdev_minors=16' > /tmp/mmc_block.conf
sudo mv /tmp/mmc_block.conf /etc/modprobe.d/mmc_block.conf

mkdir Developer-Package
pushd Developer-Package
tar xvf en.SDK-x86_64-stm32mp1-openstlinux-6.1-yocto-mickledore-mpu-v24.06.26.tar.gz
chmod +x stm32mp1-openstlinux-6.1-yocto-mickledore-mpu-v24.06.26/sdk/st-image-weston-openstlinux-weston-stm32mp1-x86_64-toolchain-4.2.4-openstlinux-6.1-yocto-mickledore-mpu-v24.06.26.sh

./stm32mp1-openstlinux-6.1-yocto-mickledore-mpu-v24.06.26/sdk/st-image-weston-openstlinux-weston-stm32mp1-x86_64-toolchain-4.2.4-openstlinux-6.1-yocto-mickledore-mpu-v24.06.26.sh -d SDK

source SDK/environment-setup-cortexa7t2hf-neon-vfpv4-ostl-linux-gnueabi

echo $ARCH
echo $CROSS_COMPILE
$CC --version
echo $OECORE_SDK_VERSION

# mkdir $HOME/STM32MPU_workspace/STM32MPU-Ecosystem-v5.1.0/Developer-Package
mkdir stm32mp1-openstlinux-24.06.26
mkdir stm32mp1-openstlinux-24.06.26/sources
mkdir stm32mp1-openstlinux-24.06.26/sources/gtk_hello_world_example
pushd stm32mp1-openstlinux-24.06.26/sources/gtk_hello_world_example
touch gtk_hello_world.c
touch Makefile
```

`gtk_hello_world.c`

```c
#include <gtk/gtk.h>

static void
print_hello (GtkWidget *widget,
             gpointer   data)
{
  g_print ("Hello World\n");
}

static void
activate (GtkApplication *app,
          gpointer        user_data)
{
  GtkWidget *window;
  GtkWidget *button;
  GtkWidget *button_box;

  window = gtk_application_window_new (app);
  gtk_window_set_title (GTK_WINDOW (window), "Window");
  gtk_window_set_default_size (GTK_WINDOW (window), 200, 200);

  button_box = gtk_button_box_new (GTK_ORIENTATION_HORIZONTAL);
  gtk_container_add (GTK_CONTAINER (window), button_box);

  button = gtk_button_new_with_label ("Hello World");
  g_signal_connect (button, "clicked", G_CALLBACK (print_hello), NULL);
  g_signal_connect_swapped (button, "clicked", G_CALLBACK (gtk_widget_destroy), window);
  gtk_container_add (GTK_CONTAINER (button_box), button);

  gtk_widget_show_all (window);
}

int
main (int    argc,
      char **argv)
{
  GtkApplication *app;
  int status;

  app = gtk_application_new ("org.gtk.example", G_APPLICATION_DEFAULT_FLAGS);
  g_signal_connect (app, "activate", G_CALLBACK (activate), NULL);
  status = g_application_run (G_APPLICATION (app), argc, argv);
  g_object_unref (app);

  return status;
}
```

`Makefile`

```makefile
PROG = gtk_hello_world
SRCS = gtk_hello_world.c

CLEANFILES = $(PROG)

# Add / change option in CFLAGS and LDFLAGS
CFLAGS += -Wall $(shell pkg-config --cflags gtk+-3.0)
LDFLAGS += $(shell pkg-config --libs gtk+-3.0)

all: $(PROG)

$(PROG): $(SRCS)
	$(CC) -o $@ $^ $(CFLAGS) $(LDFLAGS)

clean:
	rm -f $(CLEANFILES) $(patsubst %.c,%.o, $(SRCS))
```

```bash
make

# /media/dev/rootfs/usr/local
/media/dev/userfs

sudo cp ~/STM32MPU_workspace/Developer-Package/stm32mp1-openstlinux-24.06.26/sources/gtk_hello_world_example/gtk_hello_world .

# Must remove SDCARD safely
sudo eject /dev/sdb


# Push this binary onto the board (Ethernet connection needed)
scp app root@192.168.50.96:/usr/local


# Board $>
cd /usr/local/
su -l weston -c "/usr/local/gtk_hello_world"
```

scarthgap

```bash
mkdir yocto
pushd yocto
git clone git://git.yoctoproject.org/poky.git
pushd poky
git checkout -t origin/scarthgap -b scarthgap-local
git branch
popd

mkdir Distribution-Package
pushd Distribution-Package

repo init -u https://github.com/STMicroelectronics/oe-manifest.git -b refs/tags/openstlinux-6.6-yocto-scarthgap-mpu-v24.11.06
repo sync

sudo apt install gcc-multilib libegl1-mesa libgmp-dev libmpc-dev libsdl1.2-dev pylint python3-git python3-jinja2 python3-pip socat xterm zstd bsdmainutils git-lfs

# ~/stm32mp/yocto/Distribution-Package/build-openstlinuxweston-stm32mp1
DISTRO=openstlinux-weston MACHINE=stm32mp1 source layers/meta-st/scripts/envsetup.sh

bitbake st-image-weston

tmp-glibc/deploy/images/stm32mp1/scripts/create_sdcard_from_flashlayout.sh tmp-glibc/deploy/images/stm32mp1/flashlayout_st-image-weston/optee/FlashLayout_sdcard_stm32mp135f-dk-optee.tsv

sudo dd if=tmp-glibc/deploy/images/stm32mp1/FlashLayout_sdcard_stm32mp135f-dk-optee.raw of=/dev/sdb bs=8M status=progress conv=fdatasync
```

### Distribution Package

```bash
pushd $STM32WKSP
mkdir dstpkg
pushd $STM32WKSP/dstpkg
repo init -u https://github.com/STMicroelectronics/oe-manifest.git -b refs/tags/openstlinux-6.1-yocto-mickledore-mpu-v24.06.26
repo sync
# MACHINE=stm32mp1
DISTRO=openstlinux-weston MACHINE=stm32mp13-disco source layers/meta-st/scripts/envsetup.sh

# /build-openstlinuxweston-stm32mp13-disco
bitbake st-image-weston

tmp-glibc/deploy/images/stm32mp13-disco/scripts/create_sdcard_from_flashlayout.sh tmp-glibc/deploy/images/stm32mp13-disco/flashlayout_st-image-weston/optee/FlashLayout_sdcard_stm32mp135f-dk-optee.tsv

sudo dd if=tmp-glibc/deploy/images/stm32mp13-disco/FlashLayout_sdcard_stm32mp135f-dk-optee.raw of=/dev/sdb bs=8M status=progress conv=fdatasync

layers/meta-st/meta-st-openstlinux/conf/distro/openstlinux-x11.conf
DISTRO=openstlinux-weston MACHINE=stm32mp13-disco source layers/meta-st/scripts/envsetup.sh
DISTRO=openstlinux-x11 MACHINE=stm32mp13-disco source layers/meta-st/scripts/envsetup.sh


git clone https://github.com/meta-flutter/meta-flutter.git ../layers/meta-flutter
git clone -b mickledore https://github.com/kraj/meta-clang ../layers/meta-clang
bitbake-layers add-layer ../layers/meta-flutter
bitbake-layers add-layer ../layers/meta-clang
```

#### dunfell x11

Ubuntu 18.04, Ubuntu 22.04 Not work

```bash
sudo apt 
sudo apt install open-vm-tools-desktop
# Reboot

sudo apt install -y bc build-essential chrpath cpio diffstat gawk python3-git python3-jinja2 python3-subunit texinfo wget gdisk libssl-dev gcc-arm-linux-gnueabihf

sudo apt install -y bc build-essential chrpath cpio diffstat gawk python-is-python3 python3-git python3-jinja2 python3-subunit texinfo wget gdisk libssl-dev gcc-arm-linux-gnueabihf lz4
sudo apt install -y bsdmainutils gcc-multilib libegl1-mesa libgmp-dev libmpc-dev libsdl1.2-dev pylint python3-pip socat xterm
sudo locale-gen en_US.UTF-8 

mkdir dstpkg
pushd $STM32WKSP/dstpkg
repo init -u https://github.com/STMicroelectronics/oe-manifest.git -b refs/tags/openstlinux-5.4-dunfell-mp1-20-06-24
DISTRO=openstlinux-x11 MACHINE=stm32mp1 source layers/meta-st/scripts/envsetup.sh

layers/openembedded-core/meta/recipes-support/iso-codes/iso-codes_4.4.bb
# SRC_URI = "git://salsa.debian.org/iso-codes-team/iso-codes.git;protocol=http;branch=main"

bitbake st-example-image-x11
```

### Github

#### scarthgap

```bash
sudo apt install gcc-multilib libegl1-mesa libgmp-dev libmpc-dev libsdl1.2-dev pylint python3-git python3-jinja2 python3-pip socat xterm zstd bsdmainutils git-lfs
sudo apt install chrpath diffstat gawk libssl-dev lz4 texinfo

mkdir yocto
pushd yocto
git clone git://git.yoctoproject.org/poky.git
pushd poky
git checkout -t origin/scarthgap -b scarthgap-local
git branch
popd

mkdir dstpkg
pushd dstpkg

repo init -u https://github.com/STMicroelectronics/oe-manifest.git -b refs/tags/openstlinux-6.6-yocto-scarthgap-mpu-v24.11.06
repo sync

# ~/stm32mpws/yocto/dstpkg/build-openstlinuxweston-stm32mp1
DISTRO=openstlinux-weston MACHINE=stm32mp13-disco source layers/meta-st/scripts/envsetup.sh
# DISTRO=openstlinux-weston MACHINE=stm32mp13-disco BSP_DEPENDENCY="layers/meta-qt5 layers/meta-st/meta-st-x-linux-qt" source layers/meta-st/scripts/envsetup.sh
# DISTRO=openstlinux-weston MACHINE=stm32mp1 source layers/meta-st/scripts/envsetup.sh

bitbake st-image-weston

tmp-glibc/deploy/images/stm32mp1/scripts/create_sdcard_from_flashlayout.sh tmp-glibc/deploy/images/stm32mp1/flashlayout_st-image-weston/optee/FlashLayout_sdcard_stm32mp135f-dk-optee.tsv

sudo dd if=tmp-glibc/deploy/images/stm32mp1/FlashLayout_sdcard_stm32mp135f-dk-optee.raw of=/dev/sdb bs=8M status=progress conv=fdatasync

sudo eject /dev/sdb

# board $>
ip addr show end0
ifconfig end0 192.168.0.111

### Not Work ###

git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git $STM32MPWS/bin/depot_tools
echo 'export PATH=~/stm32mpws/bin/depot_tools:$PATH' >> ~/.bashrc
source ~/.bashrc
gclient

pushd $STM32MPWS/yocto/dstpkg
mkdir flutter-engine
pushd flutter-engine
fetch flutter
pushd src
gclient sync
sudo apt-get install gcc-arm-linux-gnueabihf g++-arm-linux-gnueabihf
./flutter/tools/gn --linux-cpu=arm --target-os=linux
./flutter/tools/gn --no-goma --target-os linux --linux-cpu arm --arm-float-abi hard --embedder-for-target
ninja -C out/linux_debug_arm
./flutter/tools/gn \
  --target-os=linux \
  --linux-cpu=arm \
  --cc="arm-linux-gnueabihf-gcc" \
  --cxx="arm-linux-gnueabihf-g++" \
  --ar="arm-linux-gnueabihf-ar"
  
git clone https://github.com/flutter/engine.git ../engine
pushd $STM32MPWS/yocto/dstpkg/engine

git clone https://github.com/sony/flutter-elinux.git $STM32MPWS/yocto/dstpkg/flutter-elinux
echo "caaafc5604ee9172293eb84a381be6aadd660317" >  bin/internal/engine.version
echo 'export PATH=~/stm32mpws/yocto/dstpkg/flutter-elinux/bin:$PATH' >> ~/.bashrc
export PATH=$PATH:${flutter-elinux的下载路径}/bin:${flutter-elinux的下载路径}/flutter/bin
flutter-elinux create myapp

sudo apt install cmake
pushd ~
mkdir flutter-exp
cd flutter-exp
git clone https://github.com/llvm/llvm-project.git
cd llvm-project
mkdir build
cd build
#Build the TOOLCHAIN
cmake ../llvm \
    -DLLVM_TARGETS_TO_BUILD=ARM \
    -DLLVM_DEFAULT_TARGET_TRIPLE=arm-linux-gnueabihf \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=~/flutter-exp/sdk #/PATH/TO/YOUR/SDK
make # consider some -j 
make install

sudo apt install bison m4 flex
cd ~/flutter-exp
git clone git://sourceware.org/git/binutils-gdb.git
cd binutils-gdb
#/PATH/TO/YOUR/SDK
./configure --prefix="/home/dev/flutter-exp/sdk"   \
    --enable-ld                       \
    --target=arm-linux-gnueabihf
make
make install

cd ~/flutter-exp
cd llvm-project
cd build
cmake ../llvm/projects/libcxxabi \
    -DCMAKE_CROSSCOMPILING=True \
    -DLLVM_TARGETS_TO_BUILD=ARM \
    -DCMAKE_SYSROOT=/home/dev/flutter-exp/sdk/sysroot #NOTICE SYSROOT HERE! \
    -DCMAKE_INSTALL_PREFIX=/home/dev/flutter-exp/sdk \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_SYSTEM_NAME=Linux \
    -DCMAKE_SYSTEM_PROCESSOR=ARM \
    -DCMAKE_C_COMPILER=/home/dev/flutter-exp/sdk/bin/clang \
    -DCMAKE_CXX_COMPILER=/home/dev/flutter-exp/sdk/bin/clang++ \
    -DLIBCXX_ENABLE_SHARED=False \
    -DLIBCXXABI_ENABLE_EXCEPTIONS=False 

git clone -b scarthgap https://github.com/meta-flutter/meta-flutter.git ../layers/meta-flutter
git clone https://github.com/flutter/engine.git ..

git clone -b scarthgap https://github.com/kraj/meta-clang ../layers/meta-clang
git clone -b scarthgap https://github.com/meta-flutter/meta-flutter.git ../layers/meta-flutter

bitbake-layers add-layer ../layers/meta-clang
bitbake-layers add-layer ../layers/meta-flutter

```

#### kirkstone

```bash
sudo apt install -y bc build-essential chrpath cpio diffstat gawk python-is-python3 python3-git python3-jinja2 python3-subunit texinfo wget gdisk libssl-dev gcc-arm-linux-gnueabihf lz4
sudo locale-gen en_US.UTF-8

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

## Customize TF-A

# Download TF-A
devtool modify tf-a-stm32mp


# build-stm32mp1/workspace/sources/tf-a-stm32mp/fdts
# ram: stm32mp13-ddr3-1x4Gb-1066-binF.dtsi

# stm32mp135f-dk.dts
    ## Comment for test
	memory@c0000000 {
		device_type = "memory";
		reg = <0xc0000000 0x20000000>;
	};

pushd workspace/sources/tf-a-stm32mp
git diff
git status
git add . && git commit -m "comment will be the file name"
popd
bitbake-layers create-layer ../meta-custom-layer
devtool finish tf-a-stm32mp ../meta-custom-layer
bitbake-layers add-layer ../meta-custom-layer
bitbake-layers show-layers
bitbake core-image-minimal

# devtool finish again
# tf-a-stm32mp removed automatically
devtool status
rm -rf workspace/sources/tf-a-stm32mp
bitbake-layers remove-layer ../meta-custom-layer
devtool modify tf-a-stm32mp

pushd workspace/sources/tf-a-stm32mp

# stm32mp135f-dk.dts begin #
    // Comment for test
	memory@c0000000 {
		device_type = "memory";
		reg = <0xc0000000 0x20000000>;
	};
# stm32mp135f-dk.dts end #

git diff
git status
git add . && git commit -m "comment will be the file name"
popd
devtool finish tf-a-stm32mp ../meta-custom-layer
bitbake-layers add-layer ../meta-custom-layer
bitbake core-image-minimal

## Customize OP-TEE

# workspace/sources/optee-os-stm32mp/core/arch/arm/dts/stm32mp135f-dk.dts
devtool modify optee-os-stm32mp
pushd workspace/sources/optee-os-stm32mp
git add . && git commit -m "comment will be the file name"
popd
devtool finish optee-os-stm32mp ../meta-custom-layer
bitbake-layers add-layer ../meta-custom-layer

## Customize Uboot

devtool modify u-boot-stm32mp
pushd workspace/sources/u-boot-stm32mp
git add . && git commit -m "comment will be the file name"
popd
devtool finish u-boot-stm32mp ../meta-custom-layer
bitbake-layers add-layer ../meta-custom-layer

## Customize Linux kernel

devtool modify linux-stm32mp
bitbake linux-stm32mp -c menuconfig
# workspace/sources/linux-stm32mp/arch/arm/boot/dts/stm32mp135f-dk.dts
# workspace/sources/linux-stm32mp/drivers/net/can/m_can/m_can_platform.c
```

