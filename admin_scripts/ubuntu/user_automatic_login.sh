#!/usr/bin/env bash

set -ex

if [ "$1" == "--disable" ] 
then
    # Disable autmatic login
    if id -nG user | grep -qw nopasswdlogin
    then
        deluser user nopasswdlogin
    fi
    sed -i "/autologin-user/d" /etc/lightdm/lightdm.conf
elif [ "$1" == "--enable" ]
then
    # Enable automatic login
    adduser user nopasswdlogin
    cat << EOF >> /etc/lightdm/lightdm.conf
autologin-user-timeout=10
autologin-user=user
EOF
else
    echo "Usage: user_automatic_login [--enable|--disable]"
fi


