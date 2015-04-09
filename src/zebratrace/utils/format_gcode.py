#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Copyright 2012 Maxim.S.Barabash <maxim.s.barabash@gmail.com>
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
from .. import __version__


class GCode():

    def __init__(self, dom, filename='plot.ngc', feedback=None):
        self.dom = dom
        self.filename = filename
        self.feedback = feedback

    def save(self, filename=None, dpi=90.0):
        from . import tr
        if filename is None:
            filename = self.filename
        dom = self.dom

        feedback = self.feedback
        if feedback:
            feed = feedback(text=tr('Save NGC file.'))

        header = '%\r\n'
        header += '(Generated by ZebraTRACE v%s)\r\n' % __version__
        header += 'G96 S90 (SET SPINDLE SPEED, SO M3/M5 WILL WORK)\r\n'
        header += 'G21 (All units in mm)\r\n'
        header += '\r\n'
        header += '#1  = %f (Scale X - relative to the dimensions shown in svg)\r\n' % (dom.scale)
        header += '#2  = 1.000000 (Scale Y - relative to the dimensions shown in svg)\r\n'
        header += '#3  = 0.282222 (convert pixels to inches or mm)\r\n'
        header += '#4  = 300.000000 (Feed)\r\n'
        header += '#5  = [#1*#3] (Total X scale - includes conversion to inches / mm)\r\n'
        header += '#6  = [#2*#3] (Total Y scale - inc conversions to inches / mm)\r\n'
        header += '#7  = 1.000000 (Scale z)\r\n'
        header += '#8  = 0.000000 (Offset x)\r\n'
        header += '#9  = 0.000000 (Offset y)\r\n'
        header += '#10 = 0.000000 (Offset z)\r\n'
        header += '#11 = 5.000000 (Safe distance)\r\n'
        header += '\r\n'
        header += 'F#4\r\n\r\n'

        footer = "M02\r\n%\r\n"

        body = ''.join(reversed([self.pathAsGCODE(s) for s in dom.data]))

        f = open(filename, 'wb')                # write to file
        f.write(header.encode('utf-8'))
        f.write(body.encode('utf-8'))
        f.write(footer.encode('utf-8'))
        f.close()
        if feedback:
            feedback()

    def pathAsGCODE(self, s):
        path = ''
        for p in s:
            path += 'G00 X[%f] Y[%f] Z#11\r\n' % (p.node[0].x, p.node[0].y)
            path += ''.join(['G01 X[%f*#5+#8] Y[%f*#6+#9] Z[%f*#7+#10]\r\n' % (n.x, n.y, -1.0 * n.d) for n in p.node[:]])

        path += 'Z#11\r\n'
        return path
