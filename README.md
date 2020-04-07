# metlib
Python package to performs meteorological calculations



# Requirements
- [numpy](https://numpy.org/)
- [xarray](http://xarray.pydata.org/en/stable/)



# Usage
See the next jupyter notebook examples where are calculated the relative vorticity, the horizontal divergence of wind and the temperature advection, also are showed how to creates lat-lon plots and vertical profile plots along latitude, longitude or time.

- Read data with [netCDF4](https://github.com/Unidata/netcdf4-python):
  * creates lat-lon plots using [basemap](https://matplotlib.org/basemap/)/[cartopy](https://scitools.org.uk/cartopy/docs/latest/), [matplotlib](https://matplotlib.org/) and [pcolormesh](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.pcolormesh.html)/[contourf](https://matplotlib.org/api/_as_gen/matplotlib.pyplot.contourf.html) (**[example](https://github.com/joaohenry23/metlib/blob/master/examples/ex01.ipynb)**).
  * creates vertical profile plots using [matplotlib](https://matplotlib.org/) and [pcolormesh](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.pcolormesh.html)/[contourf](https://matplotlib.org/api/_as_gen/matplotlib.pyplot.contourf.html) (**[example](https://github.com/joaohenry23/metlib/blob/master/examples/ex04.ipynb)**).

- Read data with [xarray](http://xarray.pydata.org/en/stable/):
  * creates lat-lon plots using [basemap](https://matplotlib.org/basemap/)/[cartopy](https://scitools.org.uk/cartopy/docs/latest/), [matplotlib](https://matplotlib.org/) and [pcolormesh](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.pcolormesh.html)/[contourf](https://matplotlib.org/api/_as_gen/matplotlib.pyplot.contourf.html) (**[example](https://github.com/joaohenry23/metlib/blob/master/examples/ex02.ipynb)**).
  * creates lat-lon plots using [xarray.plot](http://xarray.pydata.org/en/stable/plotting.html), [cartopy](https://scitools.org.uk/cartopy/docs/latest/), [matplotlib](https://matplotlib.org/) and [pcolormesh](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.pcolormesh.html)/[contourf](https://matplotlib.org/api/_as_gen/matplotlib.pyplot.contourf.html) (**[example](https://github.com/joaohenry23/metlib/blob/master/examples/ex03.ipynb)**).
  * creates vertical profile plots using [matplotlib](https://matplotlib.org/) and [pcolormesh](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.pcolormesh.html)/[contourf](https://matplotlib.org/api/_as_gen/matplotlib.pyplot.contourf.html) (**[example](https://github.com/joaohenry23/metlib/blob/master/examples/ex05.ipynb)**).
  * creates vertical profile plots using [xarray.plot](http://xarray.pydata.org/en/stable/plotting.html), [matplotlib](https://matplotlib.org/) and [pcolormesh](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.pcolormesh.html)/[contourf](https://matplotlib.org/api/_as_gen/matplotlib.pyplot.contourf.html) (**[example](https://github.com/joaohenry23/metlib/blob/master/examples/ex06.ipynb)**).



# Installation
You can install metlib on Python 2 or 3 on Linux, Windows or other, using the following commands.
\
\
**From github**

- Download ZIP (**metlib-master.zip**) and following commands (I recommend make it inside your favorite environment python):
```
# Recommended method
unzip metlib-master.zip
cd metlib-master
pip install .
cd ..  # it is necessary to leave the installation folder
```
or
```
unzip metlib-master.zip
cd metlib-master
python setup.py install
cd ..  # it is necessary to leave the installation folder
```

**Note:** I recomend install packages inside your favorite enviroment python


- Or also, cloning the github package  (I recommend make it inside your favorite environment python):
```
clone https://github.com/joaohenry23/metlib.git
cd metlib
python setup.py install
cd ..  # it is necessary to leave the installation folder
```
\
\
**Check if package was installed**

Open python version or the python environment where was installed the package and write:
```
import metlib
```



# Support
If you have any questions, do not hesitate to write to:
```
joaohenry23@gmail.com

```

