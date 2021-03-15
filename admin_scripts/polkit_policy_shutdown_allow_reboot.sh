#!/usr/bin/env bash

#================================================================
# HEADER
#================================================================
#% SYNOPSIS
#+    polkit_policy_shutdown_allow_reboot.sh [ENFORCE]
#%
#% DESCRIPTION
#%    This script installs a mandatory PolicyKit policy that prevents the
#%    "user" or "lightdm" users from sleeping, hibernating or
#%    shutting down the system. ALLOW rebooting.
#%
#%    It takes one optional parameter: whether or not to enforce this policy.
#%    If this parameter is missing, empty, "false", or "falsk", the policy will
#%    be removed; otherwise, it will be enforced.
#%
#================================================================
#- IMPLEMENTATION
#-    version         polkit_policy_shutdown.sh (magenta.dk) 1.0.0
#-    author          Alexander Faithfull and Carsten Agger
#-    copyright       Copyright 2019, 2020, 2021 Magenta ApS
#-    license         BSD 2 Clause 
#-    email           af@magenta.dk
#-
#================================================================
#  HISTORY
#     2019/09/25 : af : dconf_policy_shutdown.sh created
#     2020/01/27 : af : This script created based on dconf_policy_shutdown.sh
#     2020/01/27 : ca : This script created based on polkit_policy_shutdown.sh
#
#================================================================
# END_OF_HEADER
#================================================================

set -x

POLICY="/etc/polkit-1/localauthority/90-mandatory.d/10-os2borgerpc-no-user-shutdown.pkla"

if [ "$1" = "" -o "$1" = "false" -o "$1" = "falsk" -o "$1" = "nej" ]; then
    rm -f "$POLICY"
else
    if [ ! -d "`dirname "$POLICY"`" ]; then
        mkdir "`dirname "$POLICY"`"
    fi

    cat > "$POLICY" <<END
[Restrict system shutdown]
Identity=unix-user:user;unix-user:lightdm
Action=org.freedesktop.login1.hibernate*;org.freedesktop.login1.power-off*;org.freedesktop.login1.suspend*;org.freedesktop.login1.lock-sessions
ResultAny=no
ResultActive=no
ResultInactive=no
END
fi

# PolicyKit is supposed to monitor the /etc/polkit-1/localauthority folder, but
# err on the side of caution and restart the service
systemctl restart polkit.service
