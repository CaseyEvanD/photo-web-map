# -*- coding: utf-8 -*-
"""
Script for listing photos in dir and extracting their coordinates to csv file.
"""
from datetime import datetime
from exif import Image
from geojson import dump, Feature, FeatureCollection, Point
from glob import glob
from os import path


def dms2dd(dms_coord, ref):
    """Convert Degree Min Sec coordinate to Decimal Degree format."""
    dd_coord = dms_coord[0] + (dms_coord[1] / 60.0) + (dms_coord[2] / 3600.0)
    if ref == 'S' or ref == 'W':
        dd_coord = -1.0 * dd_coord
    return dd_coord


# Specify target directory -- use image_dir
image_dir = r'E:\photos'
image_type = r'\*.jpg'
image_path = image_dir + image_type

# Initialize process variables
image_path_list = glob(image_path) #glob.glob()
img_count = 0
img_features = []

# Extract image data
for img_path in image_path_list:
    img_count += 1
    img_name = path.basename(img_path) #os.path.basename()
    
    try:
        with open(img_path, 'rb') as img_file:
            img_data = Image(img_file) #exif.Image()
    except:
        print('Unable to open file {}'.format(img_path))
        
    if img_data.has_exif:
        try:
            img_dtstr = img_data.datetime
            img_dtobj = datetime.strptime(img_dtstr, '%Y:%m:%d %H:%M:%S') #datetime.datetime.strptime()
            img_datetime = img_dtobj.strftime('%Y-%m-%d %H:%M:%S')
            
            img_date = img_dtobj.strftime('%Y-%m-%d')
            img_time = img_dtobj.strftime('%H:%M:%S')
        except AttributeError:
            print('{} missing datetime'.format(image_path))
            img_datetime = None
            img_time = None
        
        try:
            lon_dms = img_data.gps_longitude
            lon_ref = img_data.gps_longitude_ref
            img_lon = dms2dd(lon_dms, lon_ref)
            
            lat_dms = img_data.gps_latitude
            lat_ref = img_data.gps_latitude_ref
            img_lat = dms2dd(lat_dms, lat_ref)
            
            img_geom = Point((img_lon, img_lat)) #geojson.Point()
        except AttributeError:
            print('{} missing gps coordinate'.format(image_path))
            img_lon = None
            img_lat = None
            img_geom = None
            
    else:
        print(img_count, img_path, 'has no EXIF data')
        
        img_datetime = None
        img_time = None
        img_lon = None
        img_lat = None
        img_geom = None
        
    img_feat = Feature(id=img_count, #geojson.Feature()
                       geometry=img_geom,
                       properties={'Name':img_name,
                                   'Path':img_path,
                                   'Datetime':img_datetime,
                                   'Date':img_date,
                                   'Time':img_time,
                                   'Lon':img_lon,
                                   'Lat':img_lat})
    img_features.append(img_feat)
feature_collection = FeatureCollection(img_features) #geojson.FeatureCollection()

# Specify output directory for geojson file -- use geojson_dir
geojson_dir = r'E:\photo-web-map'
geojson_name = r'photo_data.geojson'
geojson_path = geojson_dir + '\\' + geojson_name

# Export image data to geojson file
with open(geojson_path, 'w') as geojson_file:
    dump(feature_collection, geojson_file, indent=4) #geojson.dump()

# EOF