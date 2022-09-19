#####################################  Geoprocessing Tool ############################################
# This is a template for a Geoprocessing tool
#  It uses Python 3 language and Arcgis geospatial libraries
# Also some Opensource python librairies
# The output format is Json and Excel
# Publishing scripts are located in the Deploy folder

# Authors: 
# Company: QEnergy France
# Date: 
##################################################################################################################

import arcpy
from arcgis.gis import *
import simplejson as json
# import geographicEntities as ge #Local python script must be place on same folder as geoprocessing script
import requests
import config
import geopandas as gpd  ## Opensource librairies must be installed, also in Server
import rasterio as rio   ## Opensource librairies must be installed, also in Server
import excel_data_export #Local python script must be place on same folder as geoprocessing script

arcpy.env.overwriteOutput = True

import config
############################################# Script Variables #######################################################

gis = GIS(config.settings['portal'], config.settings['username'], config.settings['password'], verify_cert=False)

turbines_url = gis.content.get(config.settings['layout_service']).layers[0]  

layout_id = "layout_globalid='{}'".format(arcpy.GetParameterAsText(0)) 

####################################### INPUT / OUTPUT Geoprocessing definition ######################################
input_layer = arcpy.MakeFeatureLayer_management(turbines_url.url, "in_layer", where_clause=layout_id)

############################################## Vector themes function  ###################################################
def processing_vector(layout_input, theme_dictionary):

    risk_svc = gis.content.get(theme_dictionary["NATURE"]["Rnn"]['service_id']) # Get theme id in the qrcgis server
    risk_id = theme_dictionary["NATURE"]["Rnn"]['layer_index'] # Get risk index in the list of subthemes
    risk_url = risk_svc.layers[risk_id] 
    risk_buffer = theme_dictionary["NATURE"]["Rnn"]['buffer']

    risk_result = arcpy.MakeFeatureLayer_management(risk_url.url,"risk").getOutput(0)

    risk_entity = arcpy.SelectLayerByLocation_management(risk_result,"WITHIN_A_DISTANCE",layout_input,risk_buffer) 

    return str(risk_entity)

################################################## Raster themes function  ########################################################
def processing_raster(layout_url, theme_dictionary):
    image_theme = list(theme_dictionary.keys())
    image_result = []

    for subtheme in image_theme:
        gise_meso = []

        for raster in theme_dictionary[subtheme]:
            # Read the input layout layer with its layout global ID and create a geodataframe (gdf)

            #fc = gis.content.get(layout_url).layers[0] # arcgis.features.FeatureLayer(layout_url)
            layout_query=layout_url.query(where=layout_id)
            layout_json = layout_query.to_geojson
            gdf_inlayout=gpd.read_file(layout_json)
            # gdf_inlayout = gpd.read_file(layout_url + f"/query?where={layout_id}&f=pjson&outFields=*")

            # Create xy coordinates field on the geodataframe
            coord_list = [[x,y] for x,y in zip(gdf_inlayout['geometry'].x , gdf_inlayout['geometry'].y)]
            gdf_inlayout['coords'] = coord_list

            # Create and get bounding box coordinates for the layout zone 
            bounds = gdf_inlayout.total_bounds
            bounds_buffer10 = [x - 10 for x  in bounds[:2]] + [x + 10 for x  in bounds[2:]] # Adding a 10 meter bufer to the bbox to avoid border pixel issue 
            bbox_xy = f'{bounds_buffer10[0]},{bounds_buffer10[1]},{bounds_buffer10[2]},{bounds_buffer10[3]}'

            gisement_url = f"https://az-prod-gis-002.enr-fr.com:6443/arcgis/rest/services/develop/{raster}/ImageServer/exportImage?bbox={bbox_xy}&bboxSR=&format=tiff&pixelType=F32&noDataInterpretation=esriNoDataMatchAny&interpolation=+RSP_BilinearInterpolation&adjustAspectRatio=true&lercVersion=1&f=pjson"
            
            # Request the image server to get a raster TIF for the selected area (bbox)
            requete = requests.get(gisement_url, verify = False) ### Config file ###
            response = requete.json()
            tif_url = response["href"]

            # Open the tif raster with raterio module
            gis_raster = rio.open(tif_url)

            # Create a "value" field with the values extracted from the raster
            gdf_inlayout['value'] = [x[0] for x in gis_raster.sample(coord_list)] # Pandas function sample() extracts a sample of data according to a given codition
            
            raster_result = gdf_inlayout.to_json()
            # gise_meso.append(raster_result)

    return raster_result 

################################################  JSON OUTPUT  #####################################################################
vector_output = processing_vector(input_layer, config.dic_vector)
raster_output = processing_raster(turbines_url, config.dic_raster)
matrix_output = vector_output #+ raster_output
matrix_json=json.dumps(matrix_output,ensure_ascii=False,indent=4,default=str,ignore_nan=True)

# export = excel_data_export.exportExcel(matrix_output)

# Sets a specified parameter property by index using an object. This function is used to pass objects from a script to a script tool.
responseJson = arcpy.SetParameter(1, matrix_json)
# exportFile = arcpy.SetParameter(2,export)

################################################  END of CODE  #####################################################################