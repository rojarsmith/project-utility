

# T-firefly ROC-RK3568-PC SE

SBC 4G+32G

2025 TWD 3417 USD 105

Shipping List: 12V2A power adapter, Type-c, 2.4G/5G dual band

Standard 2G+32G

2025 TWD 2733 USD 84

4G+128G MOQ 1000

2025 USD 107

8G+128G MOQ 1000

2025 USD 127

Build Number: 
rk3568_firefly_roc_pc_se-userdebug 11 RD2A.211001.002
eng.lwy.20230721.155311 release-keys

## concept

**What is the design concept of this SDK? **

> **Allow developers to quickly obtain a complete and corresponding version of the Android development source code environment "offline", and can also apply the latest official updates or fixes of Firefly. **

Its design is like: "Provide a compressed source code package + an updater", so that you don't have to download Git repositories one by one from the Internet, you can use it directly, update it, and it is not easy to make mistakes in the version.

## build

Disable Memory integrity, Local Security Authority protection

300GB Storage

ubuntu 18.04

```bash
sudo apt-get install git gnupg flex bison gperf libsdl1.2-dev \
libesd-java libwxgtk3.0-dev squashfs-tools build-essential zip curl \
libncurses5-dev zlib1g-dev pngcrush schedtool libxml2 libxml2-utils \
xsltproc lzop libc6-dev schedtool g++-multilib lib32z1-dev lib32ncurses5-dev \
lib32readline-dev gcc-multilib libswitch-perl libssl-dev unzip zip device-tree-compiler \
liblz4-tool python-pyelftools python3-pyelftools p7zip-full openssh-server -y

# Host name
sudo systemctl enable avahi-daemon
sudo systemctl start avahi-daemon

# sftp
mkdir ~/proj
mv Firefly-RK356X_Android11.0_git_20210824.7z.*  ~/proj
cd ~/proj/
7z x ./Firefly-RK356X_Android11.0_git_20210824.7z.001 -oRK356X_Android11.0
cd ./RK356X_Android11.0
git reset --hard

cd ~/proj/RK356X_Android11.0

# From GitLab
git clone https://gitlab.com/TeeFirefly/rk356x-android11-bundle.git .bundle
# From local
7z x ~/android/rk356x-android11-bundle.7z.001  -r -o. && mv rk356x-android11-bundle/ .bundle/

.bundle/update
git rebase FETCH_HEAD

# HDMI
./FFTools/make.sh -d rk3568-firefly-roc-pc-se -j8 -l rk3568_firefly_roc_pc_se-userdebug
./FFTools/mkupdate/mkupdate.sh -l rk3568_firefly_roc_pc_se-userdebug

$(call inherit-product-if-exists, vendor/partner_gms/products/gms.mk)
/rk3568_firefly_roc_pc_se/rk3568_firefly_roc_pc_se.mk
$(call inherit-product, vendor/partner_gms/products/gms.mk)

GSF ID
3BAD6F475AE7457C
https://www.rapidtables.com/convert/number/hex-to-decimal.html?x=3BAD6F475AE7457C
4300215571467158908

4300215571467158908

g.co/AndroidGMSContact
g.co/AndroidDeviceRegistration
```

## adb

```bash
adb devices
adb root
adb shell # The # symbol at the beginning is the root state
adb shell dumpsys cpuinfo
adb shell monkey # stress test
adb reboot recovery
adb reboot loader # No screen
adb logcat | grep BootAnimation
```

## fetch doc

```bash
wget --mirror --convert-links --adjust-extension --page-requisites --no-parent https://wiki.t-firefly.com/zh_CN/ROC-RK3568-PC-SE/index.html
```

## bench

```yaml
Geekbench 6:
    CPU:
        Single-Core Source: 182
        Multi-Core Source: 436
        RK3399: 653
        Samsung Exynos 1380 @ 2.0GHz: 2770 
        Qualcomm snapdragon 860 @ 1.8GHz: 2542
    GPU API:
        Open CL: 412
        Vulkan: crash
Youtube:
    1080p60: pass
    1440p60: pass
    2160p60: crash
```

