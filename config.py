# -*- coding: utf-8 -*-

settings = {
    'layout_service' : '761015d8dff547c791d47304ae15669b', # Appel service ID for the projet layout services 
    'portal'     : "https://gisportal.enr-fr.com/arcgis",
    'username'   : "geoprocessing",
    'password'   : "geoprocessing2022",
}

dic_vector = {
        "LANDSCAPE":{
                        'SitesUnesco':{
                                'service_id': "dbc38e58bfcd422da2a0e202e2f2e704", #"https://az-prod-gis-002.enr-fr.com/arcgis/rest/services/develop/paysage/FeatureServer/193",
                                'layer_index':4,
                                'buffer': '30000' # Distance en metres aux sites UNESCO (30 km)
                                },

                        },

        "NATURE":{
                        'Rnn':{
                                'service_id':'9d311698fd3a47c2889b37783a6c915e',
                                'layer_index':34,
                                'buffer': '50000'
                                },
 
                        },
}

dic_raster = {
        'GISEMENT':['Mesoscale_80m','Mesoscale_100m']
}  
        