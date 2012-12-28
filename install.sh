## Setup script to pyih-uploader

if [ $UID -ne 0 ]; then
	echo "You need root access to install this program, exiting..."
	exit 1
fi

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
		cat << HELP
Usage: ./install.sh [Options]
Options:
  --prefix  :       Installation prefix
  --help    :       Show this help message
HELP
	fi
done

error(){
	echo "Error, exiting..."
	exit 1
}
echo "Installing..."
## Install executable

if [ ! -d ${PREFIX}/bin/ ]; then
	install -d ${PREFIX}/bin/
fi
echo "===> Installing ${PREFIX}/bin/pyih-uploader ..."
install -Dm=755 pyih-uploader.py ${PREFIX}/bin/pyih-uploader || error
## Install locale

if [ ! -d ${PREFIX}/share/locale ];then
	install -d ${PREFIX}/share/locale
fi
for dir in $(ls locale); do
	echo "===> Installing ${PREFIX}/share/locale/${dir}/LC_MESSAGES/pyih-uploader.mo ..."
	install locale/${dir}/LC_MESSAGES/pyih-uploader.mo ${PREFIX}/share/locale/${dir}/LC_MESSAGES/pyih-uploader.mo || error
done
echo "Installation successfully"

