import unittest
import pygsti
import numpy as np
import pickle

import pygsti.construction as pc
from pygsti.construction import std1Q_XYI as std

from ..testutils import BaseTestCase, compare_files, temp_files

class CircuitTestCase(BaseTestCase):

    def setUp(self):
        super(CircuitTestCase, self).setUp()

    def test_structure(self):
        raw_gss = pygsti.objects.CircuitStructure() #base class that doens't implmenet much

        with self.assertRaises(NotImplementedError):
            raw_gss.xvals()
        with self.assertRaises(NotImplementedError):
            raw_gss.yvals()
        with self.assertRaises(NotImplementedError):
            raw_gss.minor_xvals()
        with self.assertRaises(NotImplementedError):
            raw_gss.minor_yvals()
        with self.assertRaises(NotImplementedError):
            raw_gss.create_plaquette(baseStr="")
        with self.assertRaises(NotImplementedError):
            raw_gss.get_plaquette(x=0,y=0)
        with self.assertRaises(NotImplementedError):
            raw_gss.plaquette_rows_cols()


        gss = pygsti.objects.LsGermsStructure([1,2,4], std.germs, std.prepStrs, std.effectStrs)
        gss.truncate([1,2])


if __name__ == '__main__':
    unittest.main(verbosity=2)
