# Functions
Click on the item to see the function and their description.
<details><summary>Central difference finites</summary>
<br>

**cdiff**(Field, Dim)
```
   Calculates a centered finite difference of Numpy array or Xarray.DataArray.


   Parameters
   ----------
   Field: Numpy array or Xarray.DataArray
          Their structure can be:
          - 1D [x]
          - 2D [y,x]
          - 3D [z,y,x]
          - 4D [t,z,y,x]

   Dim: String (str)
        Defines axis of derivative and can be 'X', 'Y', 'Z', 'T'.


   Returns
   -------
   CDIFF: Numpy array or Xarray.DataArray
          Centered finite difference in Dim of Field. The shape is the same that input(Field).
```
<br>
</details>

<details><summary>Relative vorticity</summary>
<br>

**relative_vorticity**(UComp, VComp, Lon=None, Lat=None)
```
   Calculates the relative vorticity of horizontal wind.


   Parameters
   ----------
   UComp: Numpy array or Xarray.DataArray
          Zonal component of wind. Their structure can be:
          - 2D [y,x]
          - 3D [z,y,x] or [t,y,x]
          - 4D [t,z,y,x]

   VComp: Numpy array or Xarray.DataArray
          Meridional component of wind. Their structure can be:
          - 2D [y,x]
          - 3D [z,y,x] or [t,y,x]
          - 4D [t,z,y,x]

   Lon: Numpy array
        2D array with the longitudes of UComp and VComp.
        If UComp and VComp are xarray.DataArray is not necessary define this parameter.

   Lat: Numpy array
        2D array with the latitudes of UComp and VComp.
        If UComp and VComp are xarray.DataArray is not necessary define this parameter.


   Returns
   -------
   vor: Numpy array or Xarray.DataArray
        Relative vorticity of Ucomp and Vcomp [s**-1]
```
<br>
</details>

<details><summary>Absolute vorticity</summary>
<br>

**absolute_vorticity**(UComp, VComp, Lon=None, Lat=None)
```
   Calculates the absolute vorticity of horizontal wind.


   Parameters
   ----------
   UComp: Numpy array or Xarray.DataArray
          Zonal component of wind. Their structure can be:
          - 2D [y,x]
          - 3D [z,y,x] or [t,y,x]
          - 4D [t,z,y,x]

   VComp: Numpy array or Xarray.DataArray
          Meridional component of wind. Their structure can be:
          - 2D [y,x]
          - 3D [z,y,x] or [t,y,x]
          - 4D [t,z,y,x]

   Lon: Numpy array
        2D array with the longitudes of UComp and VComp.
        If UComp and VComp are xarray.DataArray is not necessary define this parameter.

   Lat: Numpy array
        2D array with the latitudes of UComp and VComp.
        If UComp and VComp are xarray.DataArray is not necessary define this parameter.


   Returns
   -------
   avor: Numpy array or Xarray.DataArray
         Absolute relative vorticity of Ucomp and Vcomp [s**-1]
```
<br>
</details>

<details><summary>Divergence</summary>
<br>

**divergence**(UComp, VComp, Lon=None, Lat=None)
```
   Calculates the divergence of horizontal wind or some vector field.


   Parameters
   ----------
   UComp: Numpy array or Xarray.DataArray
          Zonal component of wind. Their structure can be:
          - 2D [y,x]
          - 3D [z,y,x] or [t,y,x]
          - 4D [t,z,y,x]

   VComp: Numpy array or Xarray.DataArray
          Meridional component of wind. Their structure can be:
          - 2D [y,x]
          - 3D [z,y,x] or [t,y,x]
          - 4D [t,z,y,x]

   Lon: Numpy array
        2D array with the longitudes of UComp and VComp.
        If UComp and VComp are xarray.DataArray is not necessary define this parameter.

   Lat: Numpy array
        2D array with the latitudes of UComp and VComp.
        If UComp and VComp are xarray.DataArray is not necessary define this parameter.


   Returns
   -------
   div: Numpy array or Xarray.DataArray
        Horizontal divergence of Ucomp and Vcomp [1/s]
        Negative divergence is also known as convergence.
```
<br>
</details>

<details> <summary>Advection</summary>
<br>

**advection**(Field, UComp, VComp, Lon=None, Lat=None)
```
   Calculates the horizontal adveccion of Field. 


   Parameters
   ----------
   Field: Numpy array or Xarray.DataArray
          Their structure can be:
          - 2D [y,x]
          - 3D [z,y,x] or [t,y,x]
          - 4D [t,z,y,x]

   UComp: Numpy array or Xarray.DataArray
          Zonal component of wind. Their structure can be:
          - 2D [y,x]
          - 3D [z,y,x] or [t,y,x]
          - 4D [t,z,y,x]

   VComp: Numpy array or Xarray.DataArray
          Meridional component of wind. Their structure can be:
          - 2D [y,x]
          - 3D [z,y,x] or [t,y,x]
          - 4D [t,z,y,x]

   Lon: Numpy array
        2D array with the longitudes of UComp and VComp.
        If UComp and VComp are xarray.DataArray is not necessary define this parameter.

   Lat: Numpy array
        2D array with the latitudes of UComp and VComp.
        If UComp and VComp are xarray.DataArray is not necessary define this parameter.


   Returns
   -------
   adv: Numpy array or Xarray.DataArray
        Horizontal advection of Field [Field_units/s]
```
<br>
</details>

<details><summary>Potential temperature</summary>
<br>

**potential_temperature**(Temperature, Levels=None)
```
   Calculates the potential temperature.


   Parameters
   ----------
   Temperature: Numpy array or Xarray.DataArray
                Temperature field in Kelvin. Their structure can be:
                - 2D [y,x]
                - 3D [z,y,x] or [t,y,x]
                - 4D [t,z,y,x]


   Levels: Numpy array
           1D array with pressure levels of Temperature.


   Returns
   -------
   PTemp: Numpy array or Xarray.DataArray
          Potential temperature [K].
```
<br>
</details>

<details><summary>Potential vorticity</summary>
<br>

**potential_vorticity**(Temperature, UComp, VComp, Lon=None, Lat=None, Levels=None)
```
   Calculates the baroclinic potential vorticity.


   Parameters
   ----------
   Temperature: Numpy array or Xarray.DataArray
                Temperature field in Kelvin. Their structure can be:
                - 3D [z,y,x]
                - 4D [t,z,y,x]

   UComp: Numpy array or Xarray.DataArray
          Zonal component of wind. Their structure can be:
          - 3D [z,y,x]
          - 4D [t,z,y,x]

   VComp: Numpy array or Xarray.DataArray
          Meridional component of wind. Their structure can be:
          - 3D [z,y,x]
          - 4D [t,z,y,x]

   Lon: Numpy array
        2D array with the longitudes of UComp and VComp.
        If UComp and VComp are xarray.DataArray is not necessary define this parameter.

   Lat: Numpy array
        2D array with the latitudes of UComp and VComp.
        If UComp and VComp are xarray.DataArray is not necessary define this parameter.


   Levels: Numpy array
           1D array with pressure levels of Temperature.
           If UComp and VComp are xarray.DataArray is not necessary define this parameter.


   Returns
   -------
   PVor: Numpy array or Xarray.DataArray
         Baroclinic potential voticity [1/s].
```
<br>
</details>
<br><br>
