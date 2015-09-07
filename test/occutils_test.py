#!/usr/bin/env python

##Copyright 2009-2015 Thomas Paviot (tpaviot@gmail.com)
##
##This file is part of pythonOCC.
##
##pythonOCC is free software: you can redistribute it and/or modify
##it under the terms of the GNU Lesser General Public License as published by
##the Free Software Foundation, either version 3 of the License, or
##(at your option) any later version.
##
##pythonOCC is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU Lesser General Public License for more details.
##
##You should have received a copy of the GNU Lesser General Public License
##along with pythonOCC.  If not, see <http://www.gnu.org/licenses/>.

import unittest

from OCC.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.TopoDS import TopoDS_Face, TopoDS_Shape, TopoDS_Solid

from OCCUtils.Topology import Topo
from OCCUtils.edge import Edge
from OCCUtils.wire import Wire
from OCCUtils.face import Face
from OCCUtils.shell import Shell



def get_test_box_shape():
    return BRepPrimAPI_MakeBox(10, 20, 30).Shape()


class TestTopo(unittest.TestCase):

    def setUp(self):
        self.box = get_test_box_shape()

    def test_init(self):
        t = Topo(self.box)
        assert(t)

    def test_loop_faces(self):
        t = Topo(self.box)
        i = 0
        for face in t.faces():
            i += 1
            assert(isinstance(face, TopoDS_Face))
        assert(i == 6)

    def test_get_numbers_of_members(self):
        t = Topo(self.box)
        assert(t.number_of_faces() == 6)
        assert(t.number_of_edges() == 12)
        assert(t.number_of_vertices() == 8)
        assert(t.number_of_wires() == 6)
        assert(t.number_of_solids() == 1)
        assert(t.number_of_shells() == 1)
        assert(t.number_of_compounds() == 0)
        assert(t.number_of_comp_solids() == 0)

    def test_ignore_orientation(self):
        t = Topo(self.box, ignore_orientation=False)
        t_ignore = Topo(self.box, ignore_orientation=True)

        print "no ignore", len([e for e in t.edges()]) # expect 24
        print "ignore", len([e for e in t_ignore.edges()]) # expect 12
        print "OMG"

    # def test_kbe_wires(self):
    #     t = Topo(self.box, kbe_types=True)
    #     edges = [e for e in t.edges()]
    #     print "mmm"




# TODO: port the huge list of tests from the ancient pythonocc repo...


class Test_TypesLut(unittest.TestCase):
    def test_shape_to_topology(self):
        """

        ShapeToTopology returns a specific topological type from a generic TopoDS_Shape

        Many functions return a generic TopoDS_Shape, rather than a specific topological entity

        `get_test_box_shape` is a good example, it returns a `TopoDS_Shape` rather than a TopoDS_Solid


        Example
        -------

        # assume edg -> TopoDS_Edge

        # >>> print shape
        #  < OCC.TopoDS.TopoDS_Shape; proxy of <Swig... >
        #
        # >>> stt = types_lut.ShapeToTopology()
        # >>> edge = stt(shape)
        #  <OCC.TopoDS.TopoDS_Edge; proxy of <Swig... >

        """

        from OCCUtils import types_lut
        box = get_test_box_shape()
        tp = Topo(box)

        stt = types_lut.ShapeToTopology()
        assert isinstance(stt(TopoDS_Shape(box)), TopoDS_Solid)

        for i in tp.vertices():
            assert stt(TopoDS_Shape(i)) == i

        for i in tp.edges():
            assert stt(TopoDS_Shape(i)) == i

        for i in tp.faces():
            assert stt(TopoDS_Shape(i)) == i

        for i in tp.wires():
            assert stt(TopoDS_Shape(i)) == i

        for i in tp.shells():
            assert stt(TopoDS_Shape(i)) == i


class Test_KBE_types(unittest.TestCase):

    """

    inheriting from TopoDS_* classes is pretty complex
    this test just creates instances, merely creating the instances validates whether the
    constructors of the KBE types are alright

    """

    def setUp(self):
        self.box = get_test_box_shape()
        self.tp = Topo(self.box)

    def test_instantiate_edge(self):
        for i in self.tp.edges():
            assert Edge(i)

    def test_instantiate_face(self):
        for i in self.tp.faces():
            assert Face(i)

    def test_instantiate_wire(self):
        for i in self.tp.wires():
            assert Wire(i)

    def test_instantiate_shell(self):
        for i in self.tp.shells():
            assert Shell(i)



def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestTopo))
    test_suite.addTest(unittest.makeSuite(Test_TypesLut))
    return test_suite

if __name__ == "__main__":
    unittest.main()
