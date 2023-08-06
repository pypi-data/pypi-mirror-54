import pytest
import unittest

from PyFoam.RunDictionary.MeshInformation import MeshInformation
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.Execution.UtilityRunner import UtilityRunner

from PyFoam.Error import PyFoamException

from PyFoam.FoamInformation import oldAppConvention as oldApp
from PyFoam.FoamInformation import foamTutorials

from os import path,environ
from shutil import rmtree
from tempfile import mktemp

from .test_TimeDirectory import damBreakTutorial

class MeshInformationTest(unittest.TestCase):
    def setUp(self):
        self.dest=mktemp()
        SolutionDirectory(damBreakTutorial(),archive=None,paraviewLink=False).cloneCase(self.dest)

        if oldApp():
            pathSpec=[path.dirname(self.dest),path.basename(self.dest)]
        else:
            pathSpec=["-case",self.dest]

        run=UtilityRunner(argv=["blockMesh"]+pathSpec,silent=False,server=False)
        run.start()

    def tearDown(self):
        rmtree(self.dest)

    @pytest.mark.skipif(foamTutorials()=='',reason="$FOAM_TUTORIALS is not defined")
    def testBoundaryRead(self):
        mesh=MeshInformation(self.dest)
        self.assertEqual(mesh.nrOfFaces(),9176)
        self.assertEqual(mesh.nrOfPoints(),4746)
        self.assertEqual(mesh.nrOfCells(),2268)
        try:
            self.assertEqual(mesh.nrOfCells(),2268)
        except:
            if not oldApp():
                self.fail()

# Should work with Python3 and Python2
