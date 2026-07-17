# U-Boot

```bash
sudo apt install -y git build-essential gcc-aarch64-linux-gnu bison flex libssl-dev libgnutls28-dev

BOARD=board-virt
mkdir $BOARD
cd $BOARD
git clone https://source.denx.de/u-boot/u-boot.git
pushd u-boot

ls configs/qemu_*_defconfig
make ARCH=arm CROSS_COMPILE=aarch64-linux-gnu- qemu_arm64_defconfig

sudo apt-get install libncurses-dev

make menuconfig

# Partition Type  --->
#    [*] Enbale EFI GPT partition table
# Environment  --->
#    [*] Environment is in a EXT4 filesystem
#    [ ] Environment in flash memory
#    (virtio) Name of the block device for the environment 
#    (0:2) Device and partition for where to store the environemt in EXT4 partition

# Virtual board virt not support MMC
# MMC Host controller Support  --->
#    [*] MMC/SD/SDIO card support
# Environment  --->
#    (0x04000000) Environment offset
#    (0) mmc device number
#    (1) mmc partition number

make ARCH=arm CROSS_COMPILE=aarch64-linux-gnu- -j$(nproc)

popd

sudo apt install -y qemu-system-aarch64

# virt maybe not support SATA, SD, eMMC
qemu-img create -f qcow2 qemu-arm64.qcow2 16G
sudo modprobe nbd max_part=16
sudo qemu-nbd --connect=/dev/nbd0 qemu-arm64.qcow2

sudo parted /dev/nbd0 --script -- \
  mklabel gpt \
  mkpart primary fat32 1MiB 5MiB \
  mkpart primary ext4 64MiB 65MiB \
  mkpart primary ext4 128MiB 1128MiB \
  mkpart primary ext4 1128MiB 2128MiB \
  mkpart primary ext4 2128MiB 100%

sudo mkfs.vfat /dev/nbd0p1  # virt not support load u-boot from virto
sudo mkfs.ext4 -O ^metadata_csum,^64bit /dev/nbd0p2 # ENV file
sudo mkfs.ext4 /dev/nbd0p3  # System A
sudo mkfs.ext4 /dev/nbd0p4  # System B
sudo mkfs.ext4 /dev/nbd0p5  # Data

sudo parted /dev/nbd0 print

sudo qemu-nbd --disconnect /dev/nbd0
sudo modprobe -r nbd

qemu-system-aarch64 -M virt -cpu cortex-a57 -smp 2 -m 512M -nographic \
  -bios u-boot/u-boot.bin \
  -drive file=qemu-arm64.qcow2,if=virtio,format=qcow2

# At u-boot
=> saveenv
=> ext4ls virtio 0:2
            ./
            ../
            lost+found/
   262144   uboot.env

0 file(s), 3 dir(s)

# Open new console to close qemu at u-boot
kill -9 $(pgrep -f "qemu-system-aarch64")
```

Maybe not support SDcard

```bash
qemu-img create -f raw sdcard.img 16G
ls -lh sdcard.img # 16G
sudo losetup --show -f sdcard.img
# Example: /dev/loop10
LOOP=/dev/loop10
losetup -a
lsblk
ls -l /dev/loop10*

sudo parted ${LOOP} mklabel gpt
sudo parted ${LOOP} mkpart primary 1MiB 5MiB    # u-boot
sudo parted ${LOOP} mkpart primary 64MiB 65MiB  # env
sudo parted ${LOOP} mkpart primary 128MiB 1128MiB  # system A
sudo parted ${LOOP} mkpart primary 1128MiB 2128MiB  # System B
sudo parted ${LOOP} mkpart primary 2128MiB 100%  # data

sudo mkfs.vfat /dev/loop10p1  # 
sudo mkfs.ext4 -O ^metadata_csum,^64bit /dev/loop10p2
sudo mkfs.ext4 /dev/loop10p3  # System A
sudo mkfs.ext4 /dev/loop10p4  # System B
sudo mkfs.ext4 /dev/loop10p5  # Data

sudo umount /dev/loop10p1
sudo umount /dev/loop10p2
sudo umount /dev/loop10p3
sudo umount /dev/loop10p4
sudo umount /dev/loop10p5

sudo losetup -d ${LOOP}

# check part
parted sdcard.img
print
quit

dd if=u-boot/u-boot.bin of=sdcard.img bs=1M seek=1 conv=notrunc

qemu-system-aarch64 -M virt -cpu cortex-a57 -m 2048M -nographic \
   -bios u-boot/u-boot.bin \
   -device sdhci-pci \
   -drive file=sdcard.img,if=none,format=raw,id=sd \
  -device sd-card,drive=sd
```

## Test saveenv

```bash
setenv test_var hello
printenv test_var
saveenv
reset
printenv test_var
```

## Clean nhd & loop

```bash
for dev in /dev/nbd*; do
  sudo nbd-client -d $dev
done

for dev in /dev/loop*; do
  sudo losetup -d $dev
done
```

