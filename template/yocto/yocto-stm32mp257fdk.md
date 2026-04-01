# Yocto - STM32MP257F-DK

The official OpenSTLinux defaults support PCAP Touch IC with common USB interfaces, using Type-A.

## Starter Package

```bash
mkdir $HOME/STM32MPU_workspace
cd $HOME/STM32MPU_workspace


wget -q www.google.com && echo "Internet access over HTTP/HTTPS is OK !" || echo "No internet access over HTTP/HTTPS ! You may need to set up a proxy."

STCPV=2.22.0

mkdir $HOME/STM32MPU_workspace/STM32MPU-Tools
mkdir $HOME/STM32MPU_workspace/STM32MPU-Tools/STM32CubeProgrammer-$STCPV
mkdir $HOME/STM32MPU_workspace/tmp
cd $HOME/STM32MPU_workspace/tmp

unzip SetupSTM32CubeProgrammer_linux_64.zip
./SetupSTM32CubeProgrammer-$STCPV.linux

export PATH=/home/srv/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin:$PATH

sudo apt-get install libusb-1.0-0

cd /home/srv/STMicroelectronics/STM32Cube/STM32CubeProgrammer/Drivers/rules

sudo cp *.* /etc/udev/rules.d/

# 

STM32_Programmer_CLI -l usb
# Product ID: DFU in HS Mode @Device ID /0x505, @Revision ID /0x2000

STM32_Programmer_CLI --h

STECOF=STM32MPU-Ecosystem-v6.2.0

cd $HOME/STM32MPU_workspace
mkdir $HOME/STM32MPU_workspace/$STECOF
mkdir $HOME/STM32MPU_workspace/$STECOF/Starter-Package
cd $HOME/STM32MPU_workspace/$STECOF/Starter-Package
tar xvf FLASH-stm32mp2-openstlinux-6.6-yocto-scarthg ap-mpu-v26.02.18.tar.gz

$HOME/STM32MPU_workspace/$STECOF/Starter-Package/stm32mp2-openstlinux-6.6-yocto-scarthgap-mpu-v26.02.18/images/stm32mp2/flashlayout_st-image-weston/optee/FlashLayout_sdcard_stm32mp257f-dk-optee.tsv

/home/srv/STM32MPU_workspace/$STECOF/Starter-Package/stm32mp2-openstlinux-6.6-yocto-scarthgap-mpu-v26.02.18/images/stm32mp2

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

ip addr show usb0

# Time error, apt cannot function
sudo apt update
date -s "2026-03-30 12:00:00"

# Check display
modetest -c

### PC >

ssh root@192.168.7.1
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

echo 'options mmc_block perdev_minors=16' > /tmp/mmc_block.conf
sudo mv /tmp/mmc_block.conf /etc/modprobe.d/mmc_block.conf

mkdir $HOME/STM32MPU_workspace/$STECOF/Developer-Package

tar xvf SDK-x86_64-stm32mp2-openstlinux-6.6-yocto-scarthgap-mpu-v26.02.18.tar.gz

chmod +x stm32mp2-openstlinux-6.6-yocto-scarthgap-mpu-v26.02.18/sdk/st-image-weston-openstlinux-weston-stm32mp2.rootfs-x86_64-toolchain-5.0.15-openstlinux-6.6-yocto-scarthgap-mpu-v26.02.18.sh

./stm32mp2-openstlinux-6.6-yocto-scarthgap-mpu-v26.02.18/sdk/st-image-weston-openstlinux-weston-stm32mp2.rootfs-x86_64-toolchain-5.0.15-openstlinux-6.6-yocto-scarthgap-mpu-v26.02.18.sh -d $HOME/STM32MPU_workspace/$STECOF/Developer-Package/SDK

cd $HOME/STM32MPU_workspace/STM32MPU-Ecosystem-v6.2.0/Developer-Package 
source SDK/environment-setup-cortexa35-ostl-linux

echo $ARCH

echo $CROSS_COMPILE

$CC --version

echo $OECORE_SDK_VERSION

mkdir $HOME/STM32MPU_workspace/STM32MPU-Ecosystem-v6.2.0/Developer-Package/stm32mp2-openstlinux-26.02.18
mkdir $HOME/STM32MPU_workspace/STM32MPU-Ecosystem-v6.2.0/Developer-Package/stm32mp2-openstlinux-26.02.18/sources

mkdir $HOME/STM32MPU_workspace/STM32MPU-Ecosystem-v6.2.0/Developer-Package/stm32mp2-openstlinux-26.02.18/sources/gtk_hello_world_example/
cd $HOME/STM32MPU_workspace/STM32MPU-Ecosystem-v6.2.0/Developer-Package/stm32mp2-openstlinux-26.02.18/sources/gtk_hello_world_example/
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

scp gtk_hello_world root@192.168.7.1:/usr/local

## Board >

cd /usr/local/
su -l weston -c "/usr/local/gtk_hello_world"

cd $HOME/STM32MPU_workspace/$STECOF/Developer-Package

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
scp -r boot/* root@192.168.7.1:/boot/

rm lib/modules/6.6.116/build

find . -name "*.ko" | xargs $STRIP --strip-debug --remove-section=.comment --remove-section=.note --preserve-dates

scp -r lib/modules/* root@192.168.7.1:/lib/modules

## Board >
/sbin/depmod -a

sync

reboot

# Using the Linux console, check that there is no log information when the display driver is probed
dmesg | grep -i modified

## PC >

cd $HOME/STM32MPU_workspace/$STECOF/Developer-Package/stm32mp-openstlinux-6.6-yocto-scarthgap-mpu-v26.02.18/sources/ostl-linux/linux-stm32mp-6.6.116-stm32mp-r3-r0/linux-6.6.116
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

scp ${OUTPUT_BUILD_DIR}/arch/${ARCH}/boot/Image.gz root@192.168.7.1:/boot

## Board >
reboot

dmesg | grep -i modified
```

## Flutter

```bash
sudo apt update
sudo apt install -y curl git unzip xz-utils zip cmake ninja-build pkg-config clang

find /opt/st -name 'environment-setup-*'
source /opt/st/stm32mp2-sdk/environment-setup-*
echo "$CC"
echo "$CXX"
echo "$SDKTARGETSYSROOT"

flutter-elinux-3.27.1

# Load ST SDK
source /opt/st/stm32mp2-sdk/environment-setup-*

# Clean build
cd ~/stm32mp257_flutter/demo_pages
rm -rf build
rm -rf elinux/flutter/ephemeral

# Recreate eLinux scaffolding
flutter-elinux create .

# Target sysroot build
flutter-elinux build elinux \
  --target-arch=arm64 \
  --target-sysroot="$SDKTARGETSYSROOT"


cd /opt
sudo git clone https://github.com/flutter/flutter.git -b stable
sudo chown -R $USER:$USER /opt/flutter
export PATH=/opt/flutter/bin:$PATH
flutter doctor

dart pub global activate flutter_elinux
export PATH="$HOME/.pub-cache/bin:$PATH"

cd /opt
sudo git clone https://github.com/sony/flutter-elinux.git
sudo chown -R $USER:$USER /opt/flutter-elinux
export PATH=$PATH:/opt/flutter-elinux/bin

flutter --version

flutter-elinux doctor
flutter-elinux devices

cd /opt
git clone https://github.com/flutter/flutter.git -b stable
git fetch --tags
git checkout 3.27.1
bin/flutter --version
export PATH=/opt/flutter/bin:$PATH

cd /opt
git clone https://github.com/sony/flutter-elinux.git
cd /opt/flutter-elinux
git fetch --tags
git checkout 3.27.1
export PATH=$PATH:/opt/flutter-elinux/bin

flutter doctor
flutter-elinux doctor
flutter-elinux devices

mkdir -p "$OECORE_NATIVE_SYSROOT/bin"
ln -sf "$(command -v aarch64-ostl-linux-gcc)"  "$OECORE_NATIVE_SYSROOT/bin/clang"
ln -sf "$(command -v aarch64-ostl-linux-g++)" "$OECORE_NATIVE_SYSROOT/bin/clang++"

vi lib/main.dart

# Disable Performance Overlay
showPerformanceOverlay: false,

flutter-elinux create .

rm -rf build
rm -rf elinux/flutter/ephemeral

flutter-elinux build elinux   --target-arch=arm64   --target-sysroot="$SDKTARGETSYSROOT"   --target-toolchain="$OECORE_NATIVE_SYSROOT"

scp -r build/elinux/arm64/release/bundle root@192.168.7.1:/usr/local/elinux_sample6

## Board

/usr/local/elinux_sample6/elinux_sample --bundle=$PWD --fullscreen
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
      showPerformanceOverlay: true,
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
```

## Distribution Package

Share