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

from .style import Style


class DOM(object):
    image_fn = ""
    image = None
    data = None
    flat_data = None
    info = None

    def __init__(self, wh, bound=None):
        """
        :param wh: list [width, height] specifying the size of the image in pixels SVG
        :param bound: list [x1, y1, x2, y2] border coordinate plane
        """
        self.wh = wh  # [1000, 1000]
        self.w, self.h = float(wh[0]), float(wh[1])

        if bound is None:
            img_d0, img_d1 = (self.h / self.w, 1) if self.w > self.h else (1, self.w / self.h)
            bound = [-1 * img_d1, -1 * img_d0, img_d1, img_d0]

        self.bound = bound  # [-1, -1, 0, 0]
        self.x1, self.y1 = float(self.bound[0]), float(self.bound[1])
        self.x2, self.y2 = float(self.bound[2]), float(self.bound[3])

        self.dx = float(self.x2 - self.x1)
        self.dy = float(self.y2 - self.y1)

        self.scale = self.dx / self.w  # Resolution field in units per pixel SVG
        self.style = Style()

        self.clean()

    def clean(self):
        self.data = []
        self.flat_data = []
        self.info = {}

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return "[{}]".format(self.data)

    def __repr__(self):
        return "DOM({})".format(self.data)

    def __iter__(self):
        return iter(self.data)
