from os.path import dirname, join
from os import scandir
import numpy as np
import pydicom
import vtk #TODO replace by numpy

def sqdist(dataset):
    vector = dataset.ImagePositionPatient
    return sum(x*x for x in vector)

class DicomReader:

    def __init__(self, filepath):
        self.filepath = filepath
        self.imagearray = []
        self.imageInformation = {}
        self.read()

    def getArrayDicom(self):
        return self.ArrayDicom

    def getImageInformation(self):
        return self.imageInformation

    def read(self):
        # fetch the path to the test data
        print('Path to the DICOM directory: {}'.format(self.filepath))
        # load the data

        base_dir = dirname(self.filepath)
        for entry in scandir(base_dir):
            if entry.is_file():
                ds = pydicom.dcmread(entry.path)
                self.imagearray.append(ds)

        self.imagearray.sort(key=sqdist)
        exDataset = self.imagearray[0]

        self.imageInformation["imageOrientation"] = exDataset.ImageOrientationPatient
        rows = int(exDataset.Rows)
        cols = int(exDataset.Columns)

        self.imageInformation["imageExtent"] = [0,cols-1,0,rows-1,0,len(self.imagearray)-1]
        spacing = exDataset.PixelSpacing
        spacing.append(1.0)
        self.imageInformation["imageSpacing"] = spacing
        self.imageInformation["imageOrigin"] = exDataset.ImagePositionPatient

        if len(self.imagearray) > 1:
            exDataset2 = self.imagearray[1]
            origin2 = exDataset2.ImagePositionPatient
            imageVector = [0,0,0]
            for i in range(3):
                imageVector[i] = exDataset2.ImagePositionPatient[i]-exDataset.ImagePositionPatient[i]

            spacing[2] = vtk.vtkMath.Normalize(imageVector)
            self.imageInformation["imageNormal"] = imageVector
            self.imageInformation["imageSpacing"] = spacing

        # Load dimensions based on the number of rows, columns, and slices (along the Z axis)
        ConstPixelDims = (len(self.imagearray), rows, cols)

        # Load spacing values (in mm)
        ConstPixelSpacing = (float(exDataset.PixelSpacing[0]), float(exDataset.PixelSpacing[1]), 1.0)
        #x = np.arange(0.0, (ConstPixelDims[0]+1)*ConstPixelSpacing[0], ConstPixelSpacing[0])
        #y = np.arange(0.0, (ConstPixelDims[1]+1)*ConstPixelSpacing[1], ConstPixelSpacing[1])
        #z = np.arange(0.0, (ConstPixelDims[2]+1)*ConstPixelSpacing[2], ConstPixelSpacing[2])

        self.ArrayDicom = np.zeros(ConstPixelDims, dtype=exDataset.pixel_array.dtype)


        for idx,image_dataset in enumerate(self.imagearray):
            # store the raw image data
            self.ArrayDicom[idx, :, :] = image_dataset.pixel_array
