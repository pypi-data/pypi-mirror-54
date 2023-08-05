
# Documentation for Adampy_devel

## Description

Adampy allows to retrieve, analyze and download data hosted within the ADAM environment.

## Installation Procedure
```
virtualenv -p `which python3` venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip3 install adampy
```
**********

## Functions

***********

### getCollections

The getCollections function returns all available collections in the selected endpoint.

```
adam.getCollections(endpoint).get_data()
```
#### Parameters

* endpoint (str) - The name of the endpoint to get the collections from.

#### Returns

* List with name of all collections

#### Examples

To get the list of collections:

```python
import adampy as adam

collections = adam.getCollections('wcs-eo4sdcr.adamplatform.eu').get_data()

print(collections)

```

------------------------------------------------------------------

### getImage

The getImage function returns a numpy array containing the requested image. The image can be saved using Rasterio.
```
adam.getImage(endpoint, collection, time_t, min_lat = -90, max_lat = 90, min_long = -180, max_long = 180, token = 'None', geometry = 'None', masking = False, fname = 'image.tif').get_data()
```

#### Parameters

* endpoint (str) - The name of the endpoint to get the collections from.
* collection (str) - The name of the collection
* time_t (str) - The time or time range in the format yyyy-mm-ddThh:mm:ss
* min_lat (int or float; optional) - Minimum latitude of the bounding box (range -90 to 90)
* max_lat (int or float; optional) - Maximum latitude of the bounding box (range -90 to 90)
* min_long (int or float; optional) - Minimum longitude of the bounding box (range -180 to 180)
* max_long (int or float; optional) - Maximum longitude of the bounding box (range -180 to 180)
* token (str; optional) - Token to access restricted collections
* geometry (shp, geojson or kml file; optional) - Geometry to mask the output image
* masking (True or False; Default False ; optional) - Activate the masking option
* fname (str; optional) - Name for the output file, if not stated fname = image.tif

#### Returns

* Numpy array with the requested image and Metadata information for the image

#### Examples

Get a global image for a particular time

```python
import adampy as adam
import matplotlib
import matplotlib.pyplot as plt

image, out_meta = adam.getImage('wcs-eo4sdcr.adamplatform.eu', 'Z_CAMS_C_ECMF_PM10_4326_04','2019-03-26T00:00:00').get_data()

plt.subplots(figsize=(13,13))
plt.imshow(image)


```

Get a bounding box for a particular time

```python
import adampy as adam
import matplotlib
import matplotlib.pyplot as plt

image, out_meta = adam.getImage('wcs-eo4sdcr.adamplatform.eu', 'Z_CAMS_C_ECMF_PM10_4326_04','2019-03-26T00:00:00',10,20,-10,50).get_data()

plt.subplots(figsize=(13,13))
plt.imshow(image)

```

Get a bounding box for a time range

```python
import adampy as adam
import matplotlib
import matplotlib.pyplot as plt

image, out_meta = adam.getImage('wcs-eo4sdcr.adamplatform.eu', 'Z_CAMS_C_ECMF_PM10_4326_04','2019-03-26T00:00:00,2019-03-27T23:59:59',10,20,-10,50).get_data()

plt.subplots(figsize=(13,13))
plt.imshow(image)

```

Get a masked image for a time range

```python
import adampy as adam
import matplotlib
import matplotlib.pyplot as plt

image, out_meta = adam.getImage('wcs-eo4sdcr.adamplatform.eu', 'Z_CAMS_C_ECMF_PM10_4326_04','2019-03-26T00:00:00,2019-03-27T23:59:59', geometry = 'polygon.shp', masking = True).get_data()

plt.subplots(figsize=(13,13))
plt.imshow(image)

```
-----------

### getTimeSeries

The getTimeSeries function returns two arrays containing the values and time stamps for the request Latitude and Longitude location.
```
adam.getTimeSeries(endpoint, collection, time_t, lat, long, token = 'None').get_data()
```

#### Parameters

* endpoint (str) - The name of the endpoint to get the collections from.
* collection (str) - The name of the collection
* time_t (str) - The time or time range in the format yyyy-mm-ddThh:mm:ss
* lat (int or float; optional) - Minimum latitude of the bounding box (range -90 to 90)
* long (int or float; optional) - Minimum longitude of the bounding box (range -180 to 180)
* token (str; optional) - Token to access restricted collections

#### Returns

* Two arrays containing the values and time stamps for the request Latitude and Longitude location

#### Examples

```python
import adampy as adam

data, times = adam.getTimeSeries('wcs-eo4sdcr.adamplatform.eu', 'ERA-Interim_temp2m_4326_05','2014-03-26T00:00:00,2014-03-30T23:59:59', 25, 60).get_data()

```

-----------

### getAnimation

The getAnimation function crates an animated gif of a dataset given a start and end date.
```
adam.getTimeSeries(endpoint, collection, start_date, end_date, min_lat = -90, max_lat = 90, min_long = -180, max_long = 180, token = 'None', frame_duration = 0.1, legend = False).get_data()
```

#### Parameters

* endpoint (str) - The name of the endpoint to get the collections from.
* collection (str) - The name of the collection
* start_date (date object) - The start date of the animation
* end_date (date object) - The end date of the animation
* min_lat (int or float; optional) - Minimum latitude of the bounding box (range -90 to 90)
* max_lat (int or float; optional) - Maximum latitude of the bounding box (range -90 to 90)
* min_long (int or float; optional) - Minimum longitude of the bounding box (range -180 to 180)
* max_long (int or float; optional) - Maximum longitude of the bounding box (range -180 to 180)
* token (str; optional) - Token to access restricted collections
* frame_duration (float or int; optional) - Frame duration in seconds
* legend (True or False; optional) - Add legend to the animation


#### Returns

* An animated GIF of the dataset for a given start and end date.

#### Examples

```python
import adampy as adam
from datetime import datetime, timedelta, date

start_date = date(2014,3,1)
end_date = date(2014,3,5)

gif_fname = adam.getAnimation('wcs-eo4sdcr.adamplatform.eu', 'NEXGDDP-pr_4326_025',start_date = start_date, end_date=end_date, frame_duration = 0.3, legend = False).get_data()

```


```python

```
