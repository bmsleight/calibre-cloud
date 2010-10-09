#!/bin/bash

#installation

apt-get --assume-yes purge sendmail*
apt-get --assume-yespurge apache2*

apt-get update
apt-get --assume-yes install language-pack-en
apt-get --assume-yes install xvfb x11vnc matchbox matchbox-themes-extra python-django sqlite3 python-pysqlite2 apache2-mpm-prefork libapache2-mod-wsgi libapache2-mod-proxy-html python-django xdg-utils subversion python-pexpect

mkdir /usr/share/desktop-directories/
mkdir -p /usr/share/icons/hicolor/

