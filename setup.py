#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from distutils.core import setup

setup(name='pyis-uploader',
      version='0.2b',
      description='PyIS-Uploader (Python ImageShack Uploader) is small python2 program to upload images to ImageShack.',
      author='Victor Aurélio',
      author_email='victoraur.santos@gmail.com',
      url='https://github.com/hotvic/pyis-uploader',
      license='GPL3',
      package_dir={'': 'src'},
      packages=['pyis_uploader'],
      scripts=['src/pyis-uploader'])

