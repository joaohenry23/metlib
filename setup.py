import setuptools

try:
   from numpy.distutils.core import Extension
   from numpy.distutils.core import setup
except ImportError:
   print('Numpy need be installed for extensions to be compiled.')
   exit()
else:

   with open("README.md", "r") as fh:
      long_description = fh.read()

   import numpy.distutils.core
   mod = numpy.distutils.core.Extension(name = 'metlib.flib', sources = ['metlib/flib.f90'])
   numpy.distutils.core.setup(
      name = 'metlib',
      version="0.0.1.1",
      author="Joao Henry Huamán Chinchay",
      author_email="joaohenry23@gmail.com",
      description="Python package to performs meteorological calculations",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/joaohenry23/metlib",
      packages = ['metlib'],
      classifiers=[
         "Programming Language :: Python :: 2",
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: BSD License",
         "Operating System :: OS Independent",
      ],
      python_requires='>=2.7',
      install_requires=["numpy","xarray",],
      ext_modules = [mod],
   )

