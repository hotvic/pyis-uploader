#!/bin/sh

## Setup script to PyIS-Uploader

## 
#* This file is part of PyIS-Upload, licensed
#* under GNU GPL at version 3 or any other(at you preference) version.
##

LOCALES="en es pt_BR"

msg2(){
    echo -e "\033[32m==>\033[0m $1"
}

msg3(){
    echo -e "\033[33m===>\033[0m $1"
}
error(){
    echo "Error, exiting..."
    exit 1
}

compileLocale(){
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

install_app(){
    if [ -z $DESTDIR ]; then
        DESTDIR=$1
    else
        msg2 "Using $DESTDIR as destination directory..."
    fi

    if [ -d $DESTDIR ] && [ ! -w $DESTDIR ]; then
        echo "You no have permission to write to $DESTDIR"
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
    echo "python2 $DESTDIR/lib/pyis-uploader/pyis_uploader.py $@" >> $DESTDIR/bin/pyis-uploader
    chmod 755 $DESTDIR/bin/pyis-uploader
    msg3 "Installing $DESTDIR/lib/pyis-uploader/pyis_uploader.py ..."
    install -Dm=644 pyis_uploader.py $DESTDIR/lib/pyis-uploader/pyis_uploader.py || error
    msg3 "Installing $DESTDIR/lib/pyis-uploader/utils.py ..."
    install -Dm=644 utils.py $DESTDIR/lib/pyis-uploader/utils.py || error
    msg3 "Installing $DESTDIR/lib/pyis-uploader/config.py ..."
    install -Dm=644 config.py $DESTDIR/lib/pyis-uploader/config.py || error
    msg3 "Installing $DESTDIR/lib/pyis-uploader/isup.py ..."
    install -Dm=644 isup.py $DESTDIR/lib/pyis-uploader/isup.py || error

    ## Install locale

	compileLocale
    if [ ! -d $DESTDIR/share/locale ]; then
        install -d $DESTDIR/share/locale
    fi
    for loc in $LOCALES; do
        msg3 "Installing $DESTDIR/share/${loc}/LC_MESSAGES/pyis-uploader.mo ..."
        if [ ! -d $DESTDIR/share/${loc}/LC_MESSAGES/ ]; then
            install -d $DESTDIR/share/${loc}/LC_MESSAGES/
    fi
        install .temp/${loc}.mo $DESTDIR/share/${loc}/LC_MESSAGES/pyis-uploader.mo || error
    done

    ## Install man page
    msg3 "Installing man page to $DESTDIR/share/man/man1/ ..."
    if [ ! -d $DESTDIR/share/man/man1 ]; then
        install -d $DESTDIR/share/man/man1
    fi
    install -m 0644 docs/pyis-uploader.1 $DESTDIR/share/man/man1/ || error
    gzip $DESTDIR/share/man/man1/pyis-uploader.1 || error

	rm -rf .temp
    msg2 "Installation successfully"
}

uninstall_app(){
    if [ -z $DESTDIR ]; then
        DESTDIR=$1
    else
        msg2 "Using $DESTDIR as destination directory ..."
    fi

    if [ -d $DESTDIR ] && [ ! -w $DESTDIR ]; then
        echo "You no have permission to write to $DESTDIR"
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
    rm -rf $DESTDIR/lib/pyis-uploader
    
    ## Uninstall locale

    for loc in $LOCALES; do
        msg3 "Uninstalling $DESTDIR/share/${loc}/LC_MESSAGES/pyis-uploader.mo ..."
        if [ -f $DESTDIR/share/${loc}/LC_MESSAGES/pyis-uploader.mo ];then
            rm $DESTDIR/share/${loc}/LC_MESSAGES/pyis-uploader.mo
        else
            msg3 "Warning: Unable to find $DESTDIR/share/${loc}/LC_MESSAGES/pyis-uploader.mo, ignoring..."
        fi
    done

    msg2 "Uninstallation successfully"
}

passArgs(){
    for i in $@; do
        if [[ $i = "--prefix="* ]]; then
            PREFIX=$(echo $i | sed -re 's#\-\-prefix\=(.*)#\1#')
            LAST=$(echo $PREFIX | sed -re 's/.*(.)$/\1/')
            if [[ $LAST = "/" ]]; then
                PREFIX=$(echo $PREFIX | sed -re 's/(.*).$/\1/')
            fi
        elif [[ $i = "--help" ]]; then
            cat << !
Usage: ./install.sh [Options] [Command]
Options:
  --prefix  :        Installation prefix
  --help    :        Show this help message
Commands:
  install   :        Install program
  uninstall :        Uninstall program (need --prefix)
!
        elif [[ $i = "install" ]]; then
            msg2 "Using $PREFIX as prefix..."
            install_app $PREFIX
        elif [[ $i = "uninstall" ]]; then
            msg2 "Using $PREFIX as prefix..."
            uninstall_app $PREFIX
        else
            msg3 "Unknown command or option: $i"
            error
        fi
    done
}

if [ $# -gt 1 ]; then 
	passArgs $@
else
	passArgs '--help'
fi
