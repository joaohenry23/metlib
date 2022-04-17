# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------------------------------------------------------------
'''
Description: Performs meteorological calculations
Author: Joao Henry Huaman Chinchay
E-mail: joaohenry23@gmail.com
Created date: Apr 17, 2022
'''
#-----------------------------------------------------------------------------------------------------------------------------------
import numpy as np
import xarray as xr
#-----------------------------------------------------------------------------------------------------------------------------------
# finite differences centered
def cdiff(Field, Dim):
   """
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

   """


   try:
      assert type(Field) == np.ndarray or type(Field) == xr.DataArray
   except AssertionError:
      print('\nThe Field must be Numpy array or Xarray\n')
      return


   try:
      assert Dim=='X' or Dim=='x' or Dim=='Y' or Dim=='y' or Dim=='Z' or Dim=='z' or Dim=='T' or Dim=='t'
   except AssertionError:
      print('\nYou need to specify the dimension X, Y, Z or T\n')
      return


   try:
      assert Field.ndim >= 2 and Field.ndim <= 4
   except AssertionError:
      print('\nThe Field must be 2, 3 or 4 Dimensions\n')
      return


   if type(Field) == np.ndarray:
      FieldType = np.ndarray
   elif type(Field) == xr.DataArray:
      CoordsData = Field.coords
      DimsData = Field.dims


      try:
         FieldUnits = Field.units
      except:
         FieldUnits = 'Field_units'


      try:
         FieldLongName = Field.long_name
      except:
         FieldLongName = 'Field_Name'


      FieldType = xr.DataArray
      Field = Field.values



   if Field.ndim==2:

      ny, nx = Field.shape
      dy = dx = 0

      if Dim=='X' or Dim=='x':
         axis = 1
         nx = 1
         dx = 2

      elif Dim=='Y' or Dim=='y':
         axis = 0
         ny = 1
         dy = 2

      Nans = np.full((ny,nx), np.nan)
      Field = np.concatenate((Nans,Field,Nans), axis=axis)
      ny, nx = Field.shape
      CDIFF = Field[dy:,dx:] - Field[:ny-dy,:nx-dx]


   elif Field.ndim==3:

      nz, ny, nx = Field.shape
      dz = dy = dx = 0

      if Dim=='X' or Dim=='x':
         axis = 2
         nx = 1
         dx = 2

      elif Dim=='Y' or Dim=='y':
         axis = 1
         ny = 1
         dy = 2

      elif Dim=='Z' or Dim=='z' or Dim=='T' or Dim=='t':
         axis = 0
         nz = 1
         dz = 2

      Nans = np.full((nz,ny,nx), np.nan)
      Field = np.concatenate((Nans,Field,Nans), axis=axis)
      nz, ny, nx = Field.shape
      CDIFF = Field[dz:,dy:,dx:] - Field[:nz-dz,:ny-dy,:nx-dx]


   elif Field.ndim==4:

      nt, nz, ny, nx = Field.shape
      dt = dz = dy = dx = 0

      if Dim=='X' or Dim=='x':
         axis = 3
         nx = 1
         dx = 2

      elif Dim=='Y' or Dim=='y':
         axis = 2
         ny = 1
         dy = 2

      elif Dim=='Z' or Dim=='z':
         axis = 1
         nz = 1
         dz = 2

      elif Dim=='T' or Dim=='t':
         axis = 0
         nt = 1
         dt = 2

      Nans = np.full((nt,nz,ny,nx), np.nan)
      Field = np.concatenate((Nans,Field,Nans), axis=axis)
      nt, nz, ny, nx = Field.shape
      CDIFF = Field[dt:,dz:,dy:,dx:] - Field[:nt-dt,:nz-dz,:ny-dy,:nx-dx]



   if FieldType == xr.DataArray:
      CDIFF = xr.DataArray(CDIFF, coords=CoordsData, dims=DimsData)
      CDIFF.name = 'cdiff'
      CDIFF.attrs['units'] = FieldUnits
      CDIFF.attrs['long_name'] = 'CDIFF_'+FieldLongName+'_in_'+Dim
      CDIFF.attrs['standard_name'] = 'Centered_finite_difference_of_'+FieldLongName+'_in_'+Dim


   return CDIFF;


#-----------------------------------------------------------------------------------------------------------------------------------
# dynamic calcs
def relative_vorticity(UComp, VComp, Lon=None, Lat=None):

   '''
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

   '''

   if type(UComp) == type(VComp) == np.ndarray:

      try:
         assert type(Lon) == type(Lat) == np.ndarray
      except AssertionError:
         print('\nThe data input (UComp, VComp) is Numpy array, so you need pass 2D array of Lon and Lat, e.g.:')
         print('hcurl(UComp, VComp, 2DLon, 2DLat)\n')
         return
      else:

            dvdx = cdiff(VComp,'X')
            dudy = cdiff(UComp*np.cos(Lat*np.pi/180.0),'Y')
            dx = cdiff(Lon,'X') * np.pi/180.0
            dy = cdiff(Lat,'Y') * np.pi/180.0
            vor = (dvdx/dx-dudy/dy)/(6.37e6*np.cos(Lat*np.pi/180.0))


   elif type(UComp) == type(VComp) == xr.DataArray:

      try:
         assert UComp.dims == VComp.dims
      except AssertionError:
         print('\nThe data input (UComp, VComp) is Xarray.DataArray but they do not have the same dimensions\n')
         return
      else:

         try:
            assert True in [ True if word in (UComp.dims)[-1] else False for word in ['lon','LON','Lon'] ]   and   True in [ True if word in (UComp.dims)[-2] else False for word in ['lat','LAT','Lat'] ]
         except AssertionError:
            print('\nThe data input (UComp, VComp) is Xarray.DataArray and must have unless two dimensions [latitude, longitude]')
            print('If data input have three dimensions their structure must be [level, latitude, longitude] or [time, latitude, longitude]')
            print('If data input have four dimensions their structure must be [time, level, latitude, longitude] or [level, time, latitude, longitude]\n')
            return
         else:

            CoordsData = UComp.coords
            DimsData = UComp.dims

            Lon = UComp.coords[(UComp.dims)[-1]].values
            Lat = UComp.coords[(UComp.dims)[-2]].values
            Lon, Lat = np.meshgrid(Lon, Lat)

            dvdx = cdiff(VComp,'X').values
            dudy = cdiff(UComp*np.cos(Lat*np.pi/180.0),'Y').values
            dx = cdiff(Lon,'X') * np.pi/180.0
            dy = cdiff(Lat,'Y') * np.pi/180.0
            vor = (dvdx/dx-dudy/dy)/(6.37e6*np.cos(Lat*np.pi/180.0))

            vor = xr.DataArray(vor, coords=CoordsData, dims=DimsData)
            vor.name = 'vor'
            vor.attrs['units'] = 's**-1'
            vor.attrs['long_name'] = 'Vorticity'
            vor.attrs['standard_name'] = 'Relative_vorticity_of_wind'


   return vor;

#-----------------------------------------------------------------------------------------------------------------------------------
# dynamic calcs
def absolute_vorticity(UComp, VComp, Lon=None, Lat=None):

   '''
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

   '''

   if type(UComp) == type(VComp) == np.ndarray:

      try:
         assert type(Lon) == type(Lat) == np.ndarray
      except AssertionError:
         print('\nThe data input (UComp, VComp) is Numpy array, so you need pass 2D array of Lon and Lat, e.g.:')
         print('hcurl(UComp, VComp, 2DLon, 2DLat)\n')
         return
      else:

            dvdx = cdiff(VComp,'X')
            dudy = cdiff(UComp*np.cos(Lat*np.pi/180.0),'Y')
            dx = cdiff(Lon,'X') * np.pi/180.0
            dy = cdiff(Lat,'Y') * np.pi/180.0
            omega = 2.0*np.pi/86400.0
            fc = 2*omega*np.sin(Lat*np.pi/180.0)
            avor = (dvdx/dx-dudy/dy)/(6.37e6*np.cos(Lat*np.pi/180.0)) + fc


   elif type(UComp) == type(VComp) == xr.DataArray:

      try:
         assert UComp.dims == VComp.dims
      except AssertionError:
         print('\nThe data input (UComp, VComp) is Xarray.DataArray but they do not have the same dimensions\n')
         return
      else:

         try:
            assert True in [ True if word in (UComp.dims)[-1] else False for word in ['lon','LON','Lon'] ]   and   True in [ True if word in (UComp.dims)[-2] else False for word in ['lat','LAT','Lat'] ]
         except AssertionError:
            print('\nThe data input (UComp, VComp) is Xarray.DataArray and must have unless two dimensions [latitude, longitude]')
            print('If data input have three dimensions their structure must be [level, latitude, longitude] or [time, latitude, longitude]')
            print('If data input have four dimensions their structure must be [time, level, latitude, longitude] or [level, time, latitude, longitude]\n')
            return
         else:

            CoordsData = UComp.coords
            DimsData = UComp.dims

            Lon = UComp.coords[(UComp.dims)[-1]].values
            Lat = UComp.coords[(UComp.dims)[-2]].values
            Lon, Lat = np.meshgrid(Lon, Lat)

            dvdx = cdiff(VComp,'X').values
            dudy = cdiff(UComp*np.cos(Lat*np.pi/180.0),'Y').values
            dx = cdiff(Lon,'X') * np.pi/180.0
            dy = cdiff(Lat,'Y') * np.pi/180.0
            omega = 2.0*np.pi/86400.0
            fc = 2*omega*np.sin(Lat*np.pi/180.0)
            avor = (dvdx/dx-dudy/dy)/(6.37e6*np.cos(Lat*np.pi/180.0)) + fc

            avor = xr.DataArray(avor, coords=CoordsData, dims=DimsData)
            avor.name = 'avor'
            avor.attrs['units'] = 's**-1'
            avor.attrs['long_name'] = 'Absolute_vorticity'
            avor.attrs['standard_name'] = 'Absolute_relative_vorticity_of_wind'


   return avor;

#-----------------------------------------------------------------------------------------------------------------------------------
def divergence(UComp, VComp, Lon=None, Lat=None):

   '''
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

   '''

   if type(UComp) == type(VComp) == np.ndarray:

      try:
         assert type(Lon) == type(Lat) == np.ndarray
      except AssertionError:
         print('\nThe data input (UComp, VComp) is Numpy array, so you need pass 2D array of Lon and Lat, e.g.:')
         print('hdivg(UComp, VComp, 2DLon, 2DLat)\n')
         return
      else:

            dudx = cdiff(UComp,'X')
            dvdy = cdiff(VComp*np.cos(Lat*np.pi/180.0),'Y')
            dx = cdiff(Lon,'X') * np.pi/180.0
            dy = cdiff(Lat,'Y') * np.pi/180.0
            div = (dudx/dx+dvdy/dy)/(6.37e6*np.cos(Lat*np.pi/180.0))


   elif type(UComp) == type(VComp) == xr.DataArray:

      try:
         assert UComp.dims == VComp.dims
      except AssertionError:
         print('\nThe data input (UComp, VComp) is Xarray.DataArray but they do not have the same dimensions\n')
         return
      else:

         try:
            assert True in [ True if word in (UComp.dims)[-1] else False for word in ['lon','LON','Lon'] ]   and   True in [ True if word in (UComp.dims)[-2] else False for word in ['lat','LAT','Lat'] ]
         except AssertionError:
            print('\nThe data input (UComp, VComp) is Xarray.DataArray and must have unless two dimensions [latitude, longitude]')
            print('If data input have three dimensions their structure must be [level, latitude, longitude] or [time, latitude, longitude]')
            print('If data input have four dimensions their structure must be [time, level, latitude, longitude] or [level, time, latitude, longitude]\n')
            return
         else:

            CoordsData = UComp.coords
            DimsData = UComp.dims

            Lon = UComp.coords[(UComp.dims)[-1]].values
            Lat = UComp.coords[(UComp.dims)[-2]].values
            Lon, Lat = np.meshgrid(Lon, Lat)

            dudx = cdiff(UComp,'X').values
            dvdy = cdiff(VComp*np.cos(Lat*np.pi/180.0),'Y').values
            dx = cdiff(Lon,'X') * np.pi/180.0
            dy = cdiff(Lat,'Y') * np.pi/180.0
            div = (dudx/dx+dvdy/dy)/(6.37e6*np.cos(Lat*np.pi/180.0))

            div = xr.DataArray(div, coords=CoordsData, dims=DimsData)
            div.name = 'div'
            div.attrs['units'] = 's**-1'
            div.attrs['long_name'] = 'Divergence'
            div.attrs['standard_name'] = 'Horizontal_divergence_of_wind'


   return div;

#-----------------------------------------------------------------------------------------------------------------------------------

def advection(Field, UComp, VComp, Lon=None, Lat=None):

   '''
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

   '''

   if type(Field) == type(UComp) == type(VComp) == np.ndarray:

      try:
         assert type(Lon) == type(Lat) == np.ndarray
      except AssertionError:
         print('\nThe data input (Field, UComp, VComp) are Numpy array, so you need pass 2D array of Lon and Lat, e.g.:')
         print('hdivg(UComp, VComp, 2DLon, 2DLat)\n')
         return
      else:

            dfdx = cdiff(Field,'X')
            dfdy = cdiff(Field,'Y')
            dx = cdiff(Lon,'X') * np.pi/180.0
            dy = cdiff(Lat,'Y') * np.pi/180.0
            adv = -1.0*( ((UComp*dfdx)/(np.cos(Lat*np.pi/180.0)*dx)) + ((VComp*dfdy)/(dy)) )/6.37e6


   elif type(Field) == type(UComp) == type(VComp) == xr.DataArray:

      try:
         assert Field.dims == UComp.dims == VComp.dims
      except AssertionError:
         print('\nThe data input (Field, UComp, VComp) are Xarray.DataArray but they do not have the same dimensions\n')
         return
      else:

         try:
            assert True in [ True if word in (Field.dims)[-1] else False for word in ['lon','LON','Lon'] ]   and   True in [ True if word in (Field.dims)[-2] else False for word in ['lat','LAT','Lat'] ]
         except AssertionError:
            print('\nThe data input (Field, UComp, VComp) is Xarray.DataArray and must have unless two dimensions [latitude, longitude]')
            print('If data input have three dimensions their structure must be [level, latitude, longitude] or [time, latitude, longitude]')
            print('If data input have four dimensions their structure must be [time, level, latitude, longitude] or [level, time, latitude, longitude]\n')
            return
         else:

            CoordsData = Field.coords
            DimsData = Field.dims

            try:
               UnitsData = Field.units
            except:
               UnitsData = 'Field_units'


            try:
               LongNameData = Field.long_name
            except:
               LongNameData = 'Field_Name'


            Lon = Field.coords[(Field.dims)[-1]].values
            Lat = Field.coords[(Field.dims)[-2]].values
            Lon, Lat = np.meshgrid(Lon, Lat)

            dfdx = cdiff(Field,'X').values
            dfdy = cdiff(Field,'Y').values
            dx = cdiff(Lon,'X') * np.pi/180.0
            dy = cdiff(Lat,'Y') * np.pi/180.0
            adv = -1.0*( ((UComp*dfdx)/(np.cos(Lat*np.pi/180.0)*dx)) + ((VComp*dfdy)/(dy)) )/6.37e6

            adv = xr.DataArray(adv, coords=CoordsData, dims=DimsData)
            adv.name = 'adv'
            adv.attrs['units'] = UnitsData+'/s'
            adv.attrs['long_name'] = LongNameData+'_advection'
            adv.attrs['standard_name'] = 'Horizontal_advection_of_'+LongNameData


   return adv;

#-----------------------------------------------------------------------------------------------------------------------------------

def potential_temperature(Temperature, Levels=None):
   '''
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

   '''

   if type(Temperature) == np.ndarray:

      try:
         #assert Levels is not None
         assert type(Levels) == np.ndarray #type(Levels) == list or
      except AssertionError:
         print('\nYou need pass 1D array of Levels')
         print('potential_temperature(Temperature, Levels)\n')
         return
      else:

         #if isinstance(Levels,list)==True:
         #   Levels = np.array(Levels,dtype=np.float32)

         if Temperature.ndim == 2:
            pass
         elif Temperature.ndim == 3:
            Levels = Levels[:,None,None]
         elif Temperature.ndim == 4:
            Levels = Levels[None,:,None,None]


         PTemp = Temperature*np.power(1000.0/Levels,0.286)


   elif type(Temperature) == xr.DataArray:

      try:
         assert True in [ True if word in (Temperature.dims)[-1] else False for word in ['lon','LON','Lon'] ]   and   True in [ True if word in (Temperature.dims)[-2] else False for word in ['lat','LAT','Lat'] ]
      except AssertionError:
         print('\nThe data input (Temperature) is Xarray.DataArray and must have unless two dimensions [latitude, longitude]')
         print('If data input have three dimensions their structure must be [level, latitude, longitude]')
         print('If data input have four dimensions their structure must be [time, level, latitude, longitude]\n')
         return
      else:

         CoordsData = Temperature.coords
         DimsData = Temperature.dims

         Levels = Temperature.coords[(Temperature.dims)[-3]].values


         if Temperature.ndim == 2:
            pass
         elif Temperature.ndim == 3:
            Levels = Levels[:,None,None]
         elif Temperature.ndim == 4:
            Levels = Levels[None,:,None,None]


         PTemp = Temperature*np.power(1000.0/Levels,0.286)

         PTemp = xr.DataArray(PTemp, coords=CoordsData, dims=DimsData)
         PTemp.name = 'PTemp'
         PTemp.attrs['units'] = 'K'
         PTemp.attrs['long_name'] = 'Potential_temperature'
         PTemp.attrs['standard_name'] = 'Potential_temperature'


   return PTemp;

#-----------------------------------------------------------------------------------------------------------------------------------

def potential_vorticity(Temperature, UComp, VComp, Lon=None, Lat=None, Levels=None):

   '''
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
   '''

   if type(Temperature) == type(UComp) == type(VComp) == np.ndarray:

      try:
         assert type(Lon) == type(Lat) == type(Levels) == np.ndarray
      except AssertionError:
         print('\nThe data input (Temperature, UComp, VComp) are Numpy array, so you need pass 2D array of Lon and Lat,')
         print('and 1D array of Levels, e.g.:')
         print('potential_vorticity(Temperature, UComp, VComp, 2DLon, 2DLat, 1DLevels)\n')
         return
      else:

         if Temperature.ndim == 3:
            Levels2 = Levels[:,None,None]*100.0
         elif Temperature.ndim == 4:
            Levels2 = Levels[None,:,None,None]*100.0


         AVor = absolute_vorticity(UComp, VComp, Lon=Lon, Lat=Lat)
         PTemp = potential_temperature(Temperature, Levels=Levels)
         dx = 6.37e6 * cdiff(Lon,'X') * np.pi/180.0 * np.cos(Lat*np.pi/180.0)
         dy = 6.37e6 * cdiff(Lat,'Y') * np.pi/180.0
         dp = cdiff(Levels2,'Z')
         dPTempdp = cdiff(PTemp,'Z')/dp
         dUCompdp = cdiff(UComp,'Z')/dp
         dVCompdp = cdiff(VComp,'Z')/dp
         dPTempdx = cdiff(PTemp,'X')/dx
         dPTempdy = cdiff(PTemp,'Y')/dy

         PVor = -9.8*(AVor*dPTempdp - dVCompdp*dPTempdx + dUCompdp*dPTempdy)


   elif type(Temperature) == type(UComp) == type(VComp) == xr.DataArray:

      try:
         assert True in [ True if word in (Temperature.dims)[-1] else False for word in ['lon','LON','Lon'] ]   and   True in [ True if word in (Temperature.dims)[-2] else False for word in ['lat','LAT','Lat'] ]
      except AssertionError:
         print('\nThe data input (Temperature, UComp, VComp) is Xarray.DataArray and must have unless three dimensions [levels, latitude, longitude]')
         print('If data input have three dimensions their structure must be [levels, latitude, longitude]')
         print('If data input have four dimensions their structure must be [times, level, latitude, longitude]\n')
         return
      else:

         CoordsData = Temperature.coords
         DimsData = Temperature.dims

         Lon = Temperature.coords[(Temperature.dims)[-1]].values
         Lat = Temperature.coords[(Temperature.dims)[-2]].values
         Levels = Temperature.coords[(Temperature.dims)[-3]].values

         Lon, Lat = np.meshgrid(Lon, Lat)


         if Temperature.ndim == 3:
            Levels = Levels[:,None,None]*100.0
         elif Temperature.ndim == 4:
            Levels = Levels[None,:,None,None]*100.0


         AVor = absolute_vorticity(UComp, VComp).values
         PTemp = potential_temperature(Temperature).values
         dx = 6.37e6 * cdiff(Lon,'X') * np.pi/180.0 * np.cos(Lat*np.pi/180.0)
         dy = 6.37e6 * cdiff(Lat,'Y') * np.pi/180.0
         dp = cdiff(Levels,'Z')
         dPTempdp = cdiff(PTemp,'Z')/dp
         dUCompdp = cdiff(UComp.values,'Z')/dp
         dVCompdp = cdiff(VComp.values,'Z')/dp
         dPTempdx = cdiff(PTemp,'X')/dx
         dPTempdy = cdiff(PTemp,'Y')/dy

         PVor = -9.8*(AVor*dPTempdp - dVCompdp*dPTempdx + dUCompdp*dPTempdy)

         PVor = xr.DataArray(PVor, coords=CoordsData, dims=DimsData)
         PVor.name = 'PVor'
         PVor.attrs['units'] = 's**-1'
         PVor.attrs['long_name'] = 'Potential_vorticity'
         PVor.attrs['standard_name'] = 'Potential_vorticity'


   return PVor;

#-----------------------------------------------------------------------------------------------------------------------------------

