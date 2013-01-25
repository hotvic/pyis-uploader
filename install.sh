## Setup script to pyih-uploader

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
		install -d $DESTDIR/lib/pyih-uploader
	fi
	msg3 "Installing $DESTDIR/bin/pyih-uploader ..."
	echo "#!/bin/sh" > $DESTDIR/bin/pyih-uploader
	echo "cd $DESTDIR/lib/pyih-uploader/" >> $DESTDIR/bin/pyih-uploader
	echo 'python2 pyih-uploader.py $@' >> $DESTDIR/bin/pyih-uploader
	chmod 755 $DESTDIR/bin/pyih-uploader
	msg3 "Installing $DESTDIR/lib/pyih-uploader/pyih-uploader.py ..."
	install -Dm=644 pyih-uploader.py $DESTDIR/lib/pyih-uploader/pyih-uploader.py || error
	msg3 "Installing $DESTDIR/lib/pyih-uploader/utils.py ..."
	install -Dm=644 utils.py $DESTDIR/lib/pyih-uploader/utils.py || error

	## Install locale

	if [ ! -d $DESTDIR/share/locale ];then
		install -d $DESTDIR/share/locale
	fi
	for dir in $(ls locale); do
		msg3 "Installing $DESTDIR/share/locale/${dir}/LC_MESSAGES/pyih-uploader.mo ..."
		if [ ! -d $DESTDIR/share/locale/${dir}/LC_MESSAGES/ ]; then
			install -d $DESTDIR/share/locale/${dir}/LC_MESSAGES/
		fi
		install locale/${dir}/LC_MESSAGES/pyih-uploader.mo $DESTDIR/share/locale/${dir}/LC_MESSAGES/pyih-uploader.mo || error
	done

	## Install man page
	msg3 "Installing man page to $DESTDIR/share/man/man1/ ..."
	if [ ! -d $DESTDIR/share/man/man1 ]; then
		install -d $DESTDIR/share/man/man1
	fi
	install -m 0644 docs/pyih-uploader.1 $DESTDIR/share/man/man1/ || error
	gzip $DESTDIR/share/man/man1/pyih-uploader.1 || error

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

	if [ -f $DESTDIR/bin/pyih-uploader ]; then
		msg3 "Uninstalling $DESTDIR/bin/pyih-uploader ..."
		rm $DESTDIR/bin/pyih-uploader
	else
		msg3 "Warning: Unable to find $DESTDIR/bin/pyih-uploader, ignoring..."
	fi

	## Uninstall locale

	for dir in $(ls locale); do
		msg3 "Uninstalling $DESTDIR/share/locale/${dir}/LC_MESSAGES/pyih-uploader.mo ..."
		if [ -f $DESTDIR/share/locale/${dir}/LC_MESSAGES/pyih-uploader.mo ];then
			rm $DESTDIR/share/locale/${dir}/LC_MESSAGES/pyih-uploader.mo
		else
			msg3 "Warning: Unable to find $DESTDIR/share/locale/${dir}/LC_MESSAGES/pyih-uploader.mo, ignoring..."
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
Commands:
  install   :        Install program
  uninstall :        Uninstall program (need --prefix)
Options:
  --prefix  :        Installation prefix
  --help    :        Show this help message
!
		elif [[ $i = "install" ]]; then
			msg2 "Using $PREFIX as prefix..."
			install_app $PREFIX
		elif [[ $i = "uninstall" ]]; then
			msg2 "Using $PREFIX as prefix..."
			uninstall_app $PREFIX
		fi
	done
}

passArgs $@
