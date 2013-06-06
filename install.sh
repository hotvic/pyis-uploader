#!/bin/bash
# -*- coding: UTF-8 -*-
# 
# Copyright © 2012, 2013 Victor Aurélio <victoraur.santos@gmail.com>
#
# This file is part of PyIS-Uploader.
#
# PyIS-Uploader is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyIS-Uploader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

## Setup script to PyIS-Uploader

LOCALES="en es pt_BR"

msg2() {
    echo -e "\033[32m==>\033[0m $1"
}

msg3() {
    echo -e "\033[33m===>\033[0m $1"
}
error() {
    echo "Error, exiting..."
    exit 1
}

show_help() {
    cat << !EOF
Usage: ./install.sh [Options] [Command]
Options:
  --prefix  :        Installation prefix
  --help    :        Show this help message
Commands:
  install   :        Install program
  uninstall :        Uninstall program (need --prefix)
!EOF
}

compileLocale() {
	msg2 "Compiling locale..."

	if [ ! -d .temp ]; then
		mkdir .temp
	fi
	cd .temp
	for loc in $LOCALES; do
		msg3 "Compiling locale '$loc'..."
		msgfmt -o ${loc}.mo ../locale/${loc}.po
	done

	cd ..
	msg2 "Locale compiled!"
}

install_app() {
    if [ -z $DESTDIR ]; then
        DESTDIR=$1
    else
        msg2 "Using $DESTDIR as destination directory..."
    fi

    if [ -d $DESTDIR ] && [ ! -w $DESTDIR ]; then
        echo "You don't have permission to write to $DESTDIR"
        exit 1
    fi

    msg2 "Installing..."
    ## Install executable

    if [ ! -d $DESTDIR/bin/ ]; then
        install -d $DESTDIR/bin/
    fi
    if [ ! -d $DESTDIR/lib/ ]; then
        install -d $DESTDIR/lib/pyis-uploader
    fi
    msg3 "Installing $DESTDIR/bin/pyis-uploader ..."
    echo "#!/bin/sh" > $DESTDIR/bin/pyis-uploader
    echo "" >> $DESTDIR/bin/pyis-uploader
    echo "python2 $DESTDIR/lib/pyis-uploader/pyis_uploader.py \$@" >> $DESTDIR/bin/pyis-uploader
    chmod 755 $DESTDIR/bin/pyis-uploader
    msg3 "Installing $DESTDIR/lib/pyis-uploader/pyis_uploader.py ..."
    install -Dm644 pyis_uploader.py $DESTDIR/lib/pyis-uploader/pyis_uploader.py || error
    msg3 "Installing $DESTDIR/lib/pyis-uploader/utils.py ..."
    install -Dm644 utils.py $DESTDIR/lib/pyis-uploader/utils.py || error
    msg3 "Installing $DESTDIR/lib/pyis-uploader/config.py ..."
    install -Dm644 config.py $DESTDIR/lib/pyis-uploader/config.py || error
    msg3 "Installing $DESTDIR/lib/pyis-uploader/isup.py ..."
    install -Dm644 isup.py $DESTDIR/lib/pyis-uploader/isup.py || error

    ## Install locale

	compileLocale
    if [ ! -d $DESTDIR/share/locale ]; then
        install -d $DESTDIR/share/locale
    fi
    for loc in $LOCALES; do
        msg3 "Installing $DESTDIR/share/locale/${loc}/LC_MESSAGES/pyis-uploader.mo ..."
        if [ ! -d $DESTDIR/share/locale/${loc}/LC_MESSAGES/ ]; then
            install -d $DESTDIR/share/locale/${loc}/LC_MESSAGES/
    fi
        install .temp/${loc}.mo $DESTDIR/share/locale/${loc}/LC_MESSAGES/pyis-uploader.mo || error
    done

    ## Install man page
    msg3 "Installing man page to $DESTDIR/share/man/man1/ ..."
    if [ ! -d $DESTDIR/share/man/man1 ]; then
        install -d $DESTDIR/share/man/man1
    fi
    install -m0644 docs/pyis-uploader.1 $DESTDIR/share/man/man1/ || error
    gzip $DESTDIR/share/man/man1/pyis-uploader.1 || error

	rm -rf .temp
    msg2 "Installation successfully"
}

uninstall_app() {
    if [ -z $DESTDIR ]; then
        DESTDIR=$1
    else
        msg2 "Using $DESTDIR as destination directory ..."
    fi

    if [ -d $DESTDIR ] && [ ! -w $DESTDIR ]; then
        echo "You don't have permission to write to $DESTDIR"
        exit 1
    fi

    msg2 "Uninstalling..."
    ## uninstall executable

    if [ -f $DESTDIR/bin/pyis-uploader ]; then
        msg3 "Uninstalling $DESTDIR/bin/pyis-uploader ..."
        rm $DESTDIR/bin/pyis-uploader
    else
        msg3 "Warning: Unable to find $DESTDIR/bin/pyis-uploader, ignoring..."
    fi

    ## Uninstall python files
    if [ -d $DESTDIR/lib/pyis-uploader ]; then
        msg3 "Uninstalling $DESTDIR/lib/pyis-uploader ..."
        rm -rf $DESTDIR/lib/pyis-uploader
    fi
    
    ## Uninstall locale

    for loc in $LOCALES; do
        msg3 "Uninstalling $DESTDIR/share/locale/${loc}/LC_MESSAGES/pyis-uploader.mo ..."
        if [ -f $DESTDIR/share/locale/${loc}/LC_MESSAGES/pyis-uploader.mo ];then
            rm $DESTDIR/share/locale/${loc}/LC_MESSAGES/pyis-uploader.mo
        else
            msg3 "Warning: Unable to find $DESTDIR/share/locale/${loc}/LC_MESSAGES/pyis-uploader.mo, ignoring..."
        fi
    done

    ## Uinstall man page(s)
    if [ -f $DESTDIR/share/man/man1/pyis-uploader.1.gz ]; then
        msg3 "Uninstalling $DESTDIR/share/man/man1/pyis-uploader.1.gz ..."
        rm $DESTDIR/share/man/man1/pyis-uploader.1.gz
    fi

    msg2 "Uninstallation successfully"
}

passArgs() {
    TEMP=$(getopt -u -n "PyIS-Uploader Install" -l "prefix: help" -o "h" -- "$@")
    if [ $? -ne 0 ]; then
        echo $TEMP >&2
        exit 1
    fi
    set -- $TEMP
    prefix= help= action=
    while true ; do
        case "$1" in
            --prefix)
                prefix="$2"
                shift 2
                ;;
            --help|-h)
                help=1
                shift
                ;;
            --)
                shift
                break
                ;;
            *)
        esac
    done
    for arg do
        case "$arg" in
            install)
                action="install"
                ;;
            uninstall)
                action="uninstall"
                ;;
            *)
                help=1
        esac
    done
    if [ ! -z $help ]; then
        show_help
        exit
    fi
    if [ -z $prefix ]; then
        msg3 "WARNING: Using default prefix: /usr"
        prefix="/usr"
    else
        LAST=$(echo $prefix | sed -re 's/.*(.)$/\1/')
        if [ "$LAST" == "/" ]; then
            PREFIX=$(echo $prefix | sed -re 's/(.*).$/\1/')
        fi
    fi
    if [ -z $action ]; then
        show_help
    fi

    case "$action" in
        install)
            msg2 "Using $prefix as prefix..."
            install_app $prefix
            ;;
        uninstall)
            msg2 "Using $prefix as prefix..."
            uninstall_app $prefix
            ;;
        *)
    esac
}

passArgs $@
