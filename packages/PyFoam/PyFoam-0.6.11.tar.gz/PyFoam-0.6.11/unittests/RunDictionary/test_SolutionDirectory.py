import pytest
import unittest

from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.RunDictionary.TimeDirectory import TimeDirectory

from PyFoam.FoamInformation import foamTutorials

from os import path,environ,system
from tempfile import mkdtemp
from shutil import rmtree,copytree

from .test_TimeDirectory import damBreakTutorial

def chtMultiRegionTutorial():
    prefix=foamTutorials()
    return path.join(prefix,"heatTransfer","chtMultiRegionFoam","multiRegionHeater")

class SolutionDirectoryTest(unittest.TestCase):
    def setUp(self):
        self.theDir=mkdtemp()
        self.theFile=path.join(self.theDir,"damBreak")
        copytree(damBreakTutorial(),self.theFile)

    def tearDown(self):
        rmtree(self.theDir)

    @pytest.mark.skipif(foamTutorials()=='',reason="$FOAM_TUTORIALS is not defined")
    def testSolutionDirectoryBasicContainerStuff(self):
        test=SolutionDirectory(self.theFile)
        self.assertEqual(len(test),1)
        self.assertTrue("0" in test)
        self.assertTrue("1e-7" in test)
        self.assertTrue("1e-4" not in test)
        self.assertTrue(0. in test)
        td=test["0"]
        self.assertEqual(type(td),TimeDirectory)
        self.assertRaises(KeyError,test.__getitem__,"42")
        td=test[-1]
        self.assertEqual(type(td),TimeDirectory)
        lst=[]
        for t in test:
            lst.append(t.baseName())
        self.assertEqual(len(test),len(lst))
        self.assertEqual(lst,test.getTimes())

    @pytest.mark.skipif(foamTutorials()=='',reason="$FOAM_TUTORIALS is not defined")
    def testTimeCopy(self):
        test=SolutionDirectory(self.theFile)
        self.assertEqual(len(test),1)
        test["42"]=test[0]
        self.assertEqual(len(test),2)
        self.assertEqual(len(test["42"]),len(test[0]))
        del test["42"]
        self.assertEqual(len(test),1)
        del test[-1]
        self.assertEqual(len(test),0)

@pytest.fixture
def setupHeater(tmpdir,monkeypatch):
    theDir=path.join(str(tmpdir),"heater")
    copytree(chtMultiRegionTutorial(),theDir)
    monkeypatch.chdir(theDir)
    from subprocess import call
    call("./Allrun.pre")

@pytest.mark.skipif(foamTutorials()=='',reason="$FOAM_TUTORIALS is not defined")
def test_SolutionDirectoryMultiRegionTest(setupHeater):
    sol=SolutionDirectory(".")
    assert sol.isValid()
    assert len(sol.regions())==5
    assert len(sol.getRegions())==5
    assert "0" in sol
    td=sol["0"]
    assert type(td)==TimeDirectory
    assert len(td)==7
    assert sol.missingFiles()==[]
    assert sol.nrProcs()==0
    assert sol.getParallelTimes()==[]

    assert path.basename(sol.latestDir())=="0"
    assert path.basename(sol.initialDir())=="0"

    assert sol.first=="0"

    solTop=SolutionDirectory(".",region="topHeater")
    assert not solTop.isValid()
    solTop=SolutionDirectory(".",region="topAir")
    assert solTop.isValid()
    assert solTop.missingFiles()==[]
    assert solTop.nrProcs()==0

    assert sol.controlDict()==solTop.controlDict()
    assert sol.systemDir()!=solTop.systemDir()

    assert "0" in solTop
    tdTop=solTop["0"]
    assert type(tdTop)==TimeDirectory
    assert len(tdTop)==7

@pytest.fixture
def setupHeaterParallel(setupHeater):
    from subprocess import call
    call(["decomposePar","-allRegions"])

@pytest.mark.skipif(foamTutorials()=='',reason="$FOAM_TUTORIALS is not defined")
def test_SolutionDirectoryMultiRegionParallelTest(setupHeaterParallel):
    sol=SolutionDirectory(".",parallel=True)

    assert sol.isValid()
    assert sol.nrProcs()==4
    assert sol.getParallelTimes()==["0"]

    solTop=SolutionDirectory(".",region="topHeater")
    assert solTop.nrProcs()==4
    assert solTop.getParallelTimes()==["0"]

# Should work with Python3 and Python2
