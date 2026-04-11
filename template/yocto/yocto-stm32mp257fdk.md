# Yocto - STM32MP257F-DK

A 500GB hard drive, 24GB real ram should be provided for Android.

The official OpenSTLinux defaults support PCAP Touch IC with common USB interfaces, using Type-A.

## Parameter

Run each time.

```bash
STCPV=2.22.0 # Version of Cube Programmer
STWSV=$HOME/STM32MPU_workspace
STECOF=STM32MPU-Ecosystem-v6.2.0
BUSBIP=192.168.7.1 # Board USB Net IP
```

## Starter Package

```bash
mkdir $HOME/STM32MPU_workspace
cd $HOME/STM32MPU_workspace

# May cost long time in vm
wget -q www.google.com && echo "Internet access over HTTP/HTTPS is OK !" || echo "No internet access over HTTP/HTTPS ! You may need to set up a proxy."

mkdir $STWSV/STM32MPU-Tools
mkdir $STWSV/STM32MPU-Tools/STM32CubeProgrammer-$STCPV
mkdir $STWSV/tmp
cd $STWSV/tmp

unzip SetupSTM32CubeProgrammer_linux_64.zip
./SetupSTM32CubeProgrammer-$STCPV.linux

export PATH=/home/srv/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin:$PATH

sudo apt-get install libusb-1.0-0

cd $HOME/STMicroelectronics/STM32Cube/STM32CubeProgrammer/Drivers/rules

sudo cp *.* /etc/udev/rules.d/

STM32_Programmer_CLI -l usb
# DFU Interface
# Product ID: DFU in HS Mode @Device ID /0x505, @Revision ID /0x2000

STM32_Programmer_CLI --h

cd $STWSV
mkdir $STWSV/$STECOF
mkdir $STWSV/$STECOF/Starter-Package
cd $STWSV/$STECOF/Starter-Package

tar xvf FLASH-stm32mp2-openstlinux-6.6-yocto-scarthgap-mpu-v26.02.18.tar.gz

# Open STM32 Cube Programmer

# Load
$STWSV/$STECOF/Starter-Package/stm32mp2-openstlinux-6.6-yocto-scarthgap-mpu-v26.02.18/images/stm32mp2/flashlayout_st-image-weston/optee/FlashLayout_sdcard_stm32mp257f-dk-optee.tsv

# Binaries path
/home/srv/STM32MPU_workspace/STM32MPU-Ecosystem-v6.2.0/Starter-Package/stm32mp2-openstlinux-6.6-yocto-scarthgap-mpu-v26.02.18/images/stm32mp2

# Download cost long time, USB3.0 cost 30 minutes
# If the download fails, try entering DFU mode on the MCU M33 and then exiting
# Change DIP after download

sudo apt-get install minicom

# Type-C must 5A
# Connect STLINK-V3 to vmware

ls /dev/ttyACM*
minicom -D /dev/ttyACM0

### Board >

# Distribution specific
cat /etc/build

# System information
uname -a

# GCC version
cat /proc/version

# Disk
df -h

ip addr show usb0 # USB Gadget Ethernet

# Time error, apt cannot function
sudo apt update
date -s "2026-04-02 07:39:00"

sudo apt install openssh
vi /etc/ssh/sshd_config
# PermitRootLogin prohibit-password => PermitRootLogin yes
# PermitEmptyPasswords no => PermitEmptyPasswords yes

### PC >

ssh root@$BUSBIP
```

## Developer Package

