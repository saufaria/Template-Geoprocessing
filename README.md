# Matrix-Project
## Risk matrix automation project

A Geoprocessing service that allow user to identify different types of possible constraints that may represent a risk to an wind onshore project. 
It uses as inputs: 
- a project layout (uid) 
- a Risk Matrix template (Excel file) 

and returns:
- a Json files with 
- a Risk Matrix excel files 
The Json file is used as an input the risk matrix that calculates the risks associated with any particular wind farm project on its initial phases.

This repo contains:

-	Configuration file: Config.py
-	Custom geographic python module: geographicEntities.py
-	Geoprocessing services publishing files: GPScript_publishing_***.py (DEV, STG & PROD)
-	Python geoprocessing script file: Risk_matrix_geoprocessing.py 
-	Readme instructions file: README.md    

## Development Environment:
1. Install Anaconda python modules repository 
2. Clone ArcGIS python standard environment (In order to keep all arcgis required modules already installed)
3. On the new cloned environment > Install modules: Geopandas, Rasterio, Simplejson and Openpyxl

## Configuration:
The config.py file contains lists of the data to be consumed by the geoprocessing file. This data is consumed in form of web services: feature service and image services.
For the feature service layers, contained in the Dict_land dictionary, it is informed the name of the layer, the Arcgis service id, the index number of the layer corresponding the layer position in the repository and the distance used for the spatial join tool to search for neighboring entities.

## Deployment:

In ArcGIs Pro: 
1. Create New Toolbox
2. In the Execution tab of the script tool properties: Import geoprocessing python script(Risk_matrix_geoprocessing.py)
3. In properties of the script tool -> define the parameters -> 
    -  Input: the input layout variable name : 
            1. Layoutid input: Name layout_id, Datatype String, Type Required and Direction Input.
    -  Outputs: The outputs of the script: 
            1. Json output: Name responseJson, Datatype String, Type Derived and Direction Output.
            2. Excel file: Name exportExcel, Datatype File, Type Derived and Direction Output

## Publishing:

Open the GPScript_publishing_Dev*.py file in a Python IDE. *Dev, stg or Prod
Adjust the values of the following variables: 
"sc" : point to a publish folder
"intbx" : point to the path and name of the toolbox previously created
"input_layout" : Any valid layout GUID for the tool to run with the script tool while publishing
"result" : Call script tool using arcpy.{tool name}_{toolbox alias}
"server_conn" : Path to the server connection file (.ags)
"service_name" :  Name of the published service

## Custom modules:
Third-part modules in python scripts need to be placed on the same folder as the main script file so it can properly read it. Example: GeographicEntities.py
