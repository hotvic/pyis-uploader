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
  --prefix    :       Installation prefix
  --help      :       Show this help message
HELP
	fi
done

error(){
	echo "Error, exiting..."
	exit 1
}
echo "Installing..."
install -Dm=755 pyih-uploader.py ${PREFIX}/bin/pyih-uploader || error
echo "Installation successfully"

