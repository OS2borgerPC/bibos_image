#!/bin/sh

#================================================================
# HEADER
#================================================================
#% SYNOPSIS
#+    protect_config_files.sh
#%
#% DESCRIPTION
#%    This script installs or removes pre- and post-checkin hooks that
#%    together prevent OS2borgerPC configuration files from being modified.
#%
#%    It is only useful as an extra safeguard during certain remote upgrades.
#%
#================================================================
#- IMPLEMENTATION
#-    version         protect_config_files.sh (magenta.dk) 1.0.0
#-    author          Alexander Faithfull
#-    copyright       Copyright 2021, Magenta ApS
#-    license         GNU General Public License
#-    email           af@magenta.dk
#-
#================================================================
#  HISTORY
#     2021/03/15 : af : Script created
#
#================================================================
# END_OF_HEADER
#================================================================

set -x

if [ ! -f "/usr/local/bin/jobmanager.real" ]; then
    echo "This machine does not have jobmanager hook support"
    exit 1
fi
mkdir -p /etc/os2borgerpc/pre-checkin.d /etc/os2borgerpc/post-checkin.d

HOOKS="/etc/os2borgerpc/pre-checkin.d/protect_config_files.sh
/etc/os2borgerpc/post-checkin.d/protect_config_files.sh"

if [ "$1" != "" -a "$1" != "false" -a "$1" != "falsk" ]; then
    tee $HOOKS <<"END" > /dev/null
protected_files="/etc/bibos/bibos.conf /etc/os2borgerpc/os2borgerpc.conf"

case "$1" in
    pre-checkin)
        for i in $protected_files; do
            if [ -f "$i" ]; then
                echo "$0: backing up $i"
                cp --preserve=all "$i" "$i.bak"
            fi
        done ;;
    post-checkin)
        for i in $protected_files; do
            if [ -f "$i.bak" ]; then
                echo "$0: restoring backup of $i"
                mv "$i.bak" "$i"
            fi
        done ;;
    *)
        echo "$0: unknown or missing hook: $1" 1>&2 ;;
esac
END
    chmod +x $HOOKS
else
    rm -f $HOOKS
fi
