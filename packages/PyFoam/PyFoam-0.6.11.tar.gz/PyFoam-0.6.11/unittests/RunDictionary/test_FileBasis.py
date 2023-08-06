import unittest

from PyFoam.RunDictionary.FileBasis import FileBasis

from tempfile import mktemp
from os import unlink,path
import gzip

class ReadFromFileTest(unittest.TestCase):
    txt="""Fo
Bar
One more"""
    def setUp(self):
        self.dest=mktemp()
        self.dest2=mktemp()

    def tearDown(self):
        for d in [self.dest,self.dest2]:
            if path.exists(d):
                unlink(d)
            if path.exists(d+".gz"):
                unlink(d+".gz")

    def testReadFileUnzippedAscii(self):
        open(self.dest,"w").write(self.txt)
        f=FileBasis(self.dest,createZipped=False,useBinary=False)
        assert f.exists
        assert f.realName()==self.dest
        f.openFile(mode="r")
        assert f.useBinary==False
        f.readFile()
        assert self.txt==f.content

    def testReadFileUnzippedAsciiWriteAs(self):
        open(self.dest,"w").write(self.txt)
        f=FileBasis(self.dest,createZipped=False,useBinary=False)
        assert f.realName()==self.dest
        f.openFile(mode="r")
        assert f.useBinary==False
        f.writeFileAs(self.dest2)
        assert self.txt==open(self.dest2).read()

    def testReadFileUnzippedAsciiHandle(self):
        open(self.dest,"w").write(self.txt)
        f=FileBasis(open(self.dest),createZipped=False,useBinary=False)
        f.openFile(mode="r")
        assert f.useBinary==False
        f.readFile()
        assert self.txt==f.content

    def testReadFileZippedAscii(self):
        gzip.open(self.dest+".gz","w").write(self.txt.encode())
        f=FileBasis(self.dest,createZipped=False,useBinary=False)
        assert f.exists
        assert f.realName()==self.dest+".gz"
        f.openFile(mode="r")
        assert f.useBinary==False
        f.readFile()
        assert self.txt==f.content

    def testReadFileZippedAsciiWriteAs(self):
        gzip.open(self.dest+".gz","w").write(self.txt.encode())
        f=FileBasis(self.dest,createZipped=True,useBinary=False)
        assert f.realName()==self.dest+".gz"
        f.openFile(mode="r")
        assert f.useBinary==False
        f.writeFileAs(self.dest2)
        assert self.txt==gzip.open(self.dest2+".gz").read().decode()

    def testReadFileUnzippedBinary(self):
        open(self.dest,"w").write(self.txt)
        f=FileBasis(self.dest,createZipped=False,useBinary=True)
        assert f.realName()==self.dest
        f.openFile(mode="r")
        assert f.useBinary==True
        f.readFile()
        assert self.txt==f.content

    def testReadFileUnzippedBinaryHandle(self):
        open(self.dest,"w").write(self.txt)
        f=FileBasis(open(self.dest,"rb"),createZipped=False,useBinary=False)
        f.openFile(mode="r")
        assert f.useBinary==False
        f.readFile()
        assert self.txt==f.content.decode()

    def testReadFileZippedBinary(self):
        gzip.open(self.dest+".gz","w").write(self.txt.encode())
        f=FileBasis(self.dest,createZipped=False,useBinary=True)
        assert f.realName()==self.dest+".gz"
        f.openFile(mode="r")
        assert f.useBinary==True
        f.readFile()
        assert self.txt==f.content

class WriteToFileTest(unittest.TestCase):
    txt="""Fo
Bar
One more"""
    def setUp(self):
        self.dest=mktemp()

    def tearDown(self):
        if path.exists(self.dest):
            unlink(self.dest)
        if path.exists(self.dest+".gz"):
            unlink(self.dest+".gz")

    def testWriteFileUnzippedAscii(self):
        assert not path.exists(self.dest)
        f=FileBasis(self.dest,createZipped=False,useBinary=False)
        assert f.realName()==self.dest
        assert not f.exists
        f.openFile(mode="w")
        assert path.exists(self.dest)
        assert f.useBinary==False
        f.writeFile(self.txt)
        assert self.txt==open(self.dest).read()

    def testWriteFileUnzippedAsciiWith(self):
        assert not path.exists(self.dest)
        with FileBasis(self.dest,createZipped=False,useBinary=False) as f:
            assert f.realName()==self.dest
            f.openFile(mode="w")
            assert path.exists(self.dest)
            assert f.useBinary==False
            f.writeFile(self.txt)
        assert self.txt==open(self.dest).read()

    def testWriteFileUnzippedBinary(self):
        assert not path.exists(self.dest)
        f=FileBasis(self.dest,createZipped=False,useBinary=True)
        assert f.realName()==self.dest
        f.openFile(mode="w")
        assert f.useBinary==True
        assert path.exists(self.dest)
        f.writeFile(self.txt)
        assert self.txt==open(self.dest).read()

    def testWriteFileUnzippedBinary2(self):
        assert not path.exists(self.dest)
        f=FileBasis(self.dest,createZipped=False,useBinary=False)
        assert f.realName()==self.dest
        f.openFile(mode="wb")
        assert f.useBinary==True
        assert path.exists(self.dest)
        f.writeFile(self.txt)
        assert self.txt==open(self.dest).read()

    def testWriteFileZippedAscii(self):
        assert not path.exists(self.dest)
        f=FileBasis(self.dest,createZipped=True,useBinary=False)
        assert f.realName()==self.dest+".gz"
        f.openFile(mode="w")
        assert path.exists(self.dest+".gz")
        assert f.useBinary==False
        f.writeFile(self.txt)
        assert self.txt==gzip.open(self.dest+".gz").read().decode()

    def testWriteFileZippedBinary(self):
        assert not path.exists(self.dest)
        f=FileBasis(self.dest,createZipped=True,useBinary=True)
        assert f.realName()==self.dest+".gz"
        f.openFile(mode="w")
        assert path.exists(self.dest+".gz")
        assert f.useBinary==True
        f.writeFile(self.txt)
        assert self.txt==gzip.open(self.dest+".gz").read().decode()

    def testWriteFileMakeTemp(self):
        assert not path.exists(self.dest)
        f=FileBasis(self.dest,createZipped=False,useBinary=False)
        fh,fn=f.makeTemp()
        assert path.exists(fn)
        fh.write(self.txt)
        fh.close()
        assert self.txt==open(fn).read()
        unlink(fn)
