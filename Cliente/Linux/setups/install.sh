#!/bin/sh
PATHAPP=`find / -type f -and -name 'hardware_collector_linux.py' -and -size 7284c`
PATHHC=`dirname $PATHAPP`
DAEMON="/etc/init.d/hardware-collector-daemon"
$(cp -R $PATHHC /usr/share/hardware-collector-linux)
cp $PATHHC/setups/hardware-collector-daemon $DAEMON
chmod +x $DAEMON
