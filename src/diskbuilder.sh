#!/bin/bash


die() {
    echo "$1" >> /dev/stderr
    exit 1
}

do_primaries() {
    if cat /etc/fstab | grep MODDED; then
        return
    fi
    apt -y update
    apt -y install lzop initramfs-tools zstd zram-tools
    cat << EOF >> /etc/default/zramswap
CORES=1
ALLOCATION=16
PRIORITY=100
EOF
    systemctl enable zramswap
    systemctl disable dphys-swapfile
    systemctl stop dphys-swapfile
    [ -e "/boot/firmware/config.txt" ] && echo "gpu_mem=16" >> /boot/firmware/config.txt || echo "gpu_mem=16" >> /boot/config.txt
    mkswap /dev/mmcblk0p3 -L myswap
    echo "LABEL=myswap swap swap defaults 0 0" >> /etc/fstab
    rm -f /var/swap 
    swapon LABEL=myswap
    cat /etc/fstab | grep /tmp || echo "tmpfs /tmp tmpfs size=64M,nodev,nosuid 0 0 # MODDED" >> /etc/fstab
}


install_the_deb_pkgs() {
pkgs="python3-pyqt5 python3-pyqt5.qtwebkit libqt5webkit5-dev python3-pyqt5 python3-pyqt5.qtwebkit libqt5webkit5-dev pyqt5-dev-tools imagemagick fbi libsoxr-dev libsoxr0 python3-numpy python3-scipy pyqt5-dev-tools python3-pyqt5.qtwebkit alsa-utils avahi-daemon build-essential cmake cpufrequtils ffmpeg i2c-tools libb2-dev libbz2-dev libc6-dev libclang-dev libdirectfb-dev libffi-dev libgdbm-dev libgles2-mesa-dev libglu1-mesa-dev libjpeg-dev libmng-dev libncurses5-dev libncursesw5-dev libproxy-dev python3-pyqt5 python3-pyqt5.qsci python3-pyqt5.qtx11extra libqt5webkit5-dev libreadline6-dev libreadline-dev libsqlite3-dev libssl-dev libsystemd-dev libts-dev libwebp-dev libxkbcommon-x11-dev lightdm lm-sensors lxappearance lxde lxde-core lzma lzma-alone lzma-dev mesa-common-dev mpv opengl0 opengl0-dev paprefs pavucontrol pulseaudio pulseaudio-module-zeroconf pv python3-aiohttp python3-aiosignal python3-alsaaudio python3-anyio python3-asttokens python3-bs4 python3-certifi python3-charset-normalizer python3-decorator python3-executing python3-frozenlist python3-full python3-geopandas python3-h11 python3-httpcore python3-httpx python3-idna python3-ipython python3-jedi python3-matplotlib-inline python3-multidict python3-pandas python3-parse python3-parsedatetime python3-parso python3-pexpect python3-pil python3-pip python3-prompt-toolkit python3-ptyprocess python3-pure-eval python3-pyaudio python3-pydantic python3-pydub python3-pygments python3-requests python3-six python3-sniffio python3-stack-data python3-starlette python3-traitlets python3-typechecks python3-typeshed python3-typing-extensions python3-typing-inspect python3-wcwidth python3-websockets python3-yarl qt5-default qt5-qmake qt5-qmake-bin raspberrypi-ui-mods ratpoison tightvncserver tk-dev unclutter wget wmaker x11-apps xcb xscreensaver xscreensaver-* xserver-xorg zlib1g-dev zram-tools llvm-dev pyqt-advanced-slider"
for j in 1 2; do apt -y update; apt -y install $pkgs; for i in $pkgs ; do apt -y install $i; done; done
wget https://project-downloads.drogon.net/wiringpi-latest.deb -O /tmp/wiringpi-latest.deb
dpkg -i /tmp/wiringpi-latest.deb
rm -f /var/cache/apt/archives/*.deb
}



install_py312() {
    su -l m -c "mkdir -p /home/m/.tmp"
    python3 -m pip install typing_extensions
    cd /root
    wget https://www.python.org/ftp/python/3.12.4/Python-3.12.4.tar.xz -O - | tar -Jx
    cd Python-3*
    ./configure --enable-optimizations && make -j4 && make altinstall && echo WOOOO && cd .. && rm -Rf Python-3.* && echo YAYYYYY
}


install_rust() {
    apt -y remove rustc cargo
    su -l m -c "curl https://sh.rustup.rs -sSf | sh -s -- -y"
}


pythonmodules="timesetter readline wheel setuptools pillow elevenlabs numpy speechrecognition parse annotated-types bs4 more_itertools soxr soundfile pydub sliced librosa" # psola pyqt5 vosk kivymd open-meteo llvmlite


SUB_install_these_modules_with_this_python() {
    local i
    su -l m -c "mkdir -p /home/m/.tmp"
    failedmods=""; for i in $2; do echo "Installing $i"; su -l m -c "TMPDIR=/home/m/.tmp $1 -m pip install $i" || failedmods="$failedmods $i"; done; [ "$failedmods" == "" ] || (echo "Failed to install$failedmods on $1" >> /dev/stderr; return 1)
}


install_python_rust_etc() {
    su -l m -c "mkdir -p /home/m/.tmp"
    echo "Installing python packages for python 3.7; please wait."
    SUB_install_these_modules_with_this_python python3 "$pythonmodules"
    res=$?
    if python3 --version | fgrep "Python 3.7"; then
        install_py312
        install_rust
        false
        SUB_install_these_modules_with_this_python python3.12 "$pythonmodules"
        res=$(($res+$?))
    fi
    if [ "$res" -ne "0" ] ; then
        echo "WARNING -- errors occurred. Not all packages were installed."
    fi
}

install_the_software() {
    install_the_deb_pkgs
    install_python_rust_etc
}


DONOTUSE_install_pisugar() {
    wget https://cdn.pisugar.com/release/pisugar-power-manager.sh
    bash pisugar-power-manager.sh -c release
#    [ -e "/dev/i2c-1" ] || sudo ln -s /dev/i2c-11 /dev/i2c-1
}

configure_stuff() {
    wget "https://raw.githubusercontent.com/torvalds/linux/master/scripts/bootgraph.pl" -O /home/m/bootgraph.pl
    mkdir -p /boot/firmware
    mkdir -p /etc/cron.minutely
    echo "*  *    * * *   root    cd / && run-parts --report /etc/cron.minutely" >> /etc/crontab
    cat << 'EOF' > /etc/cron.minutely/reboot_if_wifi_dies
#!/bin/bash

if [ -e "/boot/firmware/reboot_if_wifi_fails" ]; then
    i=0
    while [ "$i" -le "10" ] && ! ping -c1 -w5 8.8.8.8 > /dev/null 2> /dev/null; do
        i=$(($i+1))
        sleep 1
    done
    if [ "$i" -gt "10" ]; then
        reboot
        exit 1
    else
        exit 0
    fi
fi
EOF
chmod +x /etc/cron.minutely/reboot_if_wifi_dies
sed -i s/CONF_SWAPSIZE=.*/CONF_SWAPSIZE=2048/ /etc/dphys-swapfile
sed -i s/'exit 0'// /etc/rc.local
cat << 'EOF' >> /etc/sudoers
m       ALL=(ALL:ALL) /usr/bin/date
EOF
cat << 'EOF' >> /etc/rc.local
cpufreq-set -g powersave # ondemand
if [ -e "/boot/firmware/hostname" ] || [ -e "/boot/firmware/wpa_supplicant.conf" ] ; then
    if [ -e "/boot/firmware/hostname" ] ; then
        oldhost=$(cat /etc/hostname)
        newhost=$(cat /boot/firmware/hostname)
        sed -i s/$oldhost/$newhost/ /etc/hostname # FIXME bad results if old or new happens to be a common word
        mv -f /boot/firmware/hostname /etc
        hostnamectl set-hostname $newhost
        systemctl restart avahi-daemon
    fi
    if [ -e "/boot/firmware/wpa_supplicant.conf" ] ; then
        mv -f /boot/firmware/wpa_supplicant.conf /etc/wpa_supplicant/
        ip link set dev wlan0 down
        ip link set dev wlan0 up
    fi
fi
/usr/bin/tvservice -o # disable HDMI until reboot
exit 0
EOF
cat << EOF > /boot/firmware/wpa_supplicant.conf.EXAMPLE
country=FR
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
ap_scan=1

update_config=1
network={
        ssid="Some ID Or Other"
        psk=11223344556677889900aabbccddeeffbbc1bbc2b00bd00df00d
}
EOF
echo somehostnameorother > /boot/firmware/hostname.EXAMPLE

    mkdir -p /etc/wireplumber/main.lua.d/
    cat << EOF > /etc/wireplumber/main.lua.d/51-disable-suspension.lua
table.insert (alsa_monitor.rules, {
  matches = {
    {
      -- Matches all sources.
      { "node.name", "matches", "alsa_input.*" },
    },
    {
      -- Matches all sinks.
      { "node.name", "matches", "alsa_output.*" },
    },
  },
  apply_properties = {
    ["session.suspend-timeout-seconds"] = 0,  -- 0 disables suspend
  },
})

EOF
cat <<EOF > /etc/systemd/system/myvnc.service
# START MY VNC SERVER

[Unit]
Description=Start My VNC Server at Boot-up
After=palpac.service
#After=network.target NO

[Service]
Type=simple
ExecStart=/usr/local/bin/keepvnc.sh
User=m

[Install]
WantedBy=multi-user.target

EOF
   cat <<EOF > /usr/local/bin/keepvnc.sh
#!/bin/bash

killall Xtightvnc
while true; do
    echo "Launching vncserver"
    vncserver
    while ps wax | grep -w Xtightvnc | grep -vw grep > /dev/null; do
        sleep 10
    done
done
EOF
  chmod +x /usr/local/bin/keepvnc.sh
    echo "consoleblank=0 console=serial0,115200 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=noop fsck.repair=yes rootwait cfg80211.ieee80211_regdom=FR rd.plymouth=0 plymouth.enable=0 vt.global_cursor_default=0 quiet logo.nologo nosplash silent dwc_otg.lpm_enable=0 rootflags=commit=120,data=writeback noatime nodiratime fastboot data=writeback loglevel=0 printk.time=1 initcall_debug" > /boot/cmdline.txt
    echo "boot_delay=0
dtoverlay=disable-bt" >> /boot/config.txt # DISABLES BLUETOOTH
}


