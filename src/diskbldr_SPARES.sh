

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
    cat /root/fb0.img > /dev/fb0
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














ugly_hack_to_speed_up_boot() {
    cat << 'EOF' > /etc/systemd/system/palpac.service
[Unit]
Description=PALPAC Launcher Including X
Before=local-fs-pre.target
After=slices.target
DefaultDependencies=no

[Service]
ExecStart=/usr/bin/startx /usr/bin/ratpoison
Type=simple
Restart=always
RestartSec=5s

[Install]
WantedBy=sysinit.target
EOF

    cat << 'EOF' > /root/.ratpoisonrc 
set border 0
set startupmessage 0
exec xset s off
exec xset -dpms
exec xsetroot -cursor /home/m/.emptycursor /home/m/.emptycursor
exec /usr/local/bin/palpac
EOF

    cat << 'EOF' > /usr/local/bin/palpac
#!/bin/bash

if [ "$USER" == "root" ]; then
    xhost +
    su -l m -c "DISPLAY=:0 $0"
    exit $?
else
    /home/m/autorun &
fi
EOF

    cat << 'EOF' > /root/.ratpoisonrc 
set border 0
set startupmessage 0
exec xset s off
exec xset -dpms
exec xsetroot -cursor /home/m/.emptycursor /home/m/.emptycursor
exec /usr/local/bin/palpac
EOF

    chmod +x /usr/local/bin/palpac
    systemctl daemon-reload
    systemctl set-default multi-user.target
    systemctl enable palpac
    systemctl disable raspi-config
    systemctl disable ModemManager
    [ -e "/etc/X11/xinit/xserverrc" ] && cp -f /etc/X11/xinit/xserverrc /etc/X11/xinit/xserverrc.normal
    echo "exec /usr/bin/X -background none -nolisten tcp \"\$@\"" > /etc/X11/xinit/xserverrc
    chmod +x /etc/X11/xinit/xserverrc
    cat << 'EOF' > /usr/local/bin/goregular
#!/bin/sh

systemctl disable palpac
systemctl set-default graphical.target
EOF
    chmod +x /usr/local/bin/goregular
    systemctl disable getty@tty3
}


