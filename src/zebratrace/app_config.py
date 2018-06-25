#    Copyright 2018 Maxim.S.Barabash <maxim.s.barabash@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import locale
from os import makedirs
from os.path import join, expanduser, abspath, dirname, lexists
import sys
import tempfile

from . import event, __version__
from .utils import unicode, id_generator
from .utils.jsonconfig import JsonConfigParser


default_preset = {
  "funcX": "(0.95+0.02*sin(20*a))*i/n",
  "funcY": "",
  "rangeMax": 6.28318530718,
  "rangeMin": 0.0,
  "polar": 0,
  "resolution": 1.0,
}

default_config = {
  "currentPath": "",
  "presetPath": "",
  "trace_image": "",
  "numberCurves": 80,
  "curveWidthMin": 1,
  "curveWidthMax": 5,
  "nodeReduction": 0,
  "sliderTransparency": 80,
  "curveWriting": 0,
  "boxAdvancedPref": False,
  "units": 0,
  "previewMode": 0,
  "dpi": 90.0,
}

TEMP_PREFIX = "TRACE_"


class AppData:
    app_name = "ZebraTRACE"
    app_version = __version__
    lang, enc = locale.getdefaultlocale()

    app_dir = dirname(abspath(sys.argv[0]))
    app_config_dir = join("~", ".config", "zebratrace")
    app_config_dir = expanduser(app_config_dir)

    if sys.version_info < (3,):
        app_config_dir = unicode(app_config_dir, sys.getfilesystemencoding())
        app_dir = unicode(app_dir, sys.getfilesystemencoding())

    if not lexists(app_config_dir):
        makedirs(app_config_dir)

    app_config_fn = unicode(join(app_config_dir, "preferences.cfg"))
    translations_dir = unicode(join(app_dir, "translations"))
    preset_dir = unicode(join(app_dir, "preset"))
    temp_dir = tempfile.gettempdir()
    temp_svg = unicode(join(temp_dir, TEMP_PREFIX +
                            id_generator() + ".svg"))
    help_index = unicode("http://github.com/maxim-s-barabash/ZebraTrace/wiki")


class Preset(JsonConfigParser):
    def __init__(self):
        self.update(default_preset)


class AppConfig(JsonConfigParser):
    def __init__(self):
        self.update(default_config)
        self.update(default_preset)

    def load(self, filename=None):
        JsonConfigParser.load(self, filename=filename)
        event.emit(event.CONFIG_LOADED)

    def __setattr__(self, name, value):
        self.__dict__[name] = value
        event.emit(event.CONFIG_CHANGED)