add_rollmeback_script() {
    cat << 'EOF' > /usr/local/sbin/rollmeback
#!/bin/bash

if ! echo "$0" | grep /tmp > /dev/null; then
    tempfname=/tmp/runme.$RANDOM.sh
    cp -f "$0" $tempfname
    chmod +x $tempfname
    $tempfname "$@"
    exit $?
fi
if [ "$UID" != "0" ]; then
    sudo $0 "$@"
    exit $?
fi
mkdir -p /tmp/p2 /tmp/p4
mount /dev/mmcblk0p2 /tmp/p2 2> /dev/null
mount /dev/mmcblk0p1 /tmp/p2/boot 2> /dev/null
mount /dev/mmcblk0p4 /tmp/p4 -o compress=lzo 2> /dev/null
g="$1"
if [ "$g" == "" ] || [ ! -e "/tmp/p4/"$g ]; then
    echo "SNAPSHOT NOT FOUND; PLEASE CHOOSE ONE OF THESE:
$(btrfs subvolume list /tmp/p4 | cut -d' ' -f9)" >> /dev/stderr; exit 2
else
    rsync -av --del --exclude=tmp /tmp/p4/"$g"/{bin,boot,etc,home,lib,opt,root,sbin,srv,usr,var} /tmp/p2/
    cp -f /tmp/p4/"$g"/boot/config.txt /tmp/p2/boot/
fi
read -t 10 -p "Reboot (y/n)?" choice
case "$choice" in 
  y|Y ) echo "Rebooting"; reboot;;
  n|N ) echo "ok";;
  * ) echo "Rebooting"; reboot;;
