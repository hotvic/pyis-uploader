# -*- coding: UTF-8 -*-
#
# Copyright © 2014 Victor A. Santos <victoraur.santos@gmail.com>
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

import os

def get_ui_path(ui):
    rel_ui = os.path.dirname(os.path.abspath(__file__)) + '/ui/'
    if os.path.isdir(rel_ui):
        return rel_ui + ui