from setuptools import setup, find_packages, Extension
import numpy

setup(
    name='miplib',
    version='1.0',
    packages=find_packages(),
    install_requires=['numpy', 'scipy', 'h5py', 'SimpleITK', 'jpype1',
                      'matplotlib', 'numba', 'pyculib', 'pandas', 'pims', 'scikit-image'],
    entry_points={
        'console_scripts': [
            'miplib.import = miplib.bin.import:main',
            'miplib.correlatem = miplib.bin.correlatem:main',
            'miplib.transform = miplib.bin.transform:main',
            'miplib.fuse = miplib.bin.fuse:main',
            'miplib.register = miplib.bin.register:main',
            'miplib.deconvolve = miplib.bin.deconvolve:main',
            'miplib.resolution = miplib.bin.resolution:main',
            'miplib.ism = miplib.bin.ism:main',
            'pyimq.main = miplib.bin.pyimq:main',
            'pyimq.util.blurseq = miplib.bin.utils.create_blur_sequence:main',
            'pyimq.util.imseq = miplib.bin.utils.create_photo_test_set:main',
            'pyimq.subjective = miplib.bin.subjective:main',
            'pyimq.power = miplib.bin.power:main'
        ]
    },
    platforms=["any"],
    url='https://github.com/sakoho81/miplib',
    download_url="https://github.com/sakoho81/miplib/archive/v1.0.tar.gz",
    license='BSD',
    author='Sami Koho',
    author_email='sami.koho@gmail.com',
    description='miplib software was created for Tomographic processing '
                'of STED super-resolution microscopy images.',
    ext_modules=[
        Extension(
            'miplib.processing.ops_ext',
            ['miplib/processing/src/ops_ext.c'],
            include_dirs=[numpy.get_include()]),
        Extension(
            'miplib.data.io._tifffile',
            ['miplib/data/io/src/tifffile.c'],
            include_dirs=[numpy.get_include()]),
        Extension(
            'miplib.psf._psf',
            ['miplib/psf/src/psf.c'],
            include_dirs=[numpy.get_include()]),
    ],
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: BSD License',  
    'Programming Language :: Python :: 3.6',
  ]
)
