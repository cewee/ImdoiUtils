import numpy as np
import vtk
from ImageImportFromArray import vtkImageImportFromArray

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
