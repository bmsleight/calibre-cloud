#!/bin/bash

#installation


#Skip if not needed...
#dd if=/dev/zero of=/swap bs=1024 count=1048576
#mkswap /swap
#chmod 0600 /swap
#echo "/swap            swap          swap     defaults,noatime           0 0" >>/etc/fstab

## deb http://archive.ubuntu.com/ubuntu lucid main
## deb http://security.ubuntu.com/ubuntu lucid-security main

##deb http://archive.ubuntu.com/ubuntu lucid main restricted universe
##deb http://archive.ubuntu.com/ubuntu lucid-updates main restricted universe
##deb http://archive.ubuntu.com/ubuntu lucid-security main restricted universe



echo "Password for the user cloud ? "
read PASSWORD_USER
echo "Password for the user cloud, when uploading (send in cleartext over http) ? "
read PASSWORD_CLEAR

apt-get --assume-yes purge sendmail*
apt-get --assume-yes purge apache2*
#apt-get --assume-yes purge rsyslog
#apt-get --assume-yes purge consolekit

apt-get update
apt-get --assume-yes install language-pack-en
apt-get --assume-yes install xvfb x11vnc matchbox matchbox-themes-extra python-django sqlite3 python-pysqlite2 apache2-mpm-prefork libapache2-mod-wsgi libapache2-mod-proxy-html python-django xdg-utils subversion python-pexpect imagemagick

# Get the Desktop icons cleaned.
mkdir /usr/share/desktop-directories/
mkdir -p /usr/share/icons/hicolor/
rm /usr/share/applications/python2.6.desktop /usr/share/applications/defaults.list /usr/share/applications/mb-* /usr/share/applications/x11vnc.desktop

cd /tmp/
rm /tmp/setup*
wget http://calibre-cloud.googlecode.com/svn/trunk/install/setup.py
python /tmp/setup.py --password="$PASSWORD_USER" --clear="$PASSWORD_CLEAR"

echo password="$PASSWORD_USER" clear="$PASSWORD_CLEAR" >/root/cloud.txt

echo "If the above reads: **** SETUP Ran with no errors **** "
echo "Then everything was fine."
cp /home/cloud/calibre-cloud-read-only/install/startvnc.sh /root/startvnc.sh
echo "/bin/bash /root/startvnc.sh &" > /etc/rc.local

echo "To start the services running, enter the following command :-"
echo "nohup /bin/bash /root/startvnc.sh &"
echo "... or reboot via the VPS control panel."