```bash
sudo apt-get install gawk wget git git-lfs diffstat unzip texinfo gcc-multilib  chrpath socat cpio python3 python3-pip python3-pexpect xz-utils debianutils iputils-ping python3-git python3-jinja2 libsdl1.2-dev pylint xterm bsdmainutils libusb-1.0-0 bison flex
sudo apt-get install libssl-dev libgmp-dev libmpc-dev lz4 zstd

# Ubuntu 22.04 only
sudo apt install libegl1-mesa

sudo apt-get install build-essential libncurses-dev libyaml-dev libssl-dev

sudo apt-get install coreutils bsdmainutils sed curl bc lrzsz corkscrew cvs subversion mercurial nfs-common nfs-kernel-server libarchive-zip-perl dos2unix texi2html libxml2-utils

# Set python3 as default
sudo apt install python-is-python3

# Package for repo
mkdir ~/bin
export REPO=$(mktemp /tmp/repo.XXXXXXXXX)
curl -o ${REPO} https://storage.googleapis.com/git-repo-downloads/repo
gpg --recv-keys 8BB9AD793E8E6153AF0F9A4416530D5E920F5C65
curl -s https://storage.googleapis.com/git-repo-downloads/repo.asc | gpg --verify - ${REPO} && install -m 755 ${REPO} ~/bin/repo
# Repo not found
printf '\nexport PATH="~/bin:$PATH"\n' >> ~/.bashrc && source ~/.bashrc

echo 'options mmc_block perdev_minors=16' > /tmp/mmc_block.conf
sudo mv /tmp/mmc_block.conf /etc/modprobe.d/mmc_block.conf

mkdir $STWSV/$STECOF/Developer-Package
cd $STWSV/$STECOF/Developer-Package

tar xvf SDK-x86_64-stm32mp2-openstlinux-6.6-yocto-scarthgap-mpu-v26.02.18.tar.gz

chmod +x stm32mp2-openstlinux-6.6-yocto-scarthgap-mpu-v26.02.18/sdk/st-image-weston-openstlinux-weston-stm32mp2.rootfs-x86_64-toolchain-5.0.15-openstlinux-6.6-yocto-scarthgap-mpu-v26.02.18.sh

./stm32mp2-openstlinux-6.6-yocto-scarthgap-mpu-v26.02.18/sdk/st-image-weston-openstlinux-weston-stm32mp2.rootfs-x86_64-toolchain-5.0.15-openstlinux-6.6-yocto-scarthgap-mpu-v26.02.18.sh -d $STWSV/$STECOF/Developer-Package/SDK

cd $STWSV/$STECOF/Developer-Package 
source SDK/environment-setup-cortexa35-ostl-linux

echo $ARCH

echo $CROSS_COMPILE

$CC --version

echo $OECORE_SDK_VERSION

mkdir $STWSV/$STECOF/Developer-Package/stm32mp2-openstlinux-26.02.18
mkdir $STWSV/$STECOF/Developer-Package/stm32mp2-openstlinux-26.02.18/sources

mkdir $STWSV/$STECOF/Developer-Package/stm32mp2-openstlinux-26.02.18/sources/gtk_hello_world_example/
cd $STWSV/$STECOF/Developer-Package/stm32mp2-openstlinux-26.02.18/sources/gtk_hello_world_example/
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

scp gtk_hello_world root@$BUSBIP:/usr/local

### Board >

cd /usr/local/
su -l weston -c "/usr/local/gtk_hello_world"

### PC >

cd $STWSV/$STECOF/Developer-Package
source SDK/environment-setup-cortexa35-ostl-linux

tar xvf SOURCES-stm32mp-openstlinux-6.6-yocto-scarthgap-mpu-v26.02.18.tar.gz

cd stm32mp-openstlinux-6.6-yocto-scarthgap-mpu-v26.02.18/sources/ostl-linux/linux-stm32mp-6.6.116-stm32mp-r3-r0

tar xvf linux-6.6.116.tar.xz

cd linux-6.6.116
for p in `ls -1 ../*.patch`; do patch -p1 < $p; done

export OUTPUT_BUILD_DIR=$PWD/../build
mkdir -p ${OUTPUT_BUILD_DIR}

make O="${OUTPUT_BUILD_DIR}" defconfig fragment*.config

for f in `ls -1 ../fragment*.config`; do scripts/kconfig/merge_config.sh -m -r -O ${OUTPUT_BUILD_DIR} ${OUTPUT_BUILD_DIR}/.config $f; done

(yes '' || true) |  make oldconfig O="${OUTPUT_BUILD_DIR}"

make -j$(nproc) Image.gz vmlinux dtbs O="${OUTPUT_BUILD_DIR}"
export IMAGE_KERNEL="Image.gz"

make -j$(nproc) modules O="${OUTPUT_BUILD_DIR}"

make INSTALL_MOD_PATH="${OUTPUT_BUILD_DIR}/install_artifact" modules_install O="${OUTPUT_BUILD_DIR}"

mkdir -p ${OUTPUT_BUILD_DIR}/install_artifact/boot/

cp ${OUTPUT_BUILD_DIR}/arch/${ARCH}/boot/${IMAGE_KERNEL} ${OUTPUT_BUILD_DIR}/install_artifact/boot/
find ${OUTPUT_BUILD_DIR}/arch/${ARCH}/boot/dts/ -name 'st*.dtb' -exec cp '{}' ${OUTPUT_BUILD_DIR}/install_artifact/boot/ \;

cd ${OUTPUT_BUILD_DIR}/install_artifact
scp -r boot/* root@$BUSBIP:/boot/

rm lib/modules/6.6.116/build

find . -name "*.ko" | xargs $STRIP --strip-debug --remove-section=.comment --remove-section=.note --preserve-dates

scp -r lib/modules/* root@$BUSBIP:/lib/modules

### Board >

/sbin/depmod -a

sync

reboot

# Using the Linux console, check that there is no log information when the display driver is probed
dmesg | grep -i modified

### PC >

cd $STWSV/$STECOF/Developer-Package/stm32mp-openstlinux-6.6-yocto-scarthgap-mpu-v26.02.18/sources/ostl-linux/linux-stm32mp-6.6.116-stm32mp-r3-r0/linux-6.6.116
```

`./drivers/pinctrl/stm32/pinctrl-stm32.c`

```c
int stm32_pctl_probe(struct platform_device *pdev)
{
   [...]
   dev_info(dev, "Pinctrl STM32 initialized\n");
   dev_info(dev, "I modified a linux kernel device driver\n");
   [...]
}
```

```bash
make -j$(nproc) Image.gz O="${OUTPUT_BUILD_DIR}"

scp ${OUTPUT_BUILD_DIR}/arch/${ARCH}/boot/Image.gz root@$BUSBIP:/boot

###  Board >

reboot

dmesg | grep -i modified
# [    2.177180] stm32mp257-pinctrl soc@0:pinctrl@44240000: I modified a linux kernel device driver
# [    2.200008] stm32mp257-pinctrl soc@0:pinctrl@46200000: I modified a linux kernel device driver
```

## Flutter

```bash
sudo apt update
sudo apt install -y curl git unzip xz-utils zip cmake ninja-build pkg-config clang

cd $STWSV/$STECOF/Developer-Package 
source SDK/environment-setup-cortexa35-ostl-linux

echo "$CC"
echo "$CXX"
echo "$SDKTARGETSYSROOT"

pushd /opt
sudo git clone https://github.com/flutter/flutter.git -b stable
pushd flutter
git fetch --tags
git checkout 3.27.1
git describe --tags
popd
sudo chown -R $USER:$USER /opt/flutter
export PATH=/opt/flutter/bin:$PATH
flutter doctor
dart pub global activate flutter_elinux
export PATH="$HOME/.pub-cache/bin:$PATH"
popd
flutter --version

pushd /opt
sudo git clone https://github.com/sony/flutter-elinux.git
sudo chown -R $USER:$USER /opt/flutter-elinux
export PATH=$PATH:/opt/flutter-elinux/bin

flutter-elinux doctor
flutter-elinux devices
popd
flutter-elinux --version

mkdir -p "$OECORE_NATIVE_SYSROOT/bin"
ln -sf "$(command -v aarch64-ostl-linux-gcc)"  "$OECORE_NATIVE_SYSROOT/bin/clang"
ln -sf "$(command -v aarch64-ostl-linux-g++)" "$OECORE_NATIVE_SYSROOT/bin/clang++"

mkdir $STWSV/$STECOF/Developer-Package/stm32mp2-openstlinux-26.02.18/sources/flutter_demo_1/
cd $STWSV/$STECOF/Developer-Package/stm32mp2-openstlinux-26.02.18/sources/flutter_demo_1/

# Recreate eLinux scaffolding
flutter-elinux create .

vi lib/main.dart

# Disable Performance Overlay
showPerformanceOverlay: false,

# Clean build
rm -rf build
rm -rf elinux/flutter/ephemeral

# Target sysroot build
flutter-elinux build elinux \
  --target-arch=arm64 \
  --target-sysroot="$SDKTARGETSYSROOT" \
  --target-toolchain="$OECORE_NATIVE_SYSROOT"

ssh root@$BUSBIP 'rm -rf /usr/local/flutter_demo_1'

scp -r build/elinux/arm64/release/bundle root@$BUSBIP:/usr/local/flutter_demo_1

### Board >

cd /usr/local/flutter_demo_1/flutter_demo_1

export LD_LIBRARY_PATH=$PWD/lib:$LD_LIBRARY_PATH

/usr/local/flutter_demo_1/flutter_demo_1 --bundle=$PWD --fullscreen

# Backup
tar -czvf flutter_demo_1_$(date +%Y%m%d_%H%M%S).tar.gz \
-C $STWSV/$STECOF/Developer-Package/stm32mp2-openstlinux-26.02.18/sources \
flutter_demo_1
tar -C /opt -czf flutter-full.tar.gz flutter
tar -C /opt -czf flutter-elinux-full.tar.gz flutter-elinux
```

`main.dart`

```dart
import 'dart:async';
import 'dart:math' as math;
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';

void main() {
  runApp(const EdtFlutterDemoApp());
}

class EdtFlutterDemoApp extends StatelessWidget {
  const EdtFlutterDemoApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'EDT Flutter Demo 1',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: const DemoShell(),
    );
  }
}

class DemoShell extends StatefulWidget {
  const DemoShell({super.key});

  @override
  State<DemoShell> createState() => _DemoShellState();
}

class _DemoShellState extends State<DemoShell> with TickerProviderStateMixin {
  int _currentIndex = 0;
  double _fps = 0.0;
  int _frameCount = 0;
  Duration _lastSample = Duration.zero;
  late final Ticker _ticker;

  final List<Widget> _pages = const <Widget>[
    ComponentsPage(),
    ChartPage(),
    NavigationDemoPage(),
    ThreeDTestPage(),
    AINpuTestPage(),
    StressTestPage(),
    VideoPlayerDemoPage(),
    ParkourGamePage(),
  ];

  @override
  void initState() {
    super.initState();
    _ticker = createTicker(_onTick)..start();
  }

  void _onTick(Duration elapsed) {
    _frameCount++;
    final Duration diff = elapsed - _lastSample;
    if (diff >= const Duration(seconds: 1)) {
      final double seconds = diff.inMicroseconds / 1000000.0;
      if (mounted) {
        setState(() {
          _fps = _frameCount / seconds;
          _frameCount = 0;
          _lastSample = elapsed;
        });
      }
    }
  }

  @override
  void dispose() {
    _ticker.dispose();
    super.dispose();
  }

  String get _pageTitle {
    switch (_currentIndex) {
      case 0:
        return 'Controls';
      case 1:
        return 'Live Chart';
      case 2:
        return 'Pages';
      case 3:
        return '3D Test';
      case 4:
        return 'AI NPU Test';
      case 5:
        return 'Stress Test';
      case 6:
        return 'Video Player';
      case 7:
        return 'Parkour Game';
      default:
        return 'Demo';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('EDT Flutter Demo 1 - $_pageTitle'),
      ),
      body: Stack(
        children: <Widget>[
          Positioned.fill(
            child: Padding(
              padding: const EdgeInsets.only(bottom: 76),
              child: IndexedStack(
                index: _currentIndex,
                children: _pages,
              ),
            ),
          ),
          Positioned(
            right: 16,
            bottom: 16,
            child: IgnorePointer(
              child: SafeArea(
                child: Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 16,
                    vertical: 12,
                  ),
                  decoration: BoxDecoration(
                    color: Colors.black.withOpacity(0.72),
                    borderRadius: BorderRadius.circular(14),
                    border: Border.all(color: Colors.white24),
                    boxShadow: <BoxShadow>[
                      BoxShadow(
                        color: Colors.black.withOpacity(0.2),
                        blurRadius: 10,
                        offset: const Offset(0, 4),
                      ),
                    ],
                  ),
                  child: Text(
                    'FPS ${_fps.toStringAsFixed(1)}',
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 22,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _currentIndex,
        onDestinationSelected: (int index) {
          setState(() => _currentIndex = index);
        },
        destinations: const <NavigationDestination>[
          NavigationDestination(
            icon: Icon(Icons.tune),
            label: 'Controls',
          ),
          NavigationDestination(
            icon: Icon(Icons.show_chart),
            label: 'Chart',
          ),
          NavigationDestination(
            icon: Icon(Icons.swap_horiz),
            label: 'Pages',
          ),
          NavigationDestination(
            icon: Icon(Icons.view_in_ar),
            label: '3D Test',
          ),
          NavigationDestination(
            icon: Icon(Icons.memory),
            label: 'AI NPU',
          ),
          NavigationDestination(
            icon: Icon(Icons.bolt),
            label: 'Stress',
          ),
          NavigationDestination(
            icon: Icon(Icons.ondemand_video),
            label: 'Video',
          ),
          NavigationDestination(
            icon: Icon(Icons.sports_esports),
            label: 'Game',
          ),
        ],
      ),
    );
  }
}

class PageHeader extends StatelessWidget {
  const PageHeader({
    super.key,
    required this.subtitle,
  });

  final String subtitle;

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.fromLTRB(16, 16, 16, 8),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          children: <Widget>[
            const Icon(Icons.developer_board, size: 32),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: <Widget>[
                  Text(
                    'EDT Flutter Demo 1',
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                  const SizedBox(height: 4),
                  Text(
                    subtitle,
                    style: Theme.of(context).textTheme.bodyMedium,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class ComponentsPage extends StatefulWidget {
  const ComponentsPage({super.key});

  @override
  State<ComponentsPage> createState() => _ComponentsPageState();
}

class _ComponentsPageState extends State<ComponentsPage>
    with SingleTickerProviderStateMixin {
  bool _switchValue = true;
  bool _checkboxValue = false;
  double _sliderValue = 35;
  String _dropdownValue = 'Option A';
  final TextEditingController _textController =
      TextEditingController(text: 'Hello EDT');
  late final TabController _tabController;

  final List<String> _dropdownItems = <String>[
    'Option A',
    'Option B',
    'Option C',
    'Option D',
  ];

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 3, vsync: this);
  }

  @override
  void dispose() {
    _textController.dispose();
    _tabController.dispose();
    super.dispose();
  }

  void _showInfoDialog() {
    showDialog<void>(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text('Dialog'),
          content: const Text(
            'This is a standard dialog in EDT Flutter Demo 1.',
          ),
          actions: <Widget>[
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('Close'),
            ),
          ],
        );
      },
    );
  }

  void _showSnackBar() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('This is a Snackbar message.'),
        duration: Duration(seconds: 2),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Column(
        children: <Widget>[
          const PageHeader(
            subtitle: 'Standard widgets, forms, selections, and actions.',
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            child: TabBar(
              controller: _tabController,
              tabs: const <Tab>[
                Tab(text: 'Inputs'),
                Tab(text: 'Actions'),
                Tab(text: 'Lists'),
              ],
            ),
          ),
          Expanded(
            child: TabBarView(
              controller: _tabController,
              children: <Widget>[
                _buildInputsTab(),
                _buildActionsTab(),
                _buildListsTab(),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildInputsTab() {
    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 12, 16, 96),
      children: <Widget>[
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              children: <Widget>[
                TextField(
                  controller: _textController,
                  decoration: const InputDecoration(
                    labelText: 'Text Input',
                    border: OutlineInputBorder(),
                  ),
                  onChanged: (_) => setState(() {}),
                ),
                const SizedBox(height: 16),
                DropdownButtonFormField<String>(
                  value: _dropdownValue,
                  decoration: const InputDecoration(
                    labelText: 'Dropdown',
                    border: OutlineInputBorder(),
                  ),
                  items: _dropdownItems
                      .map(
                        (String item) => DropdownMenuItem<String>(
                          value: item,
                          child: Text(item),
                        ),
                      )
                      .toList(),
                  onChanged: (String? value) {
                    if (value == null) return;
                    setState(() => _dropdownValue = value);
                  },
                ),
                const SizedBox(height: 16),
                Row(
                  children: <Widget>[
                    const Expanded(
                      child: Text(
                        'Slider',
                        style: TextStyle(fontWeight: FontWeight.bold),
                      ),
                    ),
                    Text(_sliderValue.toStringAsFixed(0)),
                  ],
                ),
                Slider(
                  min: 0,
                  max: 100,
                  value: _sliderValue,
                  onChanged: (double value) {
                    setState(() => _sliderValue = value);
                  },
                ),
                SwitchListTile(
                  value: _switchValue,
                  title: const Text('Enable Feature'),
                  subtitle: const Text('Standard switch control'),
                  onChanged: (bool value) {
                    setState(() => _switchValue = value);
                  },
                ),
                CheckboxListTile(
                  value: _checkboxValue,
                  title: const Text('Accept Selection'),
                  subtitle: const Text('Standard checkbox control'),
                  onChanged: (bool? value) {
                    setState(() => _checkboxValue = value ?? false);
                  },
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildActionsTab() {
    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 12, 16, 96),
      children: <Widget>[
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Wrap(
              spacing: 12,
              runSpacing: 12,
              children: <Widget>[
                ElevatedButton(
                  onPressed: _showInfoDialog,
                  child: const Text('Show Dialog'),
                ),
                FilledButton(
                  onPressed: _showSnackBar,
                  child: const Text('Show Snackbar'),
                ),
                OutlinedButton(
                  onPressed: () {},
                  child: const Text('Outlined Button'),
                ),
                TextButton(
                  onPressed: () {},
                  child: const Text('Text Button'),
                ),
                IconButton.filled(
                  onPressed: () {},
                  icon: const Icon(Icons.play_arrow),
                  tooltip: 'Play',
                ),
              ],
            ),
          ),
        ),
        const SizedBox(height: 8),
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: <Widget>[
                Text(
                  'Current Values',
                  style: Theme.of(context).textTheme.titleMedium,
                ),
                const SizedBox(height: 12),
                Text('Text: ${_textController.text}'),
                Text('Dropdown: $_dropdownValue'),
                Text('Slider: ${_sliderValue.toStringAsFixed(0)}'),
                Text('Feature Enabled: ${_switchValue ? "Yes" : "No"}'),
                Text('Selection Accepted: ${_checkboxValue ? "Yes" : "No"}'),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildListsTab() {
    return ListView.builder(
      padding: const EdgeInsets.fromLTRB(16, 12, 16, 96),
      itemCount: 8,
      itemBuilder: (BuildContext context, int index) {
        return Card(
          child: ListTile(
            leading: CircleAvatar(child: Text('${index + 1}')),
            title: Text('List Item ${index + 1}'),
            subtitle: const Text('Standard ListTile component'),
            trailing: const Icon(Icons.chevron_right),
            onTap: _showSnackBar,
          ),
        );
      },
    );
  }
}

class ChartPage extends StatefulWidget {
  const ChartPage({super.key});

  @override
  State<ChartPage> createState() => _ChartPageState();
}

class _ChartPageState extends State<ChartPage> {
  static const int maxPoints = 60;
  final math.Random _random = math.Random();
  final List<double> _values = List<double>.generate(60, (int i) {
    return 40 + math.sin(i / 6) * 20;
  });

  Timer? _timer;
  double _latestValue = 0;
  double _averageValue = 0;
  double _peakValue = 0;

  @override
  void initState() {
    super.initState();
    _recalculateStats();
    _timer = Timer.periodic(const Duration(milliseconds: 120), (_) {
      final double t = DateTime.now().millisecondsSinceEpoch / 1000.0;
      final double next = 50 +
          math.sin(t * 1.7) * 22 +
          math.cos(t * 0.9) * 12 +
          (_random.nextDouble() * 8 - 4);

      setState(() {
        _values.add(next.clamp(5, 95));
        if (_values.length > maxPoints) {
          _values.removeAt(0);
        }
        _recalculateStats();
      });
    });
  }

  void _recalculateStats() {
    _latestValue = _values.last;
    _averageValue =
        _values.reduce((double a, double b) => a + b) / _values.length;
    _peakValue = _values.reduce(math.max);
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Column(
        children: <Widget>[
          const PageHeader(
            subtitle: 'Real-time chart with simulated streaming data.',
          ),
          Expanded(
            child: ListView(
              padding: const EdgeInsets.fromLTRB(16, 12, 16, 96),
              children: <Widget>[
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: SizedBox(
                      height: 280,
                      child: RepaintBoundary(
                        child: CustomPaint(
                          painter: LiveChartPainter(values: _values),
                          child: const SizedBox.expand(),
                        ),
                      ),
                    ),
                  ),
                ),
                const SizedBox(height: 8),
                Row(
                  children: <Widget>[
                    Expanded(
                      child: _statCard(
                        context,
                        'Latest',
                        _latestValue.toStringAsFixed(1),
                        Icons.speed,
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: _statCard(
                        context,
                        'Average',
                        _averageValue.toStringAsFixed(1),
                        Icons.analytics,
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: _statCard(
                        context,
                        'Peak',
                        _peakValue.toStringAsFixed(1),
                        Icons.trending_up,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 12),
                const Card(
                  child: Padding(
                    padding: EdgeInsets.all(16),
                    child: Text(
                      'This chart uses simulated streaming data to keep the line moving continuously. '
                      'It is useful for testing rendering performance and UI responsiveness.',
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _statCard(
    BuildContext context,
    String label,
    String value,
    IconData icon,
  ) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 18),
        child: Column(
          children: <Widget>[
            Icon(icon, size: 28),
            const SizedBox(height: 8),
            Text(
              label,
              style: Theme.of(context).textTheme.labelLarge,
            ),
            const SizedBox(height: 6),
            Text(
              value,
              style: Theme.of(context).textTheme.titleLarge,
            ),
          ],
        ),
      ),
    );
  }
}

class LiveChartPainter extends CustomPainter {
  LiveChartPainter({required this.values});

  final List<double> values;

  @override
  void paint(Canvas canvas, Size size) {
    final Rect rect = Offset.zero & size;

    final Paint background = Paint()
      ..shader = const LinearGradient(
        colors: <Color>[
          Color(0xFF0E1A2B),
          Color(0xFF12263F),
        ],
        begin: Alignment.topCenter,
        end: Alignment.bottomCenter,
      ).createShader(rect);

    canvas.drawRRect(
      RRect.fromRectAndRadius(rect, const Radius.circular(12)),
      background,
    );

    final Paint gridPaint = Paint()
      ..color = Colors.white.withOpacity(0.12)
      ..strokeWidth = 1;

    for (int i = 1; i < 5; i++) {
      final double dy = size.height * i / 5;
      canvas.drawLine(Offset(0, dy), Offset(size.width, dy), gridPaint);
    }

    for (int i = 1; i < 6; i++) {
      final double dx = size.width * i / 6;
      canvas.drawLine(Offset(dx, 0), Offset(dx, size.height), gridPaint);
    }

    if (values.length < 2) return;

    final Path linePath = Path();
    final Path fillPath = Path();

    for (int i = 0; i < values.length; i++) {
      final double x = size.width * i / (values.length - 1);
      final double normalized = values[i] / 100.0;
      final double y = size.height - (normalized * size.height);

      if (i == 0) {
        linePath.moveTo(x, y);
        fillPath.moveTo(x, size.height);
        fillPath.lineTo(x, y);
      } else {
        linePath.lineTo(x, y);
        fillPath.lineTo(x, y);
      }
    }

    fillPath
      ..lineTo(size.width, size.height)
      ..close();

    final Paint fillPaint = Paint()
      ..shader = LinearGradient(
        colors: <Color>[
          Colors.lightBlueAccent.withOpacity(0.35),
          Colors.transparent,
        ],
        begin: Alignment.topCenter,
        end: Alignment.bottomCenter,
      ).createShader(rect);

    final Paint linePaint = Paint()
      ..color = Colors.lightBlueAccent
      ..strokeWidth = 3
      ..style = PaintingStyle.stroke;

    canvas.drawPath(fillPath, fillPaint);
    canvas.drawPath(linePath, linePaint);

    final double x = size.width;
    final double y = size.height - (values.last / 100.0 * size.height);

    final Paint pointPaint = Paint()..color = Colors.orangeAccent;
    canvas.drawCircle(Offset(x, y), 5, pointPaint);
  }

  @override
  bool shouldRepaint(covariant LiveChartPainter oldDelegate) {
    return true;
  }
}

class NavigationDemoPage extends StatelessWidget {
  const NavigationDemoPage({super.key});

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Column(
        children: <Widget>[
          const PageHeader(
            subtitle: 'Page switching, detail page, and common navigation flow.',
          ),
          Expanded(
            child: ListView(
              padding: const EdgeInsets.fromLTRB(16, 12, 16, 96),
              children: <Widget>[
                Card(
                  child: ListTile(
                    leading: const Icon(Icons.open_in_new),
                    title: const Text('Open Detail Page'),
                    subtitle: const Text('Push a new page with Navigator'),
                    trailing: const Icon(Icons.chevron_right),
                    onTap: () {
                      Navigator.of(context).push(
                        MaterialPageRoute<void>(
                          builder: (_) => const DetailDemoPage(),
                        ),
                      );
                    },
                  ),
                ),
                Card(
                  child: ListTile(
                    leading: const Icon(Icons.view_carousel),
                    title: const Text('Open PageView Demo'),
                    subtitle: const Text('Swipe between internal pages'),
                    trailing: const Icon(Icons.chevron_right),
                    onTap: () {
                      Navigator.of(context).push(
                        MaterialPageRoute<void>(
                          builder: (_) => const PageViewDemoPage(),
                        ),
                      );
                    },
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class DetailDemoPage extends StatelessWidget {
  const DetailDemoPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('EDT Flutter Demo 1 - Detail'),
      ),
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.fromLTRB(16, 16, 16, 96),
          children: const <Widget>[
            PageHeader(
              subtitle: 'This is a standard pushed page using Navigator.',
            ),
            Card(
              child: Padding(
                padding: EdgeInsets.all(16),
                child: Text(
                  'This page demonstrates a common mobile or embedded application navigation pattern.',
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class PageViewDemoPage extends StatefulWidget {
  const PageViewDemoPage({super.key});

  @override
  State<PageViewDemoPage> createState() => _PageViewDemoPageState();
}

class _PageViewDemoPageState extends State<PageViewDemoPage> {
  final PageController _controller = PageController();
  int _index = 0;

  final List<Color> _colors = <Color>[
    Colors.blue,
    Colors.green,
    Colors.deepOrange,
  ];

  void _goTo(int index) {
    _controller.animateToPage(
      index,
      duration: const Duration(milliseconds: 250),
      curve: Curves.easeInOut,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('EDT Flutter Demo 1 - Page ${_index + 1}'),
      ),
      body: Column(
        children: <Widget>[
          const PageHeader(
            subtitle: 'Swipe or tap buttons to switch pages.',
          ),
          Expanded(
            child: PageView.builder(
              controller: _controller,
              itemCount: 3,
              onPageChanged: (int index) {
                setState(() => _index = index);
              },
              itemBuilder: (BuildContext context, int index) {
                return Container(
                  margin: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: _colors[index],
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Center(
                    child: Text(
                      'EDT Flutter Demo 1\nPage ${index + 1}',
                      textAlign: TextAlign.center,
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 28,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                );
              },
            ),
          ),
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 0, 16, 96),
            child: Row(
              children: <Widget>[
                Expanded(
                  child: ElevatedButton(
                    onPressed: _index > 0 ? () => _goTo(_index - 1) : null,
                    child: const Text('Previous'),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: ElevatedButton(
                    onPressed: _index < 2 ? () => _goTo(_index + 1) : null,
                    child: const Text('Next'),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class ThreeDTestPage extends StatefulWidget {
  const ThreeDTestPage({super.key});

  @override
  State<ThreeDTestPage> createState() => _ThreeDTestPageState();
}

class _ThreeDTestPageState extends State<ThreeDTestPage>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 12),
    )..repeat();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Column(
        children: <Widget>[
          const PageHeader(
            subtitle:
                '3D performance demo with a rotating textured cube and sphere.',
          ),
          Expanded(
            child: Padding(
              padding: const EdgeInsets.fromLTRB(16, 12, 16, 96),
              child: Card(
                clipBehavior: Clip.antiAlias,
                child: AnimatedBuilder(
                  animation: _controller,
                  builder: (BuildContext context, Widget? child) {
                    return CustomPaint(
                      painter: ThreeDScenePainter(
                        time: _controller.value,
                      ),
                      child: const SizedBox.expand(),
                    );
                  },
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class ThreeDScenePainter extends CustomPainter {
  ThreeDScenePainter({required this.time});

  final double time;

  @override
  void paint(Canvas canvas, Size size) {
    final Rect rect = Offset.zero & size;
    final Paint bg = Paint()
      ..shader = const LinearGradient(
        begin: Alignment.topLeft,
        end: Alignment.bottomRight,
        colors: <Color>[
          Color(0xFF09111F),
          Color(0xFF0F1B31),
          Color(0xFF122747),
        ],
      ).createShader(rect);
    canvas.drawRect(rect, bg);

    final Paint gridPaint = Paint()
      ..color = Colors.white.withOpacity(0.06)
      ..strokeWidth = 1;
    for (double x = 0; x < size.width; x += 32) {
      canvas.drawLine(Offset(x, 0), Offset(x, size.height), gridPaint);
    }
    for (double y = 0; y < size.height; y += 32) {
      canvas.drawLine(Offset(0, y), Offset(size.width, y), gridPaint);
    }

    final Offset cubeCenter = Offset(size.width * 0.28, size.height * 0.55);
    final Offset sphereCenter = Offset(size.width * 0.72, size.height * 0.55);

    _drawCube(canvas, cubeCenter, size.shortestSide * 0.17);
    _drawSphere(canvas, sphereCenter, size.shortestSide * 0.16);

    final textStyle = TextStyle(
      color: Colors.white.withOpacity(0.85),
      fontSize: 18,
      fontWeight: FontWeight.w600,
    );

    final cubeTp = TextPainter(
      text: TextSpan(text: 'Cube', style: textStyle),
      textDirection: TextDirection.ltr,
    )..layout();
    cubeTp.paint(canvas, Offset(cubeCenter.dx - cubeTp.width / 2, 20));

    final sphereTp = TextPainter(
      text: TextSpan(text: 'Sphere', style: textStyle),
      textDirection: TextDirection.ltr,
    )..layout();
    sphereTp.paint(canvas, Offset(sphereCenter.dx - sphereTp.width / 2, 20));
  }

  void _drawCube(Canvas canvas, Offset center, double scale) {
    final double ax = time * math.pi * 2.0;
    final double ay = time * math.pi * 2.7;
    final double az = time * math.pi * 1.5;

    final List<_Vec3> vertices = <_Vec3>[
      _Vec3(-1, -1, -1),
      _Vec3(1, -1, -1),
      _Vec3(1, 1, -1),
      _Vec3(-1, 1, -1),
      _Vec3(-1, -1, 1),
      _Vec3(1, -1, 1),
      _Vec3(1, 1, 1),
      _Vec3(-1, 1, 1),
    ].map((v) => v.rotateX(ax).rotateY(ay).rotateZ(az)).toList();

    final List<List<int>> faces = <List<int>>[
      <int>[0, 1, 2, 3],
      <int>[4, 5, 6, 7],
      <int>[0, 1, 5, 4],
      <int>[2, 3, 7, 6],
      <int>[1, 2, 6, 5],
      <int>[0, 3, 7, 4],
    ];

    final List<_FaceData> faceData = <_FaceData>[];

    for (int i = 0; i < faces.length; i++) {
      final face = faces[i];
      final pts3 = face.map((idx) => vertices[idx]).toList();

      final normal = (pts3[1] - pts3[0]).cross(pts3[2] - pts3[0]).normalize();
      final light = _Vec3(0.4, -0.5, -1.0).normalize();
      final brightness = (normal.dot(light) * -1).clamp(0.15, 1.0);

      final avgZ = pts3.map((e) => e.z).reduce((a, b) => a + b) / pts3.length;

      final pts2 = pts3.map((v) => _project(v, center, scale)).toList();

      faceData.add(
        _FaceData(
          points: pts2,
          depth: avgZ,
          brightness: brightness,
          kind: i,
        ),
      );
    }

    faceData.sort((a, b) => a.depth.compareTo(b.depth));

    for (final face in faceData) {
      final path = Path()..moveTo(face.points.first.dx, face.points.first.dy);
      for (int i = 1; i < face.points.length; i++) {
        path.lineTo(face.points[i].dx, face.points[i].dy);
      }
      path.close();

      final Rect bounds = _boundsOf(face.points);

      final base1 = Color.lerp(
        const Color(0xFF1E88E5),
        const Color(0xFFFFC107),
        (face.kind % 6) / 5,
      )!;
      final base2 = Color.lerp(
        const Color(0xFF26C6DA),
        const Color(0xFFEF5350),
        ((face.kind + 2) % 6) / 5,
      )!;

      final shader = LinearGradient(
        begin: Alignment.topLeft,
        end: Alignment.bottomRight,
        colors: <Color>[
          _shade(base1, face.brightness),
          _shade(base2, face.brightness * 0.85),
        ],
      ).createShader(bounds);

      canvas.save();
      canvas.clipPath(path);

      canvas.drawPath(
        path,
        Paint()..shader = shader,
      );

      _drawTexturePattern(
        canvas,
        bounds,
        path,
        face.brightness,
        spacing: 12,
      );

      canvas.restore();

      canvas.drawPath(
        path,
        Paint()
          ..style = PaintingStyle.stroke
          ..strokeWidth = 1.5
          ..color = Colors.white.withOpacity(0.35),
      );
    }
  }

  void _drawSphere(Canvas canvas, Offset center, double radius) {
    final Rect sphereRect = Rect.fromCircle(center: center, radius: radius);

    final Paint base = Paint()
      ..shader = RadialGradient(
        center: const Alignment(-0.25, -0.35),
        radius: 1.0,
        colors: <Color>[
          const Color(0xFFFFF59D),
          const Color(0xFFFFB300),
          const Color(0xFF8D6E63),
          const Color(0xFF3E2723),
        ],
        stops: const <double>[0.0, 0.2, 0.65, 1.0],
      ).createShader(sphereRect);

    canvas.drawCircle(center, radius, base);

    canvas.save();
    canvas.clipPath(Path()..addOval(sphereRect));

    final int latLines = 11;
    final int lonLines = 14;
    final double ry = time * math.pi * 2.0;
    final double rx = time * math.pi * 1.2;

    for (int i = 0; i < latLines; i++) {
      final double lat = -math.pi / 2 + i * math.pi / (latLines - 1);
      final path = Path();
      bool started = false;
      for (int j = 0; j <= 100; j++) {
        final double lon = -math.pi + j * 2 * math.pi / 100;
        _Vec3 p = _spherePoint(lat, lon).rotateY(ry).rotateX(rx);
        final Offset pt = Offset(
          center.dx + p.x * radius,
          center.dy + p.y * radius,
        );
        if (!started) {
          path.moveTo(pt.dx, pt.dy);
          started = true;
        } else {
          path.lineTo(pt.dx, pt.dy);
        }
      }
      canvas.drawPath(
        path,
        Paint()
          ..style = PaintingStyle.stroke
          ..strokeWidth = 1
          ..color = Colors.white.withOpacity(0.18),
      );
    }

    for (int i = 0; i < lonLines; i++) {
      final double lon = -math.pi + i * 2 * math.pi / lonLines;
      final path = Path();
      bool started = false;
      for (int j = 0; j <= 100; j++) {
        final double lat = -math.pi / 2 + j * math.pi / 100;
        _Vec3 p = _spherePoint(lat, lon).rotateY(ry).rotateX(rx);
        final Offset pt = Offset(
          center.dx + p.x * radius,
          center.dy + p.y * radius,
        );
        if (!started) {
          path.moveTo(pt.dx, pt.dy);
          started = true;
        } else {
          path.lineTo(pt.dx, pt.dy);
        }
      }
      canvas.drawPath(
        path,
        Paint()
          ..style = PaintingStyle.stroke
          ..strokeWidth = 1
          ..color = Colors.cyanAccent.withOpacity(0.16),
      );
    }

    for (int y = 0; y < (radius * 2).toInt(); y += 10) {
      final double t = y / (radius * 2);
      final double yy = center.dy - radius + y;
      final double alpha =
          0.04 + 0.08 * math.sin((t + time) * math.pi * 6).abs();
      canvas.drawLine(
        Offset(center.dx - radius, yy),
        Offset(center.dx + radius, yy),
        Paint()
          ..color = Colors.white.withOpacity(alpha)
          ..strokeWidth = 2,
      );
    }

    canvas.restore();

    canvas.drawCircle(
      center,
      radius,
      Paint()
        ..style = PaintingStyle.stroke
        ..strokeWidth = 1.5
        ..color = Colors.white.withOpacity(0.4),
    );

    canvas.drawCircle(
      Offset(center.dx - radius * 0.28, center.dy - radius * 0.35),
      radius * 0.16,
      Paint()
        ..color = Colors.white.withOpacity(0.42)
        ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 12),
    );
  }

  _Vec3 _spherePoint(double lat, double lon) {
    final double x = math.cos(lat) * math.cos(lon);
    final double y = math.sin(lat);
    final double z = math.cos(lat) * math.sin(lon);
    return _Vec3(x, y, z);
  }

  Offset _project(_Vec3 v, Offset center, double scale) {
    const double distance = 4.0;
    final double perspective = distance / (distance - v.z);
    return Offset(
      center.dx + v.x * scale * perspective,
      center.dy + v.y * scale * perspective,
    );
  }

  void _drawTexturePattern(
    Canvas canvas,
    Rect bounds,
    Path clip,
    double brightness, {
    required double spacing,
  }) {
    final Paint p1 = Paint()
      ..color = Colors.white.withOpacity(0.05 + 0.10 * brightness)
      ..strokeWidth = 1;
    final Paint p2 = Paint()
      ..color = Colors.black.withOpacity(0.06)
      ..strokeWidth = 1;

    for (double x = bounds.left - bounds.height;
        x < bounds.right + bounds.height;
        x += spacing) {
      canvas.drawLine(
        Offset(x, bounds.top),
        Offset(x + bounds.height, bounds.bottom),
        p1,
      );
    }

    for (double x = bounds.left - bounds.height;
        x < bounds.right + bounds.height;
        x += spacing * 1.8) {
      canvas.drawLine(
        Offset(x, bounds.bottom),
        Offset(x + bounds.height, bounds.top),
        p2,
      );
    }
  }

  Rect _boundsOf(List<Offset> pts) {
    double left = pts.first.dx;
    double top = pts.first.dy;
    double right = pts.first.dx;
    double bottom = pts.first.dy;
    for (final p in pts) {
      left = math.min(left, p.dx);
      top = math.min(top, p.dy);
      right = math.max(right, p.dx);
      bottom = math.max(bottom, p.dy);
    }
    return Rect.fromLTRB(left, top, right, bottom);
  }

  Color _shade(Color color, double factor) {
    return Color.fromARGB(
      255,
      (color.red * factor).clamp(0, 255).toInt(),
      (color.green * factor).clamp(0, 255).toInt(),
      (color.blue * factor).clamp(0, 255).toInt(),
    );
  }

  @override
  bool shouldRepaint(covariant ThreeDScenePainter oldDelegate) {
    return oldDelegate.time != time;
  }
}

class _Vec3 {
  const _Vec3(this.x, this.y, this.z);

  final double x;
  final double y;
  final double z;

  _Vec3 operator -(_Vec3 other) => _Vec3(x - other.x, y - other.y, z - other.z);

  _Vec3 rotateX(double a) {
    final c = math.cos(a);
    final s = math.sin(a);
    return _Vec3(x, y * c - z * s, y * s + z * c);
  }

  _Vec3 rotateY(double a) {
    final c = math.cos(a);
    final s = math.sin(a);
    return _Vec3(x * c + z * s, y, -x * s + z * c);
  }

  _Vec3 rotateZ(double a) {
    final c = math.cos(a);
    final s = math.sin(a);
    return _Vec3(x * c - y * s, x * s + y * c, z);
  }

  _Vec3 cross(_Vec3 o) {
    return _Vec3(
      y * o.z - z * o.y,
      z * o.x - x * o.z,
      x * o.y - y * o.x,
    );
  }

  double dot(_Vec3 o) => x * o.x + y * o.y + z * o.z;

  double get length => math.sqrt(x * x + y * y + z * z);

  _Vec3 normalize() {
    final len = length;
    if (len == 0) return this;
    return _Vec3(x / len, y / len, z / len);
  }
}

class _FaceData {
  _FaceData({
    required this.points,
    required this.depth,
    required this.brightness,
    required this.kind,
  });

  final List<Offset> points;
  final double depth;
  final double brightness;
  final int kind;
}

class AINpuTestPage extends StatefulWidget {
  const AINpuTestPage({super.key});

  @override
  State<AINpuTestPage> createState() => _AINpuTestPageState();
}

class _AINpuTestPageState extends State<AINpuTestPage> {
  Timer? _timer;
  final math.Random _random = math.Random();

  double _latencyMs = 12.5;
  double _throughput = 24.0;
  double _utilization = 68.0;
  int _frameId = 0;
  bool _running = true;
  String _model = 'MobileNetV2';
  String _status = 'Running';

  final List<String> _models = const <String>[
    'MobileNetV2',
    'YOLO-Nano',
    'ResNet18',
    'PoseLite',
  ];

  @override
  void initState() {
    super.initState();
    _timer = Timer.periodic(const Duration(milliseconds: 180), (_) {
      if (!_running) return;
      setState(() {
        _frameId++;
        _latencyMs = 8 + _random.nextDouble() * 18;
        _throughput = 18 + _random.nextDouble() * 20;
        _utilization = 45 + _random.nextDouble() * 50;
        _status = _utilization > 90 ? 'High Load' : 'Running';
      });
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Column(
        children: <Widget>[
          const PageHeader(
            subtitle: 'Simulated AI inference pipeline and NPU workload view.',
          ),
          Expanded(
            child: ListView(
              padding: const EdgeInsets.fromLTRB(16, 12, 16, 96),
              children: <Widget>[
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      children: <Widget>[
                        DropdownButtonFormField<String>(
                          value: _model,
                          decoration: const InputDecoration(
                            labelText: 'AI Model',
                            border: OutlineInputBorder(),
                          ),
                          items: _models
                              .map((String m) => DropdownMenuItem<String>(
                                    value: m,
                                    child: Text(m),
                                  ))
                              .toList(),
                          onChanged: (String? value) {
                            if (value == null) return;
                            setState(() => _model = value);
                          },
                        ),
                        const SizedBox(height: 16),
                        Row(
                          children: <Widget>[
                            Expanded(
                              child: ElevatedButton(
                                onPressed: () {
                                  setState(() {
                                    _running = true;
                                    _status = 'Running';
                                  });
                                },
                                child: const Text('Start Inference'),
                              ),
                            ),
                            const SizedBox(width: 12),
                            Expanded(
                              child: OutlinedButton(
                                onPressed: () {
                                  setState(() {
                                    _running = false;
                                    _status = 'Paused';
                                  });
                                },
                                child: const Text('Pause'),
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 12),
                Row(
                  children: <Widget>[
                    Expanded(
                      child: _npuStatCard(
                        'Latency',
                        '${_latencyMs.toStringAsFixed(1)} ms',
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: _npuStatCard(
                        'Throughput',
                        '${_throughput.toStringAsFixed(1)} FPS',
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 12),
                Row(
                  children: <Widget>[
                    Expanded(
                      child: _npuStatCard(
                        'Utilization',
                        '${_utilization.toStringAsFixed(0)} %',
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: _npuStatCard('Frame ID', '$_frameId'),
                    ),
                  ],
                ),
                const SizedBox(height: 12),
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: <Widget>[
                        Text(
                          'Pipeline Status',
                          style: Theme.of(context).textTheme.titleMedium,
                        ),
                        const SizedBox(height: 16),
                        _pipelineBar('Input Capture', true),
                        _pipelineBar('Preprocess', _running),
                        _pipelineBar('NPU Inference', _running),
                        _pipelineBar('Postprocess', _running),
                        _pipelineBar('Overlay Render', _running),
                        const SizedBox(height: 12),
                        Text('Status: $_status'),
                        Text('Model: $_model'),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _npuStatCard(String label, String value) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 18),
        child: Column(
          children: <Widget>[
            Text(label, style: const TextStyle(fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Text(
              value,
              style: const TextStyle(fontSize: 22),
            ),
          ],
        ),
      ),
    );
  }

  Widget _pipelineBar(String label, bool active) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Row(
        children: <Widget>[
          SizedBox(
            width: 120,
            child: Text(label),
          ),
          Expanded(
            child: LinearProgressIndicator(
              value: active ? null : 0,
            ),
          ),
        ],
      ),
    );
  }
}

class StressTestPage extends StatefulWidget {
  const StressTestPage({super.key});

  @override
  State<StressTestPage> createState() => _StressTestPageState();
}

class _StressTestPageState extends State<StressTestPage>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;
  int _load = 120;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 6),
    )..repeat();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _setLoad(int value) {
    setState(() => _load = value);
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Column(
        children: <Widget>[
          const PageHeader(
            subtitle: 'High-frequency animation and repaint stress test.',
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            child: Wrap(
              spacing: 10,
              runSpacing: 10,
              children: <Widget>[
                ElevatedButton(
                  onPressed: () => _setLoad(80),
                  child: const Text('Low'),
                ),
                ElevatedButton(
                  onPressed: () => _setLoad(160),
                  child: const Text('Medium'),
                ),
                ElevatedButton(
                  onPressed: () => _setLoad(260),
                  child: const Text('High'),
                ),
                ElevatedButton(
                  onPressed: () => _setLoad(420),
                  child: const Text('Extreme'),
                ),
              ],
            ),
          ),
          Expanded(
            child: Padding(
              padding: const EdgeInsets.fromLTRB(16, 12, 16, 96),
              child: Card(
                clipBehavior: Clip.antiAlias,
                child: AnimatedBuilder(
                  animation: _controller,
                  builder: (BuildContext context, Widget? child) {
                    return CustomPaint(
                      painter: StressPainter2(
                        time: _controller.value,
                        count: _load,
                      ),
                      child: const SizedBox.expand(),
                    );
                  },
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class StressPainter2 extends CustomPainter {
  StressPainter2({
    required this.time,
    required this.count,
  });

  final double time;
  final int count;

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(
      Offset.zero & size,
      Paint()
        ..shader = const LinearGradient(
          colors: <Color>[
            Color(0xFF111827),
            Color(0xFF1F2937),
            Color(0xFF0F172A),
          ],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ).createShader(Offset.zero & size),
    );

    for (int i = 0; i < count; i++) {
      final double t = i / count;
      final double x =
          (size.width *
              (0.5 + 0.42 * math.sin((time * 2 + t) * math.pi * 2)));
      final double y =
          (size.height *
              (0.5 +
                  0.42 * math.cos((time * 1.7 + t * 1.3) * math.pi * 2)));
      final double r =
          4 + 10 * (0.5 + 0.5 * math.sin((time + t) * math.pi * 8));

      final Paint p = Paint()
        ..color = HSVColor.fromAHSV(
          0.8,
          (t * 360 + time * 360) % 360,
          0.8,
          1.0,
        ).toColor();

      canvas.drawCircle(Offset(x, y), r, p);
    }
  }

  @override
  bool shouldRepaint(covariant StressPainter2 oldDelegate) {
    return oldDelegate.time != time || oldDelegate.count != count;
  }
}

class VideoPlayerDemoPage extends StatefulWidget {
  const VideoPlayerDemoPage({super.key});

  @override
  State<VideoPlayerDemoPage> createState() => _VideoPlayerDemoPageState();
}

class _VideoPlayerDemoPageState extends State<VideoPlayerDemoPage>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;
  bool _playing = true;
  double _progress = 0.0;
  Timer? _timer;
  String _resolution = '1920x1080';
  bool _loop = true;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 12),
    )..repeat();

    _timer = Timer.periodic(const Duration(milliseconds: 120), (_) {
      if (!_playing) return;
      setState(() {
        _progress += 0.008;
        if (_progress >= 1.0) {
          _progress = _loop ? 0.0 : 1.0;
          if (!_loop) _playing = false;
        }
      });
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final String currentTime = _formatTime((_progress * 120).toInt());
    const String totalTime = '02:00';

    return SafeArea(
      child: Column(
        children: <Widget>[
          const PageHeader(
            subtitle: 'Video player UI demo with simulated playback rendering.',
          ),
          Expanded(
            child: ListView(
              padding: const EdgeInsets.fromLTRB(16, 12, 16, 96),
              children: <Widget>[
                Card(
                  clipBehavior: Clip.antiAlias,
                  child: AspectRatio(
                    aspectRatio: 16 / 9,
                    child: AnimatedBuilder(
                      animation: _controller,
                      builder: (BuildContext context, Widget? child) {
                        return CustomPaint(
                          painter: FakeVideoPainter(
                            time: _controller.value,
                            playing: _playing,
                          ),
                          child: Stack(
                            children: <Widget>[
                              Positioned(
                                left: 16,
                                top: 16,
                                child: Container(
                                  padding: const EdgeInsets.symmetric(
                                    horizontal: 10,
                                    vertical: 6,
                                  ),
                                  color: Colors.black54,
                                  child: const Text(
                                    'EDT Flutter Demo 1',
                                    style: TextStyle(color: Colors.white),
                                  ),
                                ),
                              ),
                              if (!_playing)
                                const Center(
                                  child: Icon(
                                    Icons.play_circle_fill,
                                    size: 90,
                                    color: Colors.white70,
                                  ),
                                ),
                            ],
                          ),
                        );
                      },
                    ),
                  ),
                ),
                const SizedBox(height: 12),
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      children: <Widget>[
                        Row(
                          children: <Widget>[
                            Text(currentTime),
                            Expanded(
                              child: Slider(
                                value: _progress,
                                onChanged: (double value) {
                                  setState(() => _progress = value);
                                },
                              ),
                            ),
                            const Text(totalTime),
                          ],
                        ),
                        const SizedBox(height: 8),
                        Wrap(
                          spacing: 12,
                          runSpacing: 12,
                          children: <Widget>[
                            ElevatedButton.icon(
                              onPressed: () {
                                setState(() => _playing = !_playing);
                              },
                              icon: Icon(
                                _playing ? Icons.pause : Icons.play_arrow,
                              ),
                              label: Text(_playing ? 'Pause' : 'Play'),
                            ),
                            OutlinedButton(
                              onPressed: () {
                                setState(() => _progress = 0.0);
                              },
                              child: const Text('Stop'),
                            ),
                            DropdownButton<String>(
                              value: _resolution,
                              items: const <DropdownMenuItem<String>>[
                                DropdownMenuItem(
                                  value: '1280x720',
                                  child: Text('1280x720'),
                                ),
                                DropdownMenuItem(
                                  value: '1920x1080',
                                  child: Text('1920x1080'),
                                ),
                                DropdownMenuItem(
                                  value: '3840x2160',
                                  child: Text('3840x2160'),
                                ),
                              ],
                              onChanged: (String? value) {
                                if (value == null) return;
                                setState(() => _resolution = value);
                              },
                            ),
                            Row(
                              mainAxisSize: MainAxisSize.min,
                              children: <Widget>[
                                const Text('Loop'),
                                Checkbox(
                                  value: _loop,
                                  onChanged: (bool? value) {
                                    setState(() => _loop = value ?? true);
                                  },
                                ),
                              ],
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  String _formatTime(int seconds) {
    final int mm = seconds ~/ 60;
    final int ss = seconds % 60;
    return '${mm.toString().padLeft(2, '0')}:${ss.toString().padLeft(2, '0')}';
  }
}

class FakeVideoPainter extends CustomPainter {
  FakeVideoPainter({
    required this.time,
    required this.playing,
  });

  final double time;
  final bool playing;

  @override
  void paint(Canvas canvas, Size size) {
    final Rect rect = Offset.zero & size;
    canvas.drawRect(
      rect,
      Paint()
        ..shader = const LinearGradient(
          colors: <Color>[
            Color(0xFF0B132B),
            Color(0xFF1C2541),
            Color(0xFF3A506B),
          ],
        ).createShader(rect),
    );

    final double t = playing ? time : 0.25;

    for (int i = 0; i < 12; i++) {
      final double dx = size.width * (i / 12.0);
      final double h = size.height *
          (0.2 + 0.6 * (0.5 + 0.5 * math.sin(t * math.pi * 2 + i)));
      canvas.drawRRect(
        RRect.fromRectAndRadius(
          Rect.fromLTWH(dx + 8, size.height - h, size.width / 16, h),
          const Radius.circular(8),
        ),
        Paint()
          ..color = Colors.primaries[i % Colors.primaries.length]
              .withOpacity(0.8),
      );
    }
  }

  @override
  bool shouldRepaint(covariant FakeVideoPainter oldDelegate) {
    return oldDelegate.time != time || oldDelegate.playing != playing;
  }
}

class ParkourGamePage extends StatefulWidget {
  const ParkourGamePage({super.key});

  @override
  State<ParkourGamePage> createState() => _ParkourGamePageState();
}

class _ParkourGamePageState extends State<ParkourGamePage>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;
  Timer? _timer;

  double _playerY = 0;
  double _velocityY = 0;
  bool _isJumping = false;
  double _obstacleX = 1.2;
  int _score = 0;
  bool _gameOver = false;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 16),
    )..addListener(_update);
    _controller.repeat();

    _timer = Timer.periodic(const Duration(seconds: 1), (_) {
      if (!_gameOver) {
        setState(() => _score++);
      }
    });
  }

  void _update() {
    if (_gameOver) return;

    setState(() {
      _obstacleX -= 0.02;
      if (_obstacleX < -0.2) {
        _obstacleX = 1.2;
      }

      if (_isJumping) {
        _playerY += _velocityY;
        _velocityY -= 0.012;
        if (_playerY <= 0) {
          _playerY = 0;
          _velocityY = 0;
          _isJumping = false;
        }
      }

      final bool hitX = _obstacleX < 0.22 && _obstacleX > 0.05;
      final bool hitY = _playerY < 0.16;
      if (hitX && hitY) {
        _gameOver = true;
      }
    });
  }

  void _jump() {
    if (_isJumping || _gameOver) return;
    setState(() {
      _isJumping = true;
      _velocityY = 0.08;
    });
  }

  void _restart() {
    setState(() {
      _playerY = 0;
      _velocityY = 0;
      _isJumping = false;
      _obstacleX = 1.2;
      _score = 0;
      _gameOver = false;
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Column(
        children: <Widget>[
          const PageHeader(
            subtitle: 'Simple parkour game demo for touch and animation testing.',
          ),
          Expanded(
            child: Padding(
              padding: const EdgeInsets.fromLTRB(16, 12, 16, 96),
              child: Card(
                clipBehavior: Clip.antiAlias,
                child: GestureDetector(
                  onTap: _jump,
                  child: Stack(
                    children: <Widget>[
                      Positioned.fill(
                        child: CustomPaint(
                          painter: ParkourPainter(
                            playerY: _playerY,
                            obstacleX: _obstacleX,
                          ),
                        ),
                      ),
                      Positioned(
                        left: 16,
                        top: 16,
                        child: Container(
                          padding: const EdgeInsets.all(10),
                          color: Colors.black54,
                          child: Text(
                            'EDT Flutter Demo 1\nScore: $_score',
                            style: const TextStyle(color: Colors.white),
                          ),
                        ),
                      ),
                      Positioned(
                        right: 16,
                        bottom: 16,
                        child: Wrap(
                          spacing: 12,
                          children: <Widget>[
                            ElevatedButton(
                              onPressed: _jump,
                              child: const Text('Jump'),
                            ),
                            OutlinedButton(
                              onPressed: _restart,
                              child: const Text('Restart'),
                            ),
                          ],
                        ),
                      ),
                      if (_gameOver)
                        Center(
                          child: Container(
                            padding: const EdgeInsets.all(20),
                            color: Colors.black87,
                            child: Column(
                              mainAxisSize: MainAxisSize.min,
                              children: <Widget>[
                                const Text(
                                  'Game Over',
                                  style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 28,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                const SizedBox(height: 12),
                                Text(
                                  'Final Score: $_score',
                                  style: const TextStyle(
                                    color: Colors.white,
                                    fontSize: 20,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class ParkourPainter extends CustomPainter {
  ParkourPainter({
    required this.playerY,
    required this.obstacleX,
  });

  final double playerY;
  final double obstacleX;

  @override
  void paint(Canvas canvas, Size size) {
    final Rect rect = Offset.zero & size;
    canvas.drawRect(
      rect,
      Paint()
        ..shader = const LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: <Color>[
            Color(0xFF87CEEB),
            Color(0xFFE0F7FA),
          ],
        ).createShader(rect),
    );

    final double groundY = size.height * 0.82;
    canvas.drawRect(
      Rect.fromLTWH(0, groundY, size.width, size.height - groundY),
      Paint()..color = const Color(0xFF4CAF50),
    );

    final double playerX = size.width * 0.14;
    final double playerSize = size.height * 0.12;
    final double playerBottom = groundY - playerY * size.height;

    canvas.drawRRect(
      RRect.fromRectAndRadius(
        Rect.fromLTWH(
          playerX,
          playerBottom - playerSize,
          playerSize,
          playerSize,
        ),
        const Radius.circular(10),
      ),
      Paint()..color = Colors.deepPurple,
    );

    final double obstacleWidth = size.width * 0.06;
    final double obstacleHeight = size.height * 0.14;
    final double ox = obstacleX * size.width;

    canvas.drawRRect(
      RRect.fromRectAndRadius(
        Rect.fromLTWH(
          ox,
          groundY - obstacleHeight,
          obstacleWidth,
          obstacleHeight,
        ),
        const Radius.circular(8),
      ),
      Paint()..color = Colors.redAccent,
    );
  }

  @override
  bool shouldRepaint(covariant ParkourPainter oldDelegate) {
    return oldDelegate.playerY != playerY || oldDelegate.obstacleX != obstacleX;
  }
}
```

### M33

```bash
cd $STWSV
unzip st-stm32cubeide_2.1.1_28236_20260312_0043_amd64.deb_bundle.sh.zip
chmod +x st-stm32cubeide_2.1.1_28236_20260312_0043_amd64.deb_bundle.sh
sudo ./st-stm32cubeide_2.1.1_28236_20260312_0043_amd64.deb_bundle.sh

cd $STWSV/$STECOF/Developer-Package
unzip stm32cubemp2-v1-3-0.zip

# Load
$STWSV/$STECOF/Starter-Package/stm32mp2-openstlinux-6.6-yocto-scarthgap-mpu-v26.02.18/images/stm32mp2/flashlayout_st-image-weston/optee/FlashLayout_sdcard_stm32mp257f-dk-ca35tdcid-ostl-m33-examples-optee.tsv

# Binaries path
/home/srv/STM32MPU_workspace/STM32MPU-Ecosystem-v6.2.0/Starter-Package/stm32mp2-openstlinux-6.6-yocto-scarthgap-mpu-v26.02.18/images/stm32mp2

sudo apt-get install -y git curl wget build-essential libssl-dev python3 python3-pip cmake make libncurses5

sudo apt-get install -y libncurses6 libncurses-dev

cmake --version

# error: externally-managed-environment
sudo apt install -y python3-full
pip install pyelftools
pip install pycryptodomex
wget http://security.ubuntu.com/ubuntu/pool/universe/n/ncurses/libtinfo5_6.3-2ubuntu0.1_amd64.deb
wget http://security.ubuntu.com/ubuntu/pool/universe/n/ncurses/libncurses5_6.3-2ubuntu0.1_amd64.deb
sudo apt install ./libtinfo5_6.3-2ubuntu0.1_amd64.deb ./libncurses5_6.3-2ubuntu0.1_amd64.deb
sudo chmod +x python3-pyelftools_0.30-1_all.deb
sudo dpkg -i python3-pyelftools_0.30-1_all.deb
python -c "import elftools; print(elftools.__version__)"
sudo dpkg -i python3-pycryptodome_3.20.0+dfsg-3_amd64.deb
dpkg -l | grep python3-pycryptodome

sudo apt install python3-pyelftools # Not work
sudo apt install python3-pycryptodomex # Not work

# File menu > Import > Existing Project into Workspace

# Root directory
/home/srv/STM32MPU_workspace/STM32MPU-Ecosystem-v6.2.0/Developer-Package/STM32Cube_FW_MP2_V1.3.0/Projects/STM32MP257F-DK/Applications/OpenAMP/OpenAMP_TTY_echo/STM32CubeIDE

# Select project OpenAMP_TTY_Echo_CM33_NonSecure and choose CA35TDCID_m33_ns_sign build configuration

# Open console on serial device

# Serial Target widget status
# STM32Cobe > Target Status

# In case of different statuses such as busy or console in use
# Window > Preferences > STM32Cube > MPU Serial
# /dev/ttyACM0

# Run configuration: create it by right-clicking on " OpenAMP_TTY_echo_CM33_NonSecure and selecting Run As and STM32 C/C++ Application. It opens the Embedded C/C++ Application window.

# Click the OK button. It opens the Edit the Configuration window. You may modify the name of the run configuration and must replace CA35TDCID_m33_ns_sign/OpenAMP_TTY_echo_CM33_NonSecure.elf with CA35TDCID_m33_ns_sign/OpenAMP_TTY_echo_CM33_NonSecure_sign.bin as shown in the following picture and press the OK button.

# Load Mode > Thru Linux core

# Run Configurations > Run

# Now the firmware is loaded. To debug it, a debug configuration is needed. Create it by right-clicking on OpenAMP_TTY_echo_CM33_NonSecure and selecting Debug As and STM32 C/C++ Application. It will open the Embedded C/C++ Application window.

# In the Edit the Configuration window, click the OK button. Click on the Startup tab and select the file. You may modify the name by adding _Debug

# Then click on the Edit button, in the Add/Edit item, uncheck Download and click OK.

# Click OK in the Edit Configuration where there is a False for the download.

# The debug perspective is started. If not, proceed in the same way as the run configuration but with the debug button instead. Press the suspend button, and the firmware will stop.

# In "production mode", the firmware does not break at main. GDB is simply attached to the running target. You can then use all features of the debugger.

### Board >

stty -onlcr -echo -F /dev/ttyRPMSG0
cat /dev/ttyRPMSG0 &
echo "Hello Virtual UART0" > /dev/ttyRPMSG0

# Terminate the STM32CubeIDE debug session will stop the firmware.

# Modify the main.c

# Then open the properties of the project by right-clicking on it and selecting Properties.
# Go to C/C++ Build > Settings > MCU GCC Compiler > Preprocessor
# Add a new symbol: __LOG_TRACE_IO_

# By clicking on the Run button, you can download the firmware. Then, by clicking on the Debug button, the STM32CubeIDE relaunches the debug session after performing an incremental build to account for your modifications.
# If everything is correct, you will switch back to the Debug Perspective window after reloading the new firmware.

stty -onlcr -echo -F /dev/ttyRPMSG0
stty -onlcr -echo -F /dev/ttyRPMSG1

cat /dev/ttyRPMSG0 &
cat /dev/ttyRPMSG1 &

echo "Hello Virtual UART0" > /dev/ttyRPMSG0

echo "Hello Virtual UART1" > /dev/ttyRPMSG1

### PC >

# On STM32MP2 series: When the firmware is running, log traces are output on an external terminal through a UART peripheral. For instance, the terminal is available on a Linux PC at /dev/ttyACM1:
minicom -D /dev/ttyACM1
```

`main.c`

```c
  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {

    OPENAMP_check_for_message();

    /* USER CODE END WHILE */
    if (VirtUart0RxMsg) {
      char msg_to_transmit[MAX_BUFFER_SIZE];
      int msg_size = 0;
      VirtUart0RxMsg = RESET;

      msg_size = snprintf(msg_to_transmit, MAX_BUFFER_SIZE, "Channel RPMSG0: ");
      msg_size += snprintf(msg_to_transmit + msg_size, MAX_BUFFER_SIZE, "%s\n", VirtUart0ChannelBuffRx);
      log_info("size of the message to transmit = %d bytes\n", msg_size);
      VIRT_UART_Transmit(&huart0, (uint8_t*)msg_to_transmit, msg_size);
    }

    if (VirtUart1RxMsg) {
      char msg_to_transmit[MAX_BUFFER_SIZE];
      uint16_t msg_size = 0;
      VirtUart1RxMsg = RESET;

      msg_size = snprintf(msg_to_transmit, MAX_BUFFER_SIZE, "Channel RPMSG1: ");
      msg_size += snprintf(msg_to_transmit + msg_size, MAX_BUFFER_SIZE, "%s\n", VirtUart1ChannelBuffRx);
      log_info("size of the message to transmit = %d bytes\n", msg_size);
      VIRT_UART_Transmit(&huart1, (uint8_t*)msg_to_transmit, msg_size);
    }
    /* USER CODE BEGIN 3 */
  }
  /* USER CODE END 3 */
```

## Distribution Package

Shared Document

```bash
mkdir $STWSV/$STECOF/Distribution-Package
cd $STWSV/$STECOF/Distribution-Package

git config --global user.email "you@example.com"
git config --global user.name "Your Name"

repo init -u https://github.com/STMicroelectronics/oe-manifest.git -b refs/tags/openstlinux-6.6-yocto-scarthgap-mpu-v26.02.18

repo sync

# OR

cd $STWSV/$STECOF
mkdir -p Distribution-Package
tar -xvf oe-manifest-openstlinux-6.6-yocto-scarthgap-mpu-v26.02.18.tar.gz -C Distribution-Package --strip-components=1
cd Distribution-Package
git init
git add .
git commit -m "Initial manifest"
repo init -u . -b master
repo sync

cd $STWSV/$STECOF/Distribution-Package
DISTRO=openstlinux-weston MACHINE=stm32mp2 source layers/meta-st/scripts/envsetup.sh

sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0

bitbake -c fetch m0projects-stm32mp2
bitbake -c fetch libopencsd

bitbake st-image-weston

# The build-<distro>-<machine>/tmp-glibc/deploy/images/<machine> directory receives complete file system images.

#### Generating your own Starter and Developer Packages

DISTRO=<distro> MACHINE=<machine> source layers/meta-st/scripts/envsetup.sh

