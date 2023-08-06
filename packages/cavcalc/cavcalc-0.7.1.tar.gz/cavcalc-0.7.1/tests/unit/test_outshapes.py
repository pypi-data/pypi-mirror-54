import numbers
from unittest import TestCase

import cavcalc as cc
import numpy as np

class OutputShapesTestCase(TestCase):
    def test_scalar_single_target(self):
        out = cc.calculate('w', L=1, g=0.7)
        w = out.get()

        self.assertTrue(isinstance(w.v, numbers.Number))

    def test_scalar_all_target(self):
        out = cc.calculate(L=4000, Rc1=1934, Rc2=2245)
        all_ = out.get()

        for t in all_.values():
            self.assertTrue(isinstance(t.v, numbers.Number))

    def test_scalar_single_target_quadrants(self):
        out = cc.calculate('gs', gouy=0.7)
        gsingle = out.get()

        self.assertTrue(isinstance(gsingle.v, np.ndarray))
        self.assertTrue(gsingle.v.shape == (2, ))

    def test_1D_single_target_onearg(self):
        out = cc.calculate("gouy", gs=np.linspace(-0.9, -0.5, 100))
        gouy = out.get()

        self.assertTrue(isinstance(gouy.v, np.ndarray))
        self.assertTrue(gouy.v.shape == (100, ))

    def test_1D_single_target_multiarg(self):
        out = cc.calculate("w0", L=20, gouy=(np.linspace(10, 40, 345), "deg"))
        w0 = out.get()

        self.assertTrue(cc.Parameter.GOUY in out.arraylike_dependents(just_param=True))
        self.assertTrue(cc.Parameter.CAV_LENGTH in out.constant_dependents(just_param=True))

        self.assertTrue(isinstance(w0.v, np.ndarray))
        self.assertTrue(w0.v.shape == (345, ))

    def test_1D_all_target(self):
        out = cc.calculate(L=np.linspace(1, 10, 200),
                           g1=-0.7, g2=-0.4)
        all_ = out.get()

        for p, t in all_.items():
            if p == cc.Parameter.GOUY:
                self.assertTrue(isinstance(t.v, numbers.Number))
            else:
                self.assertTrue(isinstance(t.v, np.ndarray))
                if p == cc.Parameter.CAV_GFACTOR:
                    self.assertTrue(t.v.shape == (200, 200))
                else:
                    self.assertTrue(t.v.shape == (200, ))

    def test_grid_single_target(self):
        out = cc.calculate("z0", g1=np.linspace(-0.9, -0.5, 100),
                           g2=np.linspace(-0.8, -0.4, 100), L=10)
        gouy = out.get()

        self.assertTrue(isinstance(gouy.v, np.ndarray))
        self.assertTrue(gouy.v.shape == (100, 100))