esac
EOF
    chmod +x /usr/local/sbin/rollmeback
}


purge_crap() {
    rm -Rf /usr/share/doc/*
    apt --purge -y remove libreoffice* chromium-browser wolfram*
    rm -f /etc/xdg/autostart/piwiz.desktop # to disable the wizard that sets region etc.
    apt -y purge piwiz # https://forums.raspberrypi.com/viewtopic.php?t=231557
}



snag_kernel_src() {
    apt -y install git fakeroot build-essential ncurses-dev xz-utils libssl-dev bc flex libelf-dev bison lz4 liblz4*
    mkdir -p /usr/src && cd /usr/src && git clone --depth=1 --branch rpi-5.10.y https://github.com/raspberrypi/linux
    cd /usr/src/linux
    make clean
    KERNEL=kernel8
    make bcm2711_defconfig
    mv .config .config.BEFORE
    modprobe configs
}




optimA() {
    echo "CONFIG_CC_OPTIMIZE_FOR_SIZE=y" >> .config
    sed -i s/CONFIG_CC_OPTIMIZE_FOR_PERFORMANCE.*// .config
    (yes "" | make -j4 zImage) & procno=$!
    sleep 30
    kill $procno
    killall gcc make 
}

optimB() {
    sed -i s/CONFIG_KERNEL_GZIP=.*/CONFIG_KERNEL_LZ4=y/ .config
    (yes "" | make -j4 zImage) & procno=$!
    sleep 30
    kill $procno
    killall gcc make 
}

optimC() {
    sed -i s/CONFIG_USB_STORAGE=.*/CONFIG_USB_STORAGE=n/ .config
    sed -i s/CONFIG_USB_GADGET=.*/CONFIG_USB_GADGET=n/ .config
    sed -i s/CONFIG_USB_GADGETFS=.*/CONFIG_USB_GADGETFS=n/ .config
    sed -i s/CONFIG_USB_MIDI_GADGET=.*/CONFIG_USB_MIDI_GADGET=n/ .config
    sed -i s/CONFIG_SCSI.*=y// .config
    sed -i s/CONFIG_.*RADIO.*=.*// .config
    sed -i s/CONFIG_F2FS_FS=y/CONFIG_F2FS_FS=m/ .config
    sed -i s/CONFIG_USB_DWC2=y/CONFIG_USB_DWC2=m/ .config
    sed -i s/CONFIG_USB_USBNET=y/CONFIG_USB_USBNET=m/ .config
    sed -i s/CONFIG_USB_NET_DRIVERS=y/CONFIG_USB_NET_DRIVERS=m/ .config
    (yes "n" | make -j4 zImage) & procno=$!
    sleep 30
    kill $procno
    killall gcc make 
}

