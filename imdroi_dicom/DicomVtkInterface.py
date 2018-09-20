import numpy as np
import vtk

from vtk import vtkImageImport
from vtk import VTK_SIGNED_CHAR
from vtk import VTK_UNSIGNED_CHAR
from vtk import VTK_SHORT
from vtk import VTK_UNSIGNED_SHORT
from vtk import VTK_INT
from vtk import VTK_UNSIGNED_INT
from vtk import VTK_LONG
from vtk import VTK_UNSIGNED_LONG
from vtk import VTK_FLOAT
from vtk import VTK_DOUBLE

class vtkImageImportFromArray:
    def __init__(self):
        self.__import = vtkImageImport()
        self.__ConvertIntToUnsignedShort = False
        self.__Array = None

    # type dictionary: note that python doesn't support
    # unsigned integers properly!
    __typeDict = {'b':VTK_SIGNED_CHAR,     # int8
                  'B':VTK_UNSIGNED_CHAR,   # uint8
                  'h':VTK_SHORT,           # int16
                  'H':VTK_UNSIGNED_SHORT,  # uint16
                  'i':VTK_INT,             # int32
                  'I':VTK_UNSIGNED_INT,    # uint32
                  'f':VTK_FLOAT,           # float32
                  'd':VTK_DOUBLE,          # float64
                  'F':VTK_FLOAT,           # float32
                  'D':VTK_DOUBLE,          # float64
                  }

    __sizeDict = { VTK_SIGNED_CHAR:1,
                   VTK_UNSIGNED_CHAR:1,
                   VTK_SHORT:2,
                   VTK_UNSIGNED_SHORT:2,
                   VTK_INT:4,
                   VTK_UNSIGNED_INT:4,
                   VTK_FLOAT:4,
                   VTK_DOUBLE:8 }

    # convert 'Int32' to 'unsigned short'
    def SetConvertIntToUnsignedShort(self,yesno):
        self.__ConvertIntToUnsignedShort = yesno

    def GetConvertIntToUnsignedShort(self):
        return self.__ConvertIntToUnsignedShort

    def ConvertIntToUnsignedShortOn(self):
        self.__ConvertIntToUnsignedShort = True

    def ConvertIntToUnsignedShortOff(self):
        self.__ConvertIntToUnsignedShort = False

    def Update(self):
        self.__import.Update()

    # get the output
    def GetOutputPort(self):
        return self.__import.GetOutputPort()

    # get the output
    def GetOutput(self):
        return self.__import.GetOutput()

    # import an array
    def SetArray(self,imArray):
        self.__Array = imArray
        numComponents = 1
        dim = imArray.shape
        if len(dim) == 0:
            dim = (1,1,1)
        elif len(dim) == 1:
            dim = (1, 1, dim[0])
        elif len(dim) == 2:
            dim = (1, dim[0], dim[1])
        elif len(dim) == 4:
            numComponents = dim[3]
            dim = (dim[0],dim[1],dim[2])

        typecode = imArray.dtype.char

        ar_type = self.__typeDict[typecode]

        complexComponents = 1
        if (typecode == 'F' or typecode == 'D'):
            numComponents = numComponents * 2
            complexComponents = 2

        size = len(imArray.flat)*self.__sizeDict[ar_type]*complexComponents
        self.__import.CopyImportVoidPointer(imArray, size)
        self.__import.SetDataScalarType(ar_type)
        self.__import.SetNumberOfScalarComponents(numComponents)
        extent = self.__import.GetDataExtent()
        self.__import.SetDataExtent(extent[0],extent[0]+dim[2]-1,
                                    extent[2],extent[2]+dim[1]-1,
                                    extent[4],extent[4]+dim[0]-1)
        self.__import.SetWholeExtent(extent[0],extent[0]+dim[2]-1,
                                     extent[2],extent[2]+dim[1]-1,
                                     extent[4],extent[4]+dim[0]-1)

    def GetArray(self):
        return self.__Array

    # a whole bunch of methods copied from vtkImageImport

    def SetDataExtent(self,extent):
        self.__import.SetDataExtent(extent)

    def GetDataExtent(self):
        return self.__import.GetDataExtent()

    def SetDataSpacing(self,spacing):
        self.__import.SetDataSpacing(spacing)

    def GetDataSpacing(self):
        return self.__import.GetDataSpacing()

    def SetDataOrigin(self,origin):
        self.__import.SetDataOrigin(origin)

    def GetDataOrigin(self):
        return self.__import.GetDataOrigin()