# Modify the build-<distro>-<machine>/conf/local.conf file to enable archiver for recipes that are configured to use it; the objective is to generate the "source code" software packages for the Developer Package (Linux kernel, gcnano-driver, U-Boot, TF-A and OP-TEE OS)
ST_ARCHIVER_ENABLE = "1"

bitbake <image> --runall=deploy_archives

# The image (binaries) for the Starter Package are available in the build-<DISTRO>-<MACHINE>/tmp-glibc/deploy/images/<machine> directory
# The "source code" for the Developer Package software packages (Linux kernel, gcnano-driver, U-Boot, TF-A and OP-TEE OS) are available in the build-<distro>-<machine>/tmp-glibc/deploy/sources/arm-ostl-linux-gnueabi directory
```

### Display

DFROBOT DFR0506 7-inch HDMI Capacitive Touchscreen Display not support.

Default driver not support 1024x600@43Hz.

Waveshare 5.5inch HDMI AMOLED not support.

EDID report wrong message like 1280x720@100Hz, default driver not support user mode.

```bash
### Board >

# Check display
modetest -c
modetest -M stm

vi /etc/xdg/weston/weston.ini
vi /boot/mmc0_extlinux/extlinux.conf

systemctl restart weston-graphical-session

systemctl stop weston-graphical-session
modetest -M stm -s 32@41:1920x1080@XR24
systemctl start weston-graphical-session

