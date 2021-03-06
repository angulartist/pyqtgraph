# -*- coding: utf-8 -*-
"""
Vector.py -  Extension of QVector3D which adds a few missing methods.
Copyright 2010  Luke Campagnola
Distributed under MIT/X11 license. See license.txt for more information.
"""

from .Qt import QtGui, QtCore, QT_LIB
import numpy as np

class Vector(QtGui.QVector3D):
    """Extension of QVector3D which adds a few helpful methods."""
    
    def __init__(self, *args):
        if len(args) == 1:
            if isinstance(args[0], QtCore.QSizeF):
                x = float(args[0].width())
                y = float(args[0].height())
                z = 0
            elif isinstance(args[0], QtCore.QPoint) or isinstance(args[0], QtCore.QPointF):
                x = float(args[0].x())
                y = float(args[0].y())
                z = 0
            elif isinstance(args[0], QtGui.QVector3D):
                x = args[0].x()
                y = args[0].y()
                z = args[0].z()
            elif hasattr(args[0], '__getitem__'):
                vals = list(args[0])
                if len(vals) == 2:
                    x, y = vals
                    z = 0
                elif len(vals) == 3:
                    x, y, z = vals
                else:
                    raise ValueError('Cannot init Vector with sequence of length %d' % len(args[0]))
        elif len(args) == 2:
            x, y = args
            z = 0
        else:
            x, y, z = args  # Could raise ValueError

        QtGui.QVector3D.__init__(self, x, y, z)

    def __len__(self):
        return 3

    def __add__(self, b):
        # workaround for pyside bug. see https://bugs.launchpad.net/pyqtgraph/+bug/1223173
        if QT_LIB == 'PySide' and isinstance(b, QtGui.QVector3D):
            b = Vector(b)
        return QtGui.QVector3D.__add__(self, b)
    
    #def __reduce__(self):
        #return (Point, (self.x(), self.y()))
        
    def __getitem__(self, i):
        if i == 0:
            return self.x()
        elif i == 1:
            return self.y()
        elif i == 2:
            return self.z()
        else:
            raise IndexError("Point has no index %s" % str(i))
        
    def __setitem__(self, i, x):
        if i == 0:
            return self.setX(x)
        elif i == 1:
            return self.setY(x)
        elif i == 2:
            return self.setZ(x)
        else:
            raise IndexError("Point has no index %s" % str(i))
        
    def __iter__(self):
        yield(self.x())
        yield(self.y())
        yield(self.z())

    def angle(self, a):
        """Returns the angle in degrees between this vector and the vector a."""
        n1 = self.length()
        n2 = a.length()
        if n1 == 0. or n2 == 0.:
            return None
        ## Probably this should be done with arctan2 instead..
        ang = np.arccos(np.clip(QtGui.QVector3D.dotProduct(self, a) / (n1 * n2), -1.0, 1.0)) ### in radians
#        c = self.crossProduct(a)
#        if c > 0:
#            ang *= -1.
        return ang * 180. / np.pi

    def __abs__(self):
        return Vector(abs(self.x()), abs(self.y()), abs(self.z()))
        
        