from .utils import *
from ..hdl import *
from ..hdl.rec import *
from ..back.pysim import *
from ..lib.io import *


class PinLayoutCombTestCase(FHDLTestCase):
    def test_pin_layout_i(self):
        layout_1 = pin_layout(1, dir="i")
        self.assertEqual(layout_1.fields, {
            "i": ((1, False), DIR_NONE),
        })

        layout_2 = pin_layout(2, dir="i")
        self.assertEqual(layout_2.fields, {
            "i": ((2, False), DIR_NONE),
        })

    def test_pin_layout_o(self):
        layout_1 = pin_layout(1, dir="o")
        self.assertEqual(layout_1.fields, {
            "o": ((1, False), DIR_NONE),
        })

        layout_2 = pin_layout(2, dir="o")
        self.assertEqual(layout_2.fields, {
            "o": ((2, False), DIR_NONE),
        })

    def test_pin_layout_oe(self):
        layout_1 = pin_layout(1, dir="oe")
        self.assertEqual(layout_1.fields, {
            "o":  ((1, False), DIR_NONE),
            "oe": ((1, False), DIR_NONE),
        })

        layout_2 = pin_layout(2, dir="oe")
        self.assertEqual(layout_2.fields, {
            "o":  ((2, False), DIR_NONE),
            "oe": ((1, False), DIR_NONE),
        })

    def test_pin_layout_io(self):
        layout_1 = pin_layout(1, dir="io")
        self.assertEqual(layout_1.fields, {
            "i":  ((1, False), DIR_NONE),
            "o":  ((1, False), DIR_NONE),
            "oe": ((1, False), DIR_NONE),
        })

        layout_2 = pin_layout(2, dir="io")
        self.assertEqual(layout_2.fields, {
            "i":  ((2, False), DIR_NONE),
            "o":  ((2, False), DIR_NONE),
            "oe": ((1, False), DIR_NONE),
        })


class PinLayoutSDRTestCase(FHDLTestCase):
    def test_pin_layout_i(self):
        layout_1 = pin_layout(1, dir="i", xdr=1)
        self.assertEqual(layout_1.fields, {
            "i_clk": ((1, False), DIR_NONE),
            "i": ((1, False), DIR_NONE),
        })

        layout_2 = pin_layout(2, dir="i", xdr=1)
        self.assertEqual(layout_2.fields, {
            "i_clk": ((1, False), DIR_NONE),
            "i": ((2, False), DIR_NONE),
        })

    def test_pin_layout_o(self):
        layout_1 = pin_layout(1, dir="o", xdr=1)
        self.assertEqual(layout_1.fields, {
            "o_clk": ((1, False), DIR_NONE),
            "o": ((1, False), DIR_NONE),
        })

        layout_2 = pin_layout(2, dir="o", xdr=1)
        self.assertEqual(layout_2.fields, {
            "o_clk": ((1, False), DIR_NONE),
            "o": ((2, False), DIR_NONE),
        })

    def test_pin_layout_oe(self):
        layout_1 = pin_layout(1, dir="oe", xdr=1)
        self.assertEqual(layout_1.fields, {
            "o_clk": ((1, False), DIR_NONE),
            "o":  ((1, False), DIR_NONE),
            "oe": ((1, False), DIR_NONE),
        })

        layout_2 = pin_layout(2, dir="oe", xdr=1)
        self.assertEqual(layout_2.fields, {
            "o_clk": ((1, False), DIR_NONE),
            "o":  ((2, False), DIR_NONE),
            "oe": ((1, False), DIR_NONE),
        })

    def test_pin_layout_io(self):
        layout_1 = pin_layout(1, dir="io", xdr=1)
        self.assertEqual(layout_1.fields, {
            "i_clk": ((1, False), DIR_NONE),
            "i":  ((1, False), DIR_NONE),
            "o_clk": ((1, False), DIR_NONE),
            "o":  ((1, False), DIR_NONE),
            "oe": ((1, False), DIR_NONE),
        })

        layout_2 = pin_layout(2, dir="io", xdr=1)
        self.assertEqual(layout_2.fields, {
            "i_clk": ((1, False), DIR_NONE),
            "i":  ((2, False), DIR_NONE),
            "o_clk": ((1, False), DIR_NONE),
            "o":  ((2, False), DIR_NONE),
            "oe": ((1, False), DIR_NONE),
        })


class PinLayoutDDRTestCase(FHDLTestCase):
    def test_pin_layout_i(self):
        layout_1 = pin_layout(1, dir="i", xdr=2)
        self.assertEqual(layout_1.fields, {
            "i_clk": ((1, False), DIR_NONE),
            "i0": ((1, False), DIR_NONE),
            "i1": ((1, False), DIR_NONE),
        })

        layout_2 = pin_layout(2, dir="i", xdr=2)
        self.assertEqual(layout_2.fields, {
            "i_clk": ((1, False), DIR_NONE),
            "i0": ((2, False), DIR_NONE),
            "i1": ((2, False), DIR_NONE),
        })

    def test_pin_layout_o(self):
        layout_1 = pin_layout(1, dir="o", xdr=2)
        self.assertEqual(layout_1.fields, {
            "o_clk": ((1, False), DIR_NONE),
            "o0": ((1, False), DIR_NONE),
            "o1": ((1, False), DIR_NONE),
        })

        layout_2 = pin_layout(2, dir="o", xdr=2)
        self.assertEqual(layout_2.fields, {
            "o_clk": ((1, False), DIR_NONE),
            "o0": ((2, False), DIR_NONE),
            "o1": ((2, False), DIR_NONE),
        })

    def test_pin_layout_oe(self):
        layout_1 = pin_layout(1, dir="oe", xdr=2)
        self.assertEqual(layout_1.fields, {
            "o_clk": ((1, False), DIR_NONE),
            "o0": ((1, False), DIR_NONE),
            "o1": ((1, False), DIR_NONE),
            "oe": ((1, False), DIR_NONE),
        })

        layout_2 = pin_layout(2, dir="oe", xdr=2)
        self.assertEqual(layout_2.fields, {
            "o_clk": ((1, False), DIR_NONE),
            "o0": ((2, False), DIR_NONE),
            "o1": ((2, False), DIR_NONE),
            "oe": ((1, False), DIR_NONE),
        })

    def test_pin_layout_io(self):
        layout_1 = pin_layout(1, dir="io", xdr=2)
        self.assertEqual(layout_1.fields, {
            "i_clk": ((1, False), DIR_NONE),
            "i0": ((1, False), DIR_NONE),
            "i1": ((1, False), DIR_NONE),
            "o_clk": ((1, False), DIR_NONE),
            "o0": ((1, False), DIR_NONE),
            "o1": ((1, False), DIR_NONE),
            "oe": ((1, False), DIR_NONE),
        })

        layout_2 = pin_layout(2, dir="io", xdr=2)
        self.assertEqual(layout_2.fields, {
            "i_clk": ((1, False), DIR_NONE),
            "i0": ((2, False), DIR_NONE),
            "i1": ((2, False), DIR_NONE),
            "o_clk": ((1, False), DIR_NONE),
            "o0": ((2, False), DIR_NONE),
            "o1": ((2, False), DIR_NONE),
            "oe": ((1, False), DIR_NONE),
        })


class PinTestCase(FHDLTestCase):
    def test_attributes(self):
        pin = Pin(2, dir="io", xdr=2)
        self.assertEqual(pin.width, 2)
        self.assertEqual(pin.dir,   "io")
        self.assertEqual(pin.xdr,   2)
