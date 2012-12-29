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
	if [ $UID -ne 0 ]; then
		echo "You need root access to install this program, exiting..."
		exit 1
	fi

	msg2 "Installing..."
	## Install executable

	if [ ! -d $1/bin/ ]; then
		install -d $1/bin/
	fi
	msg3 "Installing $1/bin/pyih-uploader ..."
	install -Dm=755 pyih-uploader.py $1/bin/pyih-uploader || error

	## Install locale

	if [ ! -d $1/share/locale ];then
		install -d $1/share/locale
	fi
	for dir in $(ls locale); do
		msg3 "Installing $1/share/locale/${dir}/LC_MESSAGES/pyih-uploader.mo ..."
		install locale/${dir}/LC_MESSAGES/pyih-uploader.mo $1/share/locale/${dir}/LC_MESSAGES/pyih-uploader.mo || error
	done

	msg2 "Installation successfully"
}

uninstall_app(){
	if [ $UID -ne 0 ]; then
		echo "You need root access to install this program, exiting..."
		exit 1
	fi

	msg2 "Uninstalling..."
	## uninstall executable

	if [ -f $1/bin/pyih-uploader ]; then
		msg3 "Uninstalling $1/bin/pyih-uploader ..."
		rm $1/bin/pyih-uploader
	else
		msg3 "Warning: Unable to find $1/bin/pyih-uploader, ignoring..."
	fi

	## Uninstall locale

	for dir in $(ls locale); do
		msg3 "Uninstalling $1/share/locale/${dir}/LC_MESSAGES/pyih-uploader.mo ..."
		if [ -f $1/share/locale/${dir}/LC_MESSAGES/pyih-uploader.mo ];then
			rm $1/share/locale/${dir}/LC_MESSAGES/pyih-uploader.mo
		else
			msg3 "Warning: Unable to find $1/share/locale/${dir}/LC_MESSAGES/pyih-uploader.mo, ignoring..."
		fi
	done

	msg2 "Uninstallation successfully"
}

passArgs(){
	for i in $@; do
		PREFIX="/usr"
		if [[ $i = "--prefix="* ]]; then
			PREFIX=$(echo $i | sed -re 's#\-\-prefix\=(.*)#\1#')
			LAST=$(echo $PREFIX | sed -re 's/.*(.)$/\1/')
			if [[ $LAST = "/" ]]; then
				PREFIX=$(echo $PREFIX | sed -re 's/(.*).$/\1/')
			fi
			echo "Using $PREFIX as prefix..."
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
			install_app $PREFIX
		elif [[ $i = "uninstall" ]]; then
			uninstall_app $PREFIX
		fi
	done
}

passArgs $@