optimD() {
    # ABANDON ALL PREVIOUS CHANGES!
    cp -f .config.BEFORE .config
    for d in CONFIG_RD_ CONFIG_HAVE_KERNEL_ CONFIG_ZSWAP_COMPRESSOR_ INITRAMFS_COMPRESS CONFIG_ZSWAP_COMPRESSOR_DEFAULT_; do
        sed -i s/"$d"*// .config
    done
# CONFIG_USB_GADGET CONFIG_USB_STORAGE  CONFIG_USB_GADGETFS 
# CONFIG_USB_MIDI_GADGET CONFIG_USB_USBNET CONFIG_USB_NET_DRIVERS 
# CONFIG_USB_DWC2 CONFIG_NETWORK_FILESYSTEMS CONFIG_QUOTA MD CONFIG_RC_CORE CONFIG_F2FS_FS
# CONFIG_SECURITY_APPARMOR CONFIG_CPU_SPECTRE
    for d in CONFIG_RD_GZIP \
            CONFIG_HAVE_KERNEL_LZMA CONFIG_HAVE_KERNEL_GZIP CONFIG_HAVE_KERNEL_XZ CONFIG_HAVE_KERNEL_LZO \
            CONFIG_KERNEL_GZIP CONFIG_KERNEL_LZMA CONFIG_KERNEL_XZ CONFIG_KERNEL_LZO \
            INITRAMFS_COMPRESSION_GZIP CONFIG_ZSWAP_COMPRESSOR_DEFAULT_DEFLATE \
            CONFIG_ZSWAP_COMPRESSOR_DEFAULT_LZO CONFIG_ZSWAP_COMPRESSOR_DEFAULT_LZ4HC \
            CONFIG_ZSWAP_COMPRESSOR_DEFAULT_ZSTD CONFIG_ZSWAP_COMPRESSOR_DEFAULT_842 \
            CONFIG_INITRAMFS_COMPRESSION_GZIP CONFIG_LZO_DECOMPRESS CONFIG_ZSTD_DECOMPRESS \
            CONFIG_CC_OPTIMIZE_FOR_PERFORMANCE; do
        sed -i s/$d=/'# '$d' is not set'/ .config
    done 
    cat << 'EOF' >> .config
CONFIG_CC_OPTIMIZE_FOR_SIZE=y
INITRAMFS_SOURCE=""
CONFIG_HAVE_KERNEL_LZ4=y
CONFIG_KERNEL_LZ4=y
CONFIG_RD_GZIP=n
CONFIG_RD_LZ4=y
CONFIG_RD_BZIP2=n
CONFIG_RD_LZO=n
CONFIG_RD_LZMA=n
CONFIG_RD_RD_LZMA=n
CONFIG_RD_XZ=n
CONFIG_RD_ZSTD=n
CONFIG_INITRAMFS_COMPRESSION_LZ4=y
CONFIG_LZ4_DECOMPRESS=y
INITRAMFS_COMPRESSION_LZ4=y
CONFIG_ZSWAP_COMPRESSOR_DEFAULT_LZ4=y
CONFIG_ZSWAP_COMPRESSOR_DEFAULT="lz4"
NET_VENDOR_XILINX=n
EOF
   ./scripts/config --file .config -d DEBUG_INFO \
  -d DEBUG_INFO_DWARF_TOOLCHAIN_DEFAULT -d DEBUG_INFO_DWARF4 \
  -d DEBUG_INFO_DWARF5 -e CONFIG_DEBUG_INFO_NONE
    make olddefconfig
}


optimE() {
    # ABANDON ALL PREVIOUS CHANGES!
    cp -f .config.BEFORE .config
   ./scripts/config --file .config -d DEBUG_INFO \
  -d DEBUG_INFO_DWARF_TOOLCHAIN_DEFAULT -d DEBUG_INFO_DWARF4 \
  -d DEBUG_INFO_DWARF5 -e CONFIG_DEBUG_INFO_NONE

    for d in CONFIG_RD_ CONFIG_HAVE_KERNEL_ CONFIG_ZSWAP_COMPRESSOR_ INITRAMFS_COMPRESS CONFIG_ZSWAP_COMPRESSOR_DEFAULT_; do
        sed -i s/"$d"*// .config
    done

    for d in CONFIG_USB_DWC2 CONFIG_NETWORK_FILESYSTEMS CONFIG_QUOTA MD CONFIG_RC_CORE CONFIG_F2FS_FS CONFIG_RD_GZIP \
            CONFIG_HAVE_KERNEL_LZMA CONFIG_HAVE_KERNEL_GZIP CONFIG_HAVE_KERNEL_XZ CONFIG_HAVE_KERNEL_LZO \
            CONFIG_KERNEL_GZIP CONFIG_KERNEL_LZMA CONFIG_KERNEL_XZ CONFIG_KERNEL_LZO \
            INITRAMFS_COMPRESSION_GZIP CONFIG_ZSWAP_COMPRESSOR_DEFAULT_DEFLATE \
            CONFIG_ZSWAP_COMPRESSOR_DEFAULT_LZO CONFIG_ZSWAP_COMPRESSOR_DEFAULT_LZ4HC \
            CONFIG_ZSWAP_COMPRESSOR_DEFAULT_ZSTD CONFIG_ZSWAP_COMPRESSOR_DEFAULT_842 \
            CONFIG_INITRAMFS_COMPRESSION_GZIP CONFIG_LZO_DECOMPRESS CONFIG_ZSTD_DECOMPRESS \
            CONFIG_CC_OPTIMIZE_FOR_PERFORMANCE; do
        sed -i s/$d=/'# '$d' is not set'/ .config
    done
    cat << 'EOF' >> .config
CONFIG_CC_OPTIMIZE_FOR_SIZE=y
INITRAMFS_SOURCE=""
CONFIG_HAVE_KERNEL_LZ4=y
CONFIG_KERNEL_LZ4=y
CONFIG_RD_GZIP=n
CONFIG_RD_LZ4=y
CONFIG_RD_BZIP2=n
CONFIG_RD_LZO=n
CONFIG_RD_LZMA=n
CONFIG_RD_RD_LZMA=n
CONFIG_RD_XZ=n
CONFIG_RD_ZSTD=n
CONFIG_INITRAMFS_COMPRESSION_LZ4=y
CONFIG_LZ4_DECOMPRESS=y
INITRAMFS_COMPRESSION_LZ4=y
CONFIG_ZSWAP_COMPRESSOR_DEFAULT_LZ4=y
CONFIG_ZSWAP_COMPRESSOR_DEFAULT="lz4"
NET_VENDOR_XILINX=n
EOF
}





optimF() {
    # ABANDON ALL PREVIOUS CHANGES!
    cp -f .config.BEFORE .config
   ./scripts/config --file .config -d DEBUG_INFO \
  -d DEBUG_INFO_DWARF_TOOLCHAIN_DEFAULT -d DEBUG_INFO_DWARF4 \
  -d DEBUG_INFO_DWARF5 -e CONFIG_DEBUG_INFO_NONE

    for d in CONFIG_RD_ CONFIG_HAVE_KERNEL_ CONFIG_ZSWAP_COMPRESSOR_ INITRAMFS_COMPRESS CONFIG_ZSWAP_COMPRESSOR_DEFAULT_; do
        sed -i s/"$d"*// .config
    done
    for d in CONFIG_USB_GADGET CONFIG_USB_STORAGE CONFIG_USB_GADGETFS CONFIG_USB_MIDI_GADGET CONFIG_USB_USBNET CONFIG_USB_NET_DRIVERS \
            CONFIG_USB_DWC2 CONFIG_NETWORK_FILESYSTEMS CONFIG_QUOTA MD CONFIG_RC_CORE CONFIG_F2FS_FS CONFIG_RD_GZIP \
            CONFIG_HAVE_KERNEL_LZMA CONFIG_HAVE_KERNEL_GZIP CONFIG_HAVE_KERNEL_XZ CONFIG_HAVE_KERNEL_LZO \
            CONFIG_KERNEL_GZIP CONFIG_KERNEL_LZMA CONFIG_KERNEL_XZ CONFIG_KERNEL_LZO \
            INITRAMFS_COMPRESSION_GZIP CONFIG_ZSWAP_COMPRESSOR_DEFAULT_DEFLATE \
            CONFIG_ZSWAP_COMPRESSOR_DEFAULT_LZO CONFIG_ZSWAP_COMPRESSOR_DEFAULT_LZ4HC \
            CONFIG_ZSWAP_COMPRESSOR_DEFAULT_ZSTD CONFIG_ZSWAP_COMPRESSOR_DEFAULT_842 \
            CONFIG_INITRAMFS_COMPRESSION_GZIP CONFIG_LZO_DECOMPRESS CONFIG_ZSTD_DECOMPRESS \
            CONFIG_CC_OPTIMIZE_FOR_PERFORMANCE; do
        sed -i s/$d=/'# '$d' is not set'/ .config
    done
    cat << 'EOF' >> .config
CONFIG_CC_OPTIMIZE_FOR_SIZE=y
INITRAMFS_SOURCE=""
CONFIG_HAVE_KERNEL_LZ4=y
CONFIG_KERNEL_LZ4=y
CONFIG_RD_GZIP=n
CONFIG_RD_LZ4=y
CONFIG_RD_BZIP2=n
CONFIG_RD_LZO=n
CONFIG_RD_LZMA=n
CONFIG_RD_RD_LZMA=n
CONFIG_RD_XZ=n
CONFIG_RD_ZSTD=n
CONFIG_INITRAMFS_COMPRESSION_LZ4=y
CONFIG_LZ4_DECOMPRESS=y
INITRAMFS_COMPRESSION_LZ4=y
CONFIG_ZSWAP_COMPRESSOR_DEFAULT_LZ4=y
CONFIG_ZSWAP_COMPRESSOR_DEFAULT="lz4"
NET_VENDOR_XILINX=n
ZSWAP_DEFAULT_ON=y
EOF
}



