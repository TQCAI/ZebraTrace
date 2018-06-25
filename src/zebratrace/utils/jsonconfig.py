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


import codecs
import json
import os
import sys

from . import unicode


def _encode(data):
    if isinstance(data, unicode):
        data = data.encode('utf-8')

    if isinstance(data, bytes):
        data = data.decode('utf-8')
    elif isinstance(data, list):
        data = _encode_list(data)
    elif isinstance(data, dict):
        data = _encode_dict(data)
    return data


def _encode_list(data):
        rv = []
        for item in data:
            rv.append(_encode(item))
        return rv


def _encode_dict(data):
        rv = {}
        #for key, value in data.iteritems():
        for key, value in data.items():
            if isinstance(key, unicode):
                key = key.encode('utf-8').decode('utf-8')
            rv[key] = _encode(value)
        return rv


class JsonConfigParser(object):

    def update(self, cnf=None):
        if cnf:
            self.__dict__.update(cnf)

    def load(self, filename=None):
        if os.path.exists(filename):
            try:
                with codecs.open(filename, mode='r', encoding='utf-8') as f:
                    dic = f.read()
                dic = json.loads(dic, object_hook=_encode_dict)
                self.update(dic)
            except (IOError, os.error):
                err = sys.exc_info()[1]
                print(err)

    def save(self, filename=None):
        if len(self.__dict__) == 0 or filename is None:
            return
        try:
            s = json.dumps(self.__dict__, ensure_ascii=False, indent=2)
            with codecs.open(filename, mode='w', encoding='utf-8') as f:
                f.write(s)
        except (IOError, os.error):
            err = sys.exc_info()[1]
            print(err)