# Retrieve all the video modes supported by the HDMI monitor
dmesg -C
echo 4 > /sys/module/drm/parameters/debug
systemctl restart weston-graphical-session
dmesg
```

## Android

Starter Package only for STM32MP257x-EV1.

Use Distribution Package for Android.

```bash
# Expand Disk with EXT4
# Delete all snapshots.
# Expand size with UI
lsblk
sudo fdisk -l
sudo apt install -y cloud-guest-utils
sudo growpart /dev/sda 2
sudo resize2fs /dev/sda2
df -h /
lsblk -o NAME,SIZE,FSTYPE,TYPE,MOUNTPOINT

# For Ubuntu 24.04
sudo tee /etc/apt/sources.list.d/jammy-security-ncurses.list >/dev/null <<'EOF'
deb http://security.ubuntu.com/ubuntu jammy-security main universe
EOF

sudo apt update
sudo apt install -y libtinfo5 libncurses5

ldconfig -p | grep -E 'libncurses.so.5|libtinfo.so.5'

cd $STWSV
mkdir Developer-Package-Android
cd Developer-Package-Android

git config --global user.email "you@example.com"
git config --global user.name "Your Name"

repo init -u https://github.com/STMicroelectronics/android-manifest  -b refs/tags/st-android-13.0.0-2025-11-21 -m stm32mp2droid.xml

# Try downloading in stages.
repo sync frameworks/base
# Long time, use SSH to log into the console to close the desktop and log out.
repo sync

source ./build/envsetup.sh
hmm
lunch aosp_dk-eng
stm32mp2setup
make -j $(nproc)

dmesg -T | grep -i -E 'killed process|out of memory|oom'
# Out of memory: Killed process xxxx (java)
# Killed process xxxx (ninja)
make -j 4

## ERROR: Not possible to load https://github.com/OP-TEE/optee_client/archive/3.19.0.tar.gz
vi device/stm/scripts/load_tee
447:          \wget ${archive_path}/archive/${tee_version}.tar.gz >/dev/null 2>&1
# to
447:          \curl -L ${archive_path}/archive/${tee_version}.tar.gz >/dev/null 2>&1

## "android.hardware.graphics.composer3-service.stm32mpu" depends on undefined module "hwcomposer3.drm_defaults"
cd $STWSV/Developer-Package-Android
find . -path "*drm_hwcomposer*" -type d
pushd external/drm_hwcomposer
git apply --check $STWSV/Developer-Package-Android/device/stm/stm32mp2/patch/android/drm_hwcomposer/0001-implement-the-AIDL-composer3-HAL-version.patch
git apply $STWSV/Developer-Package-Android/device/stm/stm32mp2/patch/android/drm_hwcomposer/0001-implement-the-AIDL-composer3-HAL-version.patch
ls hwc3
grep -R -n 'name: "hwcomposer3.drm_defaults"' .
popd
rm -rf out/soong
rm -f
source build/envsetup.sh
lunch aosp_dk-eng
stm32mp2setup
make -j4

## ERROR: files are incompatible: Runtime info and framework compatibility matrix are incompatible: No kernel entry found for kernel version 6.1 at kernel FCM version 7.
grep -R -n "PRODUCT_OTA_ENFORCE_VINTF_KERNEL_REQUIREMENTS" device/stm vendor/stm build
grep -R -n "5.10\|5.15\|6.1" device/stm vendor/stm system
cat out/target/product/dk/obj/PACKAGING/check_vintf_all_intermediates/kernel_version.txt
# 6.1.78-00033-g3b05c8f8a0eb
# For DK
vi device/stm/stm32mp2/dk/device.mk
vi device/stm/stm32mp2/eval/device.mk
source build/envsetup.sh
lunch aosp_dk-eng
stm32mp2setup
make -j4
```

