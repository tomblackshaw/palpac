

cat << 'EOF' > /etc/systemd/system/splash.service
Description=PALPAC Launcher Including X
Before=local-fs-pre.target
After=slices.target
DefaultDependencies=no

[Service]
ExecStart=/bin/cp /img /dev/fb0
Type=simple
#Restart=always
#RestartSec=5s

[Install]
WantedBy=sysinit.target
EOF
systemctl enable splash
[ -e "/etc/X11/xinit/xserverrc.BEFORE" ] || cp /etc/X11/xinit/xserverrc /etc/X11/xinit/xserverrc.BEFORE
echo "exec /usr/bin/X -background none -nolisten tcp \"\$@\"" > /etc/X11/xinit/xserverrc
chmod +x /etc/X11/xinit/xserverrc
    






cat << 'EOF' > /.myinit.sh
#!/bin/sh

first() {
    mount -t proc proc /proc
    mount -t sysfs sys /sys
    mount -t tmpfs tmp /run
    mkdir -p /run/systemd
    mount /boot
#    sed -i 's| init=/.myinit.sh||' /boot/cmdline.txt
    mount / -o remount,rw
}

second() {
    mount /boot -o remount,ro
    sync
    echo 1 > /proc/sys/kernel/sysrq
    umount /boot
    mount / -o remount,ro
    sync
    echo b > /proc/sysrq-trigger
    sleep 5
}
    
main() {
    echo hi > /.pay.txt || echo oh
    echo "PAYLOAD: $(date)" > /boot/.pay.txt || echo dear
    echo "MORE PAY: $(date)" > /.pay.txt || echo dear
    mv /dev/fb0 /dev/fb0.orig
    mv /dev/fb1 /dev/fb0
    fbi -a --noverbose -T 1 -d /dev/fb0.orig /boot/splash.png
    exec /sbin/init
    exit $?
}

first
main
second
exit 0
EOF
rm -f /boot/.pay* /.pay*
chmod +x /.myinit.sh

