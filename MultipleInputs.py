from mpl_toolkits.basemap import Basemap, shiftgrid, addcyclic
import gdal
import matplotlib.pyplot as plt
import numpy as np
#np.set_printoptions( threshold = np.nan )
import pandas as pd
#pd.set_option( "display.max_rows", None )

class Data:

    def __init__( self, link ):

        self.source = link
        self.x = self.opener()[0]
        self.y = self.opener()[1]
        self.data = self.opener()[2]

    def opener( self ):

        '''
        # This helps to troubleshoot problems with the opening of grib2 files.
        gdal.UseExceptions()
        ds = None
        try:
            
            ds = gdal.Open( self.source, gdal.GA_ReadOnly )

        except RuntimeError, err:
            
            print( "Exception: ", err )
            exit( 1 )
        '''
        ds = gdal.Open( self.source, gdal.GA_ReadOnly )

        data = ds.ReadAsArray()
        gt = ds.GetGeoTransform()
        proj = ds.GetProjection()

        xres = gt[1]
        yres = gt[5]

        xsize = ds.RasterXSize
        ysize = ds.RasterYSize

        # get the edge coordinates and add half the resolution 
        # to go to center coordinates
        xmin = gt[0] + xres * 0.5
        xmax = gt[0] + (xres * xsize) - xres * 0.5
        ymin = gt[3] + (yres * ysize) + yres * 0.5
        ymax = gt[3] - yres * 0.5

        ds = None

        # Create the latitudes and longitudes according to our minimum and maximum values,
        # also according to the step or resolution of the grid
        xx = np.arange( xmin, xmax + xres, xres )
        yy = np.arange( ymax + yres, ymin, yres )
        
        # If you are plotting the data directly from python, uncomment the following line.
        #data, xx = shiftgrid( 180.0, data, xx, start = False )

        x, y = np.meshgrid( xx, yy )

        return x, y, data;

# Note that the links change to the location in your own computer where you store the grib2 files.
# Wind grib2 file.
linkOne = "C:\Users\Paula\Downloads\pgbf2018102406.01.2018102406.grb2"
dataOne = Data( linkOne )
wind = dataOne.data
# Latitude and Longitude.
xWind = dataOne.x
yWind = dataOne.y

# Temperature grib2 file.
linkTwo = "C:\Users\Paula\Downloads\enspost.t00z.prcp_24hbc (3).grib2"
dataTwo = Data( linkTwo )
temp = dataTwo.data
# Latitude and Longitude.
xTemp = dataTwo.x
yTemp = dataTwo.y

# Precipitation grib2 file.
linkThree = "C:\Users\Paula\Downloads\ge10pt.t12z.pgrb2a.0p50_bcf003"
dataThree = Data( linkThree )
prec = dataThree.data
# Latitude and Longitude.
xPrec = dataThree.x
yPrec = dataThree.y

# Ice grib2 file.
linkFour = "C:\Users\Paula\Downloads\seaice.t00z.grb.grib2"
dataFour = Data( linkFour )
ice = dataFour.data
# Latitude and Longitude.
xIce = dataFour.x
yIce = dataFour.y

'''
# This helps to troubleshoot problems with the opening of grib2 files.
gdal.UseExceptions()
ds = None
try:
    
    ds = gdal.Open( 'C:\Users\Paula\Downloads\AODModelForecast.grib2', gdal.GA_ReadOnly )

except RuntimeError, err:
    
    print( "Exception: ", err )
    exit( 1 )
'''

'''
# Ozone grib2 file.
linkFour = 'C:\Users\Paula\Downloads\waves.grib2'
dataFour = Data( linkFour )
ozon = dataFour.data
# Latitude and Longitude.
xOzon = dataFour.x
yOzon = dataFour.y
'''

# Make the data available for Pandas'.
# Wind.
dfWind = pd.DataFrame( list( zip( xWind.flatten(), yWind.flatten(), wind.flatten() ) ), \
columns = ["WindLatitude", "WindLongitude", "Wind"] )

# Temperature.
dfTemp = pd.DataFrame( list( zip( xTemp.flatten(), yTemp.flatten(), temp.flatten() ) ), \
columns = ["TempLatitude", "TempLongitude", "Temperature"] )     

# Precipitation.
dfPrec = pd.DataFrame( list( zip( xPrec.flatten(), yPrec.flatten(), prec.flatten() ) ), \
columns = ["PrecLatitude", "PrecLongitude", "Precipitation"] )

# Ice.
dfIce = pd.DataFrame( list( zip( xIce.flatten(), yIce.flatten(), ice.flatten() ) ), \
columns = ["IceLatitude", "IceLongitude", "Ice"] )

# Write the data to Excel xlsl file.
writer = pd.ExcelWriter( "C:\Users\Paula\Desktop\Felipe\IceLatLong.xlsx" )

# Write each DataFrame to a different sheet.
dfWind.to_excel( writer, "Sheet1", index = False )
dfTemp.to_excel( writer, "Sheet2", index = False )
dfPrec.to_excel( writer, "Sheet3", index = False )
dfIce.to_excel( writer, "Sheet4", index = False )

# Close and output to Excel.

writer.save()

'''
# Construct a map from the data we already have using Basemap.

# Mercator
#m = Basemap(projection='merc',llcrnrlat=-85,urcrnrlat=85,\
#            llcrnrlon=-180,urcrnrlon=180,lat_ts=0,resolution='c')

# Robinson
#m = Basemap(projection='robin', lon_0=0, resolution='c')

# Cylindrical
m = Basemap(llcrnrlon=-180.0,llcrnrlat=-85.0,urcrnrlon=180.0,urcrnrlat=85.0,
            resolution='c',projection='cyl',lon_0=0.0,lat_0=0.0)

# plot the data (first layer) data[0,:,:].T
im1 = m.pcolormesh( xWind, yWind, wind[0,:,:], shading = "flat", cmap=plt.cm.jet )

# annotate
m.drawcountries()
m.drawcoastlines(linewidth=.5)

plt.show()
'''
