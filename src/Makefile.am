SUBDIRS = pyis_uploader

bin_SCRIPTS = pyis-uploader
CLEANFILES = $(bin_SCRIPTS)
EXTRA_DIST = pyis-uploader.in

do_substitution = sed -e 's,[@]PYTHON[@],$(PYTHON),g' \
    -e 's,[@]pythondir[@],$(pythondir),g'

pyis-uploader: pyis-uploader.in Makefile
	$(do_substitution) < $(srcdir)/pyis-uploader.in > pyis-uploader
	chmod +x pyis-uploader