def dtypeToVtkType(d_type):
    if np.issubdtype(np.int8, d_type):
        return vtk.VTK_CHAR
    elif np.issubdtype(np.int16, d_type):
        return vtk.VTK_SHORT
    elif np.issubdtype(np.int32, d_type):
        return vtk.VTK_INT
    elif np.issubdtype(np.uint8, d_type):
        return vtk.VTK_UNSIGNED_CHAR
    elif np.issubdtype(np.uint16, d_type):
        return vtk.VTK_UNSIGNED_SHORT
    elif np.issubdtype(np.uint32, d_type):
        return vtk.VTK_UNSIGNED_INT
    else:
        return vtk.VTK_INT

class VtkImageHelper:

    def __init__(self):
        print("imageHelper")

    def createVtkMarchingCube(self, DicomArray, imageInformation):


        dataImporter = vtkImageImportFromArray()
        dataImporter.SetArray(DicomArray)

        #VTK_data = numpy_support.numpy_to_vtk(num_array=DicomArray.ravel(), deep=True, array_type=dtypeToVtkType(DicomArray.dtype))

        #data_string = DicomArray.tostring()
        #dataImporter.CopyImportVoidPointer(VTK_data, len(VTK_data))
        #dataImporter.SetDataScalarType(dtypeToVtkType(DicomArray.dtype))
        #dataImporter.SetNumberOfScalarComponents(1)
        dataImporter.SetDataExtent(imageInformation["imageExtent"])
        #dataImporter.SetDataExtent([0,9,0,9,0,9])
        #dataImporter.SetWholeExtent(imageInformation["imageExtent"])
        dataImporter.SetDataSpacing(imageInformation["imageSpacing"])
        dataImporter.SetDataOrigin(imageInformation["imageOrigin"])

        #writer = vtk.vtkXMLImageDataWriter()
        #writer.SetFileName("/home/christoph/test.vti")
        #writer.SetInputConnection(dataImporter.GetOutputPort())
        #writer.SetDataModeToAscii()
        #writer.Write()

        # An isosurface, or contour value of 500 is known to correspond to the
        # skin of the patient.
        skinExtractor = vtk.vtkMarchingCubes()
        skinExtractor.SetInputConnection(dataImporter.GetOutputPort())
        skinExtractor.ComputeScalarsOff()
        skinExtractor.ComputeGradientsOff()
        skinExtractor.ComputeNormalsOff()
        skinExtractor.SetValue(0, 1)

        # smoothingIterations = 2
        # passBand = 0.01
        # featureAngle = 60.0
        # smoother = vtk.vtkWindowedSincPolyDataFilter()
        # smoother.SetInputConnection(skinExtractor.GetOutputPort())
        # smoother.SetNumberOfIterations(smoothingIterations)
        # smoother.BoundarySmoothingOff()
        # smoother.FeatureEdgeSmoothingOff()
        # smoother.SetFeatureAngle(featureAngle)
        # smoother.SetPassBand(passBand)
        # smoother.NonManifoldSmoothingOn()
        # smoother.NormalizeCoordinatesOn()
        # smoother.Update()
        #
        # normals = vtk.vtkPolyDataNormals()
        # normals.SetInputConnection(smoother.GetOutputPort())
        # normals.SetFeatureAngle(featureAngle)
        #
        # stripper = vtk.vtkStripper()
        # stripper.SetInputConnection(normals.GetOutputPort())

        iOr = imageInformation["imageOrientation"]
        xdir = [float(iOr[0]), float(iOr[1]), float(iOr[2])]
        ydir = [float(iOr[3]), float(iOr[4]), float(iOr[5])]
        normal = [0.0,0.0,0.0]
        vtk.vtkMath.Cross(xdir,ydir,normal)

        matrix = [
        xdir[0] , ydir[0] , normal[0] , 0 ,
        xdir[1] , ydir[1] , normal[1] , 0 ,
        xdir[2] , ydir[2] , normal[2] , 0 ,
        0       , 0       , 0         , 1
        ]

        transform = vtk.vtkTransform()
        transform.SetMatrix(matrix)

        transformFilter = vtk.vtkTransformFilter()
        transformFilter.SetInputConnection(skinExtractor.GetOutputPort())
        transformFilter.SetTransform(transform)

        return transformFilter.GetOutput()
        #contourfilter
        #writer = vtk.vtkXMLPolyDataWriter()
        #writer.SetFileName("/home/christoph/test.vtp")
        #writer.SetInputConnection(transformFilter.GetOutputPort())
        #writer.Write()