optimG() {
    # ABANDON ALL PREVIOUS CHANGES!
    cp -f .config.BEFORE .config
   ./scripts/config --file .config -d DEBUG_INFO \
  -d DEBUG_INFO_DWARF_TOOLCHAIN_DEFAULT -d DEBUG_INFO_DWARF4 \
  -d DEBUG_INFO_DWARF5 -e CONFIG_DEBUG_INFO_NONE

    for d in CONFIG_RD_ CONFIG_HAVE_KERNEL_ CONFIG_ZSWAP_COMPRESSOR_ INITRAMFS_COMPRESS CONFIG_ZSWAP_COMPRESSOR_DEFAULT_; do
        sed -i s/"$d"*// .config
    done
    for d in CONFIG_KERNFS CONFIG_CPU_SPECTRE CONFIG_SECURITY_APPARMOR MD \
            CONFIG_USB_GADGET CONFIG_USB_STORAGE CONFIG_USB_GADGETFS CONFIG_USB_MIDI_GADGET CONFIG_USB_USBNET CONFIG_USB_NET_DRIVERS \
            CONFIG_USB_DWC2 CONFIG_NETWORK_FILESYSTEMS CONFIG_QUOTA MD CONFIG_RC_CORE CONFIG_F2FS_FS CONFIG_RD_GZIP \
            CONFIG_HAVE_KERNEL_LZMA CONFIG_HAVE_KERNEL_GZIP CONFIG_HAVE_KERNEL_XZ CONFIG_HAVE_KERNEL_LZO \
            CONFIG_KERNEL_GZIP CONFIG_KERNEL_LZMA CONFIG_KERNEL_XZ CONFIG_KERNEL_LZO \
            INITRAMFS_COMPRESSION_GZIP CONFIG_ZSWAP_COMPRESSOR_DEFAULT_DEFLATE \
            CONFIG_ZSWAP_COMPRESSOR_DEFAULT_LZO CONFIG_ZSWAP_COMPRESSOR_DEFAULT_LZ4HC \
            CONFIG_ZSWAP_COMPRESSOR_DEFAULT_ZSTD CONFIG_ZSWAP_COMPRESSOR_DEFAULT_842 \
            CONFIG_INITRAMFS_COMPRESSION_GZIP CONFIG_LZO_DECOMPRESS CONFIG_ZSTD_DECOMPRESS \
            CONFIG_CC_OPTIMIZE_FOR_PERFORMANCE; do
        sed -i s/$d=/'# '$d' is not set'/ .config
    done
    cat << 'EOF' >> .config
CONFIG_CC_OPTIMIZE_FOR_SIZE=y
INITRAMFS_SOURCE=""
CONFIG_HAVE_KERNEL_LZ4=y
CONFIG_KERNEL_LZ4=y
CONFIG_RD_GZIP=n
CONFIG_RD_LZ4=y
CONFIG_RD_BZIP2=n
CONFIG_RD_LZO=n
CONFIG_RD_LZMA=n
CONFIG_RD_RD_LZMA=n
CONFIG_RD_XZ=n
CONFIG_RD_ZSTD=n
CONFIG_INITRAMFS_COMPRESSION_LZ4=y
CONFIG_LZ4_DECOMPRESS=y
INITRAMFS_COMPRESSION_LZ4=y
CONFIG_ZSWAP_COMPRESSOR_DEFAULT_LZ4=y
CONFIG_ZSWAP_COMPRESSOR_DEFAULT="lz4"
NET_VENDOR_XILINX=n
ZSWAP_DEFAULT_ON=y
EOF
}


    
optimH() {
    cd /usr/src/linux
    sed -i s/palpac-G/palpac-H/ .config
    sed -i s/CONFIG_CC_OPTIMIZE_FOR_.*// .config
    cat << EOF >> .config
CONFIG_CC_OPTIMIZE_FOR_PERFORMANCE=y
# CONFIG_CC_OPTIMIZE_FOR_SIZE is not set
EOF
}
 





optimI() {
cd /usr/src/linux
    cat << 'EOF' > /boot/splash.txt
## Initramfs-Splash
image=splash.png
fullscreen=0
EOF
    wget "https://png.pngtree.com/png-clipart/20221025/original/pngtree-free-home-delivery-png-image_8720530.png" -O /boot/splash.png
    wget "https://gitlab.com/DarkElvenAngel/initramfs-splash/-/raw/master/boot/initramfs.img?ref_type=heads" -O /boot/initramfs.img.ORIG
    rm -Rf splashhere
    mkdir -p splashhere
    cd splashhere
    zcat /boot/initramfs.img.ORIG | cpio -iV
    mv -f init init.old
    head -n$(grep -n "umount /mnt/boot" init.old | cut -d':' -f1) init.old > init
    cat << 'EOF' >> init
mount -o rw /dev/mmcblk0p2 /mnt/root || Rescue_Shell
echo "The time is $(date)" >> /mnt/root/.hi.txt
mount -o remount,ro /mnt/root

umount /proc /sys
mount --move /dev /mnt/root/dev

exec switch_root /mnt/root /sbin/init
EOF
    chmod +x init
    find . | cpio -oH newc | gzip -9 > /boot/initramfs.img
    cd ..
    zcat /boot/initramfs.img > rd.cpio
    sed -i s/CONFIG_INITRAMFS_SOURCE=.*/CONFIG_INITRAMFS_SOURCE=\"rd.cpio\"/ .config
    sed -i s/CONFIG_INITRAMFS_COMPRESSION_.*// .config
    echo "CONFIG_INITRAMFS_COMPRESSION_LZ4=y
# CONFIG_INITRAMFS_COMPRESSION_BZIP2 is not set
# CONFIG_INITRAMFS_COMPRESSION_LZMA is not set
# CONFIG_INITRAMFS_COMPRESSION_XZ is not set
# CONFIG_INITRAMFS_COMPRESSION_LZO is not set
# CONFIG_INITRAMFS_COMPRESSION_GZIP is not set
# CONFIG_INITRAMFS_COMPRESSION_ZSTD is not set
# CONFIG_INITRAMFS_COMPRESSION_NONE is not set" >> .config
}