## apks

```yaml
package:com.android.cts.priv.ctsshim
package:com.google.android.youtube
package:com.android.internal.display.cutout.emulation.corner
package:com.android.internal.display.cutout.emulation.double
package:com.android.providers.telephony
package:com.android.dynsystem
package:com.android.theme.color.amethyst
package:com.android.theme.icon.pebble
package:com.android.providers.calendar
package:com.android.providers.media
package:com.firefly.devicetest
package:com.google.android.onetimeinitializer
package:com.google.android.ext.shared
package:com.android.internal.systemui.navbar.gestural_wide_back
package:com.android.theme.color.sand
package:com.android.wallpapercropper
package:com.android.theme.icon.vessel
package:com.android.theme.color.cinnamon
package:com.android.theme.icon_pack.victor.settings
package:com.android.theme.icon_pack.rounded.systemui
package:com.android.rockchip_test.camera2
package:com.android.theme.icon.taperedrect
package:com.evozi.deviceid
package:com.android.documentsui
package:com.android.externalstorage
package:com.android.htmlviewer
package:com.android.companiondevicemanager
package:com.android.mms.service
package:com.android.providers.downloads
package:com.android.theme.icon_pack.rounded.android
package:com.toralabs.apkextractor
package:com.android.theme.icon_pack.victor.systemui
package:com.android.theme.icon_pack.circular.themepicker
package:com.google.android.configupdater
package:com.android.soundrecorder
package:com.android.theme.color.tangerine
package:com.android.providers.downloads.ui
package:com.android.vending
package:com.android.pacprocessor
package:com.android.simappdialog
package:com.android.networkstack
package:com.android.theme.color.aquamarine
package:com.android.internal.display.cutout.emulation.hole
package:com.android.internal.display.cutout.emulation.tall
package:com.android.modulemetadata
package:com.android.certinstaller
package:com.rockchip.overlay.pinnerservice
package:com.android.theme.color.black
package:com.android.theme.color.green
package:com.android.theme.color.ocean
package:com.android.theme.color.space
package:com.android.internal.systemui.navbar.threebutton
package:android.rockchip.update.service
package:android
package:com.android.camera2
package:com.android.theme.icon_pack.rounded.launcher
package:com.android.theme.icon_pack.kai.settings
package:com.android.egg
package:com.android.mtp
package:com.android.nfc
package:com.android.launcher3
package:com.android.backupconfirm
package:com.google.android.deskclock
package:com.android.statementservice
package:com.google.android.overlay.gmsconfig.common
package:com.android.theme.icon_pack.sam.settings
package:com.android.settings.intelligence
package:com.android.calendar
package:com.android.internal.systemui.navbar.gestural_extra_wide_back
package:com.android.theme.icon_pack.kai.themepicker
package:com.google.android.setupwizard
package:com.android.providers.settings
package:com.android.sharedstoragebackup
package:com.android.theme.icon_pack.victor.launcher
package:com.android.printspooler
package:com.android.theme.icon_pack.filled.settings
package:com.android.dreams.basic
package:com.android.theme.icon_pack.kai.systemui
package:com.android.rk
package:com.android.se
package:com.android.inputdevices
package:com.google.android.apps.wellbeing
package:com.google.android.dialer
package:com.android.bips
package:com.android.theme.icon_pack.circular.settings
package:com.google.android.overlay.gmsconfig.comms
package:com.android.musicfx
package:com.android.theme.icon_pack.sam.systemui
package:com.google.android.webview
package:com.android.theme.icon.teardrop
package:com.google.android.contacts
package:com.android.server.telecom
package:com.google.android.syncadapters.contacts
package:com.firefly.technicalcase
package:com.android.theme.icon_pack.rounded.themepicker
package:com.android.keychain
package:com.android.gallery3d
package:com.android.theme.icon_pack.filled.systemui
package:com.google.android.packageinstaller
package:com.google.android.gms
package:com.google.android.gsf
package:com.google.android.ims
package:com.google.android.tts
package:android.ext.services
package:acr.browser.lightning
package:com.android.wifi.resources
package:com.google.android.gmsintegration
package:com.google.android.partnersetup
package:com.android.localtransport
package:com.google.android.overlay.gmsconfig.gsa
package:com.android.theme.icon_pack.sam.android
package:com.android.theme.font.notoserifsource
package:com.android.theme.icon_pack.filled.android
package:com.android.proxyhandler
package:com.android.internal.display.cutout.emulation.waterfall
package:com.android.theme.icon_pack.circular.systemui
package:com.android.inputmethod.latin
package:com.google.android.feedback
package:com.google.android.printservice.recommendation
package:com.android.theme.icon_pack.kai.android
package:com.android.managedprovisioning
package:com.android.networkstack.tethering
package:com.android.soundpicker
package:com.android.dreams.phototable
package:com.firefly.fireflyapi2demo
package:com.android.theme.icon_pack.kai.launcher
package:com.android.smspush
package:com.android.wallpaper.livepicker
package:com.ytheekshana.deviceinfo
package:com.cghs.stresstest
package:com.firefly.fireflyapi2service
package:com.android.theme.icon_pack.sam.launcher
package:com.android.theme.icon.squircle
package:com.tchip.testscheduleonoff
package:com.android.theme.icon_pack.victor.android
package:com.android.storagemanager
package:com.android.theme.color.palette
package:com.android.bookmarkprovider
package:com.android.settings
package:com.android.theme.icon_pack.filled.launcher
package:com.primatelabs.geekbench6
package:com.android.networkstack.permissionconfig
package:com.android.calculator2
package:com.google.android.projection.gearhead
package:com.android.cts.ctsshim
package:com.android.theme.color.carbon
package:com.android.theme.icon_pack.circular.launcher
package:com.android.vpndialogs
package:com.android.music
package:com.android.phone
package:com.android.shell
package:com.android.theme.icon_pack.filled.themepicker
package:com.android.wallpaperbackup
package:com.android.providers.blockednumber
package:com.android.providers.userdictionary
package:com.android.providers.media.module
package:com.android.hotspot2.osulogin
package:com.google.android.gms.location.history
package:com.android.internal.systemui.navbar.gestural
package:com.android.location.fused
package:com.android.theme.icon_pack.victor.themepicker
package:com.android.theme.color.orchid
package:com.android.systemui
package:com.android.theme.color.purple
package:com.android.bluetoothmidiservice
package:com.android.permissioncontroller
package:com.android.traceur
package:com.android.theme.icon_pack.sam.themepicker
package:com.android.bluetooth
package:com.android.wallpaperpicker
package:com.android.providers.contacts
package:com.android.captiveportallogin
package:com.android.theme.icon.roundedrect
package:android.rk.RockVideoPlayer
package:com.android.internal.systemui.navbar.gestural_narrow_back
package:com.android.theme.icon_pack.rounded.settings
package:com.google.android.inputmethod.latin
package:android.auto_generated_rro_vendor__
package:com.android.theme.icon_pack.circular.android
package:com.google.android.apps.restore
```

`adb shell pm list packages -3`

```yaml
package:com.google.android.youtube
package:com.evozi.deviceid
package:com.toralabs.apkextractor
package:com.ytheekshana.deviceinfo
package:com.primatelabs.geekbench6
```

## modify

### List

1. Boot Logo

```bash
# Boot animation
device/rockchip/common/bootanimation.zip

# desk screen
device/rockchip/rk356x/overlay/frameworks/base/core/res/res/drawable-nodpi/default_wallpaper.jpg
```

## 
