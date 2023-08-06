import pytest
import unittest

from PyFoam.RunDictionary.SolutionFile import SolutionFile

from os import path,environ,remove,system
from tempfile import mktemp
from shutil import copyfile

from .test_TimeDirectory import damBreakTutorial,gammaName
from PyFoam.FoamInformation import foamVersionNumber,foamFork,foamTutorials


class SolutionFileTest(unittest.TestCase):
    def setUp(self):
        self.theFile=mktemp()
        if foamVersionNumber()<(2,0):
            extension=""
        elif foamFork() in ["openfoam","openfoamplus"] and foamVersionNumber()>=(4,):
            extension=".orig"
        else:
            extension=".org"
        copyfile(path.join(damBreakTutorial(),"0",gammaName()+extension),self.theFile)

    def tearDown(self):
        remove(self.theFile)

    @pytest.mark.skipif(foamTutorials()=='',reason="$FOAM_TUTORIALS is not defined")
    def testSolutionFileReadWrite(self):
        test=SolutionFile(path.dirname(self.theFile),path.basename(self.theFile))
        self.assertEqual(test.readInternalUniform(),"0")
        self.assertEqual(test.readBoundary("atmosphere"),"0")
        self.assertEqual(test.readDimension(),"0 0 0 0 0 0 0")
        test.replaceBoundary("atmosphere",2.3)
        self.assertEqual(test.readBoundary("atmosphere"),"2.3")
        test.replaceInternal(3.14)
        self.assertEqual(test.readInternalUniform(),"3.14")


class SolutionFileTestZipped(unittest.TestCase):
    def setUp(self):
        self.theFile=mktemp()
        if foamVersionNumber()<(2,0):
            extension=""
        elif foamFork() in ["openfoam","openfoamplus"] and foamVersionNumber()>=(4,):
            extension=".orig"
        else:
            extension=".org"
        copyfile(path.join(damBreakTutorial(),"0",gammaName()+extension),self.theFile)
        system("gzip -f "+self.theFile)

    def tearDown(self):
        remove(self.theFile+".gz")

    @pytest.mark.skipif(foamTutorials()=='',reason="$FOAM_TUTORIALS is not defined")
    def testSolutionFileZippedReadWrite(self):
        test=SolutionFile(path.dirname(self.theFile),path.basename(self.theFile))
        self.assertEqual(test.readInternalUniform(),"0")
        self.assertEqual(test.readBoundary("atmosphere"),"0")
        self.assertEqual(test.readDimension(),"0 0 0 0 0 0 0")
        test.replaceBoundary("atmosphere",2.3)
        self.assertEqual(test.readBoundary("atmosphere"),"2.3")
        test.replaceInternal(3.14)
        self.assertEqual(test.readInternalUniform(),"3.14")


# Should work with Python3 and Python2
