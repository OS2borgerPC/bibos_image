#!/bin/sh

#================================================================
# HEADER
#================================================================
#% SYNOPSIS
#+    network_up.sh
#%
#% DESCRIPTION
#%    This script installs or removes a pre-checkin hook that instructs
#%    NetworkManager to bring up all network connections known to the target
#%    machine.
#%
#================================================================
#- IMPLEMENTATION
#-    version         network_up.sh (magenta.dk) 1.0.0
#-    author          Alexander Faithfull
#-    copyright       Copyright 2021, Magenta ApS
#-    license         GNU General Public License
#-    email           af@magenta.dk
#-
#================================================================
#  HISTORY
#     2021/03/12 : af : Script created
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

HOOKS="/etc/os2borgerpc/pre-checkin.d/network_up.sh"

if [ "$1" != "" -a "$1" != "false" -a "$1" != "falsk" ]; then
    tee $HOOKS <<"END" > /dev/null
#!/bin/sh

nmcli() {
    command nmcli --terse --colors no "$@"
}

case "$1" in
    pre-checkin)
        nmcli radio wifi on
        nmcli networking on
        for device in $(
            nmcli --fields device,type device status \
                    | egrep '(wifi|ethernet)' \
                    | cut --delimiter : --fields 1); do
            nmcli device connect "$device" && break
        done ;;
    post-checkin)
        # nothing to do
        : ;;
    *)
        echo "$0: unknown or missing hook: $1" 1>&2 ;;
esac
END
    chmod +x $HOOKS
else
    rm -f $HOOKS
fi
