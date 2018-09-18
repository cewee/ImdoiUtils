from os.path import dirname, join
from os import scandir
from pprint import pprint
import numpy as np
import pydicom

def sqdist(dataset):
    vector = dataset.ImagePositionPatient
    return sum(x*x for x in vector)

class DicomReader:

    def __init__(self, filepath):
        self.filepath = filepath
        self.imagearray = []
        self.read()

    def getArrayDicom(self):
        return self.ArrayDicom

    def read(self):
        # fetch the path to the test data
        print('Path to the DICOM directory: {}'.format(self.filepath))
        # load the data

        base_dir = dirname(self.filepath)
        for entry in scandir(base_dir):
            if entry.is_file():
                ds = pydicom.dcmread(entry.path)
                #self.myprint(ds)
                #print(ds.SOPInstanceUID)
                #print(ds.ImagePositionPatient)
                self.imagearray.append(ds)

        self.imagearray.sort(key=sqdist)
        ConstPixelDims = (int(image_dataset.Rows), int(image_dataset.Columns), len(self.imagearray))
        self.ArrayDicom = np.zeros(ConstPixelDims, dtype=image_dataset.pixel_array.dtype)

        for idx,image_dataset in enumerate(self.imagearray):
            #print(image_dataset.ImagePositionPatient)
            #print([image_dataset.Rows,image_dataset.Columns])
            # store the raw image data
            self.ArrayDicom[:, :, idx] = image_dataset.pixel_array
