import setuptools
from distutils.core import setup

setup(
    name='ImdroiTools',
    version='0.1alpha-3',
    packages=['imdroi_reporting','imdroi_dicom',],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    install_requires=[
          'numpy',
          'pydicom',
          'pyvtk',
          'vtk'
      ],
)
