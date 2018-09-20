import argparse
from DicomReader import DicomReader
from DicomVtkInterface import VtkImageHelper
import os
import vtk

class DicomWorker:

    def __init__(self, path):
        DicomReader(path).read()

if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    #apg = ap.add_argument_group(title="Input Output")
    #apg.add_argument("-i", "--input", help="Input 7 Segment Image", type=str, default="7SegInput.png")
    #apg.add_argument("-o", "--output", help="Output 7 Segment Font", type=str, default="7SegOutput.bmp")
    #apg.add_argument("-b", "--background", help="Background color", type=int, nargs=3, default=[3, 17, 34])
    #apg.add_argument("-c", "--color", help="Segment color", type=int, nargs=3, default=[255, 255, 0])
    #apg.add_argument("-r", "--rainbow", help="Segment color", action='store_true')
    #apg.add_argument("-s", "--skewness", help="Italic factor", type=float, default=0)

    #args = ap.parse_args(sys.argv[1:])

    dw = DicomReader("/data/image/tcia/110/")

    imageVtk = VtkImageHelper()
    print(dw.getImageInformation())
    test = imageVtk.createVtkMarchingCube(dw.getArrayDicom(), dw.getImageInformation())
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName("/home/christoph/test.vtp")
    writer.SetInputData(test)
    writer.Write()