test_optim() {
    local ver=$1
    cd /usr/src/linux
    optim$ver
    sed -i s/CONFIG_LOCALVERSION=.*/CONFIG_LOCALVERSION=\"-v8-palpac-$ver\"/ .config
    cp -f .config .config.$ver
    rm arch/arm/boot/*mage
    yes "" | make -j4 zImage modules dtbs
    mount /boot
    make modules_install
    cp arch/arm/boot/dts/*.dtb /boot/
    cp arch/arm/boot/dts/overlays/*.dtb* /boot/overlays/
    cp arch/arm/boot/dts/overlays/README /boot/overlays/
    cp arch/arm/boot/zImage /boot/kernel-v8-$ver.img
    sed -i s/kernel=.*// /boot/config.txt
    echo "kernel=kernel-v8-$ver.img" >> /boot/config.txt
    snappit "@after_building_kernel_$ver"
}



compile_and_install_kernel_and_modules() {
    local ver
    mount /boot
    cpufreq-set -g powersave # performance
    if [ -e "/boot/kernel-v8-stockish.img" ]; then
        echo "Built the stock(ish) kernel already. No need to snag kernel code etc."
    else
        snag_kernel_src
        cd /usr/src/linux
        zcat /proc/config.gz > .config
        yes "" | make oldconfig
        sed -i s/CONFIG_LOCALVERSION=.*/CONFIG_LOCALVERSION=\"-v8-stockish\"/ .config
        yes "" | make -j4 zImage modules dtbs; mount /boot; make modules_install; cp arch/arm/boot/dts/*.dtb /boot/; cp arch/arm/boot/dts/overlays/*.dtb* /boot/overlays/; cp arch/arm/boot/dts/overlays/README /boot/overlays/; cp arch/arm/boot/zImage /boot/kernel-v8-stockish.img
    fi
    for ver in A B C D E F G H; do
        if [ -e "/boot/kernel-v8-$ver.img" ]; then
            echo "Skipping $ver because we did it already"
        else
            echo "Building kernel variant $ver"
            test_optim $ver
        fi
    done
}





do_btrfs_prep() {
    apt -y install btrfs-tools
    umount /tmp/p4
    umount /tmp/p4
    umount /dev/mmcblk0p4
    umount /dev/mmcblk0p4
    umount /dev/mmcblk0p4
    mkfs.btrfs -f -L mybackup /dev/mmcblk0p4 || die "FAILED TO FORMAT BTRFS P4"
    mkdir -p /tmp/p2 /tmp/p4
    mount /dev/mmcblk0p2 /tmp/p2
    mount /dev/mmcblk0p1 /tmp/p2/boot
    mount /dev/mmcblk0p4 /tmp/p4 -o compress=lzo || die "FAILED TO PREP BRTFS P4"
    btrfs subvolume create /tmp/p4/@ || die "FAILED TO CREATE BTRFS P4 SNAPSHOT '@'"
    btrfs subvolume set-default $(btrfs subvolume list /tmp/p4 | cut -d' ' -f2) /tmp/p4
    umount /tmp/p4
    umount /tmp/p4
    mount /dev/mmcblk0p4 /tmp/p4 -o compress=lzo || die "FAILED TO RE-MOUNT BRTFS P4"
    rsync -av /tmp/p2/[a-z]* /tmp/p4/
}

remount_p4_p2_and_p1() {
    mkdir -p /tmp/p2 /tmp/p4
    mount /dev/mmcblk0p2 /tmp/p2
    mount /dev/mmcblk0p1 /tmp/p2/boot
    mount /dev/mmcblk0p4 /tmp/p4 -o compress=lzo
}


snappit() {
    echo "Sync'ing..."
    remount_p4_p2_and_p1
    rsync --del -av /tmp/p2/* /tmp/p4/
    btrfs subvolume snapshot /tmp/p4/ /tmp/p4/"$1" || die "FAILED TO MAKE $1 SNAPSHOT"
}


shave_three_seconds_off_boot() {
    apt -y --purge remove plymouth cups cups-browsed cups-client cups-common cups-core-drivers cups-daemon cups-filters cups-filters-core-drivers cups-ipp-utils cups-pk-helper cups-ppdc cups-server-common hplip printer-driver-gutenprint printer-driver-hpcups
    cat << 'EOF' > /usr/local/sbin/launch_x11_and_ratpoison
#!/bin/bash
# -retro -rw -background # https://www.computerhope.com/unix/ux.htm
/usr/bin/X -retro -nolisten &
for i in {1..999}; do
    DISPLAY=:0 xhost +
    DISPLAY=:0 xset s off
    DISPLAY=:0 xset -dpms
    DISPLAY=:0 xset s 0 0
    DISPLAY=:0 xset s noblank
    DISPLAY=:0 systemd-inhibit su -l m -c "DISPLAY=:0 /home/m/autorun" >> /tmp/log.txt 2>> /tmp/log.txt
    sleep 0.4
done
exit 0
EOF
    chmod +x /usr/local/sbin/launch_x11_and_ratpoison
    cat << 'EOF' > /etc/systemd/system/x11_and_ratpoison.service
[Unit]
Description=Launch X11 and Ratpoison
Before=local-fs-pre.target
After=slices.target
DefaultDependencies=no

[Service]
ExecStart=/usr/local/sbin/launch_x11_and_ratpoison
Type=simple

[Install]
WantedBy=sysinit.target
EOF
    systemctl enable x11_and_ratpoison
    systemctl disable display-manager
}
    
    



run_pi0circle_screen_installer() {
    cat << 'SSS' > /home/m/.pi0s.sh
#!/bin/bash
mkdir -p ~/Downloads
cd ~/Downloads
git clone https://github.com/pimoroni/hyperpixel2r

cd hyperpixel2r
sudo ./install.sh
exit
SSS
    su -l -c "bash /home/m/.pi0s.sh"
}

run_home_tweaker_script() {
    cat << 'RRR' > /home/m/.m.sh
mememe() {
cat <<EOF > ~/.emptycursor
#define nn1_width 16
#define nn1_height 16
static unsigned char nn1_bits[] = {
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};
EOF
cat <<EOF > ~/.ratpoisonrc
set border 0
set startupmessage 0
exec xset s off
exec xset -dpms
exec xset s 0 0
exec xset s noblank
exec xsetroot -cursor /home/m/.emptycursor /home/m/.emptycursor
exec ~/autorun
EOF
cd ~/Music
wget "https://cdn.pixabay.com/download/audio/2022/03/20/audio_90d59efbe6.mp3?filename=computer-startup-music-97699.mp3" -O startup.mp3
wget https://freetestdata.com/wp-content/uploads/2021/09/Free_Test_Data_1MB_MP3.mp3
echo "When prompted, please choose a password - for VNC server - and enter it twice. Then, press Ctrl-C."
tightvncserver
sed -i s/#x-window-manager/wmaker/ ~/.vnc/xstartup
sudo systemctl start myvnc
ln -sf /usr/bin/xeyes ~/autorun
sudo systemctl enable myvnc
echo "/usr/bin/ratpoison" > ~/.xsession
chmod +x ~/.xsession
}
mememe
exit

RRR
    chmod +x /home/m/.m.sh
    chown m:m /home/m/.m.sh
    su -l m "/home/m/.m.sh"
}


rollback() {
    if [ "$1" == "" ]; then
        echo "PLEASE SPECIFY SNAPSHOT"
    else
        mkdir -p /tmp/p2 /tmp/p4
        mount /dev/mmcblk0p2 /tmp/p2 2> /dev/null
        mount /dev/mmcblk0p1 /tmp/p2/boot 2> /dev/null
        mount /dev/mmcblk0p4 /tmp/p4 -o compress=lzo 2> /dev/null
        rsync -av --del --exclude=tmp /tmp/p4/"$1"/{bin,boot,etc,home,lib,opt,root,sbin,srv,usr,var} /tmp/p2/
    fi
}


do_my_hip_thang() {
    local jjjj=$1
    remount_p4_p2_and_p1
    if [ -e "/tmp/p4/@after_$jjjj" ]; then
        echo "Skipping @after_$jjjj -- we already have a snapshot"
        last_good_snapshot=@after_$jjjj
    else
        if [ "$last_good_snapshot" != "" ]; then
            echo "Rolling back to $last_good_snapshot"
            rollback $last_good_snapshot
            last_good_snapshot=""
        fi
        $jjjj
        snappit "@"after_"$jjjj"
    fi
}


############################################


last_good_snapshot=""
do_primaries
do_btrfs_prep
add_rollmeback_script

echo "DOING MY HIP THANG"
do_my_hip_thang install_the_software
do_my_hip_thang compile_and_install_kernel_and_modules
do_my_hip_thang purge_crap
do_my_hip_thang configure_stuff
do_my_hip_thang run_home_tweaker_script
do_my_hip_thang run_pi0circle_screen_installer
#do_my_hip_thang shave_three_seconds_off_boot

if [ "$last_good_snapshot" != "" ]; then
    $last_good_snapshot
    last_good_snapshot=""
fi

mkdir -p /tmp/p2 /tmp/p4
mount /dev/mmcblk0p2 /tmp/p2 2> /dev/null
mount /dev/mmcblk0p1 /tmp/p2/boot 2> /dev/null
mount /dev/mmcblk0p4 /tmp/p4 -o compress=lzo 2> /dev/null
for i in $(btrfs subvolume list /tmp/p4 | cut -d' ' -f9); do
    cp /usr/local/sbin/rollmeback /tmp/p4/$i/usr/local/sbin/
done


