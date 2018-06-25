#    Copyright (C) 2011-2012 by Igor E. Novikov
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

"""
The package provides Qt-like signal-slot functionality
for internal events processing.
"""

CANCEL = False


# Signal channels

CONFIG_LOADED = ['CONFIG_LOADED']
CONFIG_CHANGED = ['CONFIG_CHANGED']

APP_STATUS = ['APP_STATUS']


NO_DOCS = ['NO_DOCS']
DOC_OPENED = ['DOC_OPENED']
DOC_EXPECTS = ['DOC_EXPECTS']
DOC_TRACE = ['DOC_TRACE']  # Trace the image started
DOC_MODIFIED = ['DOC_MODIFIED']
DOC_SAVED = ['DOC_SAVED']
DOC_CLOSED = ['DOC_CLOSED']


def connect(channel, receiver):
    """Connects signal receive method to provided channel.
    """
    if callable(receiver):
        try:
            channel.append(receiver)
        except:
            msg = 'Cannot connect to channel:'
            print("%s %s receiver: %s" % (msg, channel, receiver))


def disconnect(channel, receiver):
    """Disconnects signal receive method from provided channel.
    """
    if callable(receiver):
        try:
            channel.remove(receiver)
        except:
            msg = 'Cannot disconnect from channel:'
            print("%s %s receiver: %s" % (msg, channel, receiver))


def emit(channel, **args):
    """Sends signal to all receivers in channel.
    """
    for receiver in channel[1:]:
        if callable(receiver):
            receiver(**args)
'''    try:
        for receiver in channel[1:]:
            try:
                if callable(receiver):
                    receiver(*args)
            except Exception as e:
                msg = 'Cannot emit from channel:'
                print("%s %s receiver: %s" % (msg, channel, receiver))
                print(e)
    except:
        print('Cannot send signal to channel: %s' % channel)
'''
