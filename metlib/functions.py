# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------------------------------------------------------------
'''
Description: Performs meteorological calculations
Author: Joao Henry Huaman Chinchay
E-mail: joaohenry23@gmail.com
Created date: Apr 06, 2020
'''
#-----------------------------------------------------------------------------------------------------------------------------------
import numpy as np
import xarray as xr
from . import flib
#-----------------------------------------------------------------------------------------------------------------------------------
# finite differences centered
def cdiff(field, Dim):
   """
   Performs a centered difference operation of numpy array or xarray.DataArray.
   The function use a fortran subroutine to perform a quick calculation.


   Parameters
   ----------
   field: array with maximum 4 dimensions. The data structure must be:
          ['X'], ['Y','X'], ['Z','Y','X'] or ['T','Z','Y','X']
   Dim: (str) define axis of derivative that can be 'X', 'Y', 'Z', 'T'.


   Returns
   -------
   CDIFF: ndrray. The shape is the same that input(field).
          Centered finite difference in Dim of field

   """


   try:
      assert type(field) == np.ndarray or type(field) == xr.DataArray
   except AssertionError:
      print('\nThe field must be numpy array or xarray\n')
      return


   try:
      assert Dim=='X' or Dim=='x' or Dim=='Y' or Dim=='y' or Dim=='Z' or Dim=='z' or Dim=='T' or Dim=='t'
   except AssertionError:
      print('\nYou need to specify the dimension X, Y, Z or T\n')
      return


   try:
      assert field.ndim >= 2 and field.ndim <= 4
   except AssertionError:
      print('\nThe field must be 2, 3 or 4 Dimensions\n')
      return


   if type(field) == np.ndarray:
      fieldType = np.ndarray
   elif type(field) == xr.DataArray:
      CoordsData = field.coords
      DimsData = field.dims


      try:
         fieldUnits = field.units
      except:
         fieldUnits = 'Field_units'


      try:
         fieldLongName = field.long_name
      except:
         fieldLongName = 'Field_Name'


      fieldType = xr.DataArray
      field = field.values


   # replaces np.nan before pass to fortran
   field = np.where(np.isnan(field)==True,-999.99,field)



   if field.ndim==2:
      if Dim=='X' or Dim=='x':
         axis = 1
      elif Dim=='Y' or Dim=='y':
         axis = 0

      CDIFF = flib.cdiff2d(field, axis)

   elif field.ndim==3:
      if Dim=='X' or Dim=='x':
         axis = 2
      elif Dim=='Y' or Dim=='y':
         axis = 1
      elif Dim=='Z' or Dim=='z' or Dim=='T' or Dim=='t':
         axis = 0

      CDIFF = flib.cdiff3d(field, axis)

   elif field.ndim==4:
      if Dim=='X' or Dim=='x':
         axis = 3
      elif Dim=='Y' or Dim=='y':
         axis = 2
      elif Dim=='Z' or Dim=='z':
         axis = 1
      elif Dim=='T' or Dim=='t':
         axis = 0

      CDIFF = flib.cdiff4d(field, axis)


   CDIFF = np.where(CDIFF<-990.0, np.nan, CDIFF)


   if fieldType == xr.DataArray:
      CDIFF = xr.DataArray(CDIFF, coords=CoordsData, dims=DimsData)
      CDIFF.name = 'cdiff'
      CDIFF.attrs['units'] = fieldUnits
      CDIFF.attrs['long_name'] = 'CDIFF_'+fieldLongName+'_in_'+Dim
      CDIFF.attrs['standard_name'] = 'Centered_finite_difference_of_'+fieldLongName+'_in_'+Dim


   return CDIFF;


#-----------------------------------------------------------------------------------------------------------------------------------
# dynamic calcs
def hcurl(UComp, VComp, Lon=None, Lat=None):

   '''
   Calculates vertical component of curl (vorticity) of numpy array or xarray.DataArray.
   The dimension of array can be:
      - 2D [y,x]
      - 3D [z,y,x] or [t,y,x]
      - 4D [t,z,y,x]


   Parameters
   ----------
   UComp: (M, N) ndarray
   VComp: (M, N) ndarray
   Lon: (M, N) ndarray
   Lat: (M, N) ndarray


   Returns
   -------
   vor: (M,N) ndarray
        Relative vorticity of Ucomp and Vcomp [s**-1]

   '''

   if type(UComp) == type(VComp) == np.ndarray:

      try:
         assert type(Lon) == type(Lat) == np.ndarray
      except AssertionError:
         print('The data input (UComp, VComp) is np.ndarray, so you need pass 2D array of Lon and Lat, e.g.:')
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
         print('The data input (UComp, VComp) is xr.DataArray but they do not have the same dimensions\n')
         return
      else:

         try:
            assert (UComp.dims)[-1] in ['longitude','Longitude','lon','Lon','long','Long','longitud','Longitud'] or (UComp.dims)[-2] in ['latitude','Latitude','lat','Lat','lati','Lati','latitud','Latitud']
         except AssertionError:
            print('The data input (UComp, VComp) is xr.DataArray and must have unless two dimensions [latitude, longitude]')
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
def hdivg(UComp, VComp, Lon=None, Lat=None):

   '''
   Calculates the horizontal divergence of numpy array or xarray.DataArray.
   The dimension of array can be:
      - 2D [y,x]
      - 3D [z,y,x] or [t,y,x]
      - 4D [t,z,y,x]


   Parameters
   ----------
   UComp: (M, N) ndarray
   VComp: (M, N) ndarray
   Lon: (M, N) ndarray
   Lat: (M, N) ndarray


   Returns
   -------
   div: (M,N) ndarray
         Horizontal divergence of Ucomp and Vcomp [s**-1]

   '''

   if type(UComp) == type(VComp) == np.ndarray:

      try:
         assert type(Lon) == type(Lat) == np.ndarray
      except AssertionError:
         print('The data input (UComp, VComp) is np.ndarray, so you need pass 2D array of Lon and Lat, e.g.:')
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
         print('The data input (UComp, VComp) is xr.DataArray but they do not have the same dimensions\n')
         return
      else:

         try:
            assert (UComp.dims)[-1] in ['longitude','Longitude','lon','Lon','long','Long','longitud','Longitud'] or (UComp.dims)[-2] in ['latitude','Latitude','lat','Lat','lati','Lati','latitud','Latitud']
         except AssertionError:
            print('The data input (UComp, VComp) is xr.DataArray and must have unless two dimensions [latitude, longitude]')
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

def hadv(Field, UComp, VComp, Lon=None, Lat=None):

   '''
   Calculates the horizontal adveccion of Field. The Field is a numpy array or xarray.DataArray.
   The dimension of Field array can be:
      - 2D [y,x]
      - 3D [z,y,x] or [t,y,x]
      - 4D [t,z,y,x]


   Parameters
   ----------
   Field: (M, N) ndarray
   UComp: (M, N) ndarray
   VComp: (M, N) ndarray
   Lon: (M, N) ndarray
   Lat: (M, N) ndarray


   Returns
   -------
   adv: (M,N) ndarray
         Horizontal advection of Field [Field_units/s]

   '''

   if type(Field) == type(UComp) == type(VComp) == np.ndarray:

      try:
         assert type(Lon) == type(Lat) == np.ndarray
      except AssertionError:
         print('The data input (Field, UComp, VComp) are np.ndarray, so you need pass 2D array of Lon and Lat, e.g.:')
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
         print('The data input (Field, UComp, VComp) are xr.DataArray but they do not have the same dimensions\n')
         return
      else:

         try:
            assert (Field.dims)[-1] in ['longitude','Longitude','lon','Lon','long','Long','longitud','Longitud'] or (Field.dims)[-2] in ['latitude','Latitude','lat','Lat','lati','Lati','latitud','Latitud']
         except AssertionError:
            print('The data input (Field, UComp, VComp) is xr.DataArray and must have unless two dimensions [latitude, longitude]')
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


