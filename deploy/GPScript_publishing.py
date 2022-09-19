import arcpy
from arcgis.gis import GIS
# import geographicEntities as ge
import os

arcpy.env.overwriteOutput = True

# A publishing folder path on your PC:
sc = r"C:\Dev\Arcgis\RiskMatrixGeoprocessing\toolbox\dev\publish"

#  Set inputs and run the script tool
intbx = os.path.join(r"C:\Dev\Arcgis\RiskMatrixGeoprocessing\toolbox\dev", 'RiskMatrix_dev.tbx') # Path for the Toolbox
input_layout = '{17BA3401-BFF9-4122-AD27-A9D7351B5FBA}' # A layout global ID in order to run the Risk Matrix tool 

try:
    arcpy.ImportToolbox(intbx)

    # Call geoprocessing using arcpy.{tool name}_{toolbox alias}
    result = arcpy.MatrixProjectDev_RiskMatrixDev(input_layout)
    print("Tool runs successfully")

except arcpy.ExecuteError:
    #print("Running tool error", sys.exc_info())#[0]
    print("Running tool error: ", arcpy.GetMessages(2))

# SERVER CONNECTION
# Important the server connection file requires a connection to the MANAGER
server_conn = r"C:\Dev\Arcgis\RiskMatrixGeoprocessing\toolbox\dev\connection\arcgis on az-prod-gis-002.enr-fr.com.ags" # Path for the server connection file

try:
    # Create a service definition draft
    draft_file = os.path.join(sc,'gpservice.sddraft')
    draft_file_return = arcpy.CreateGPSDDraft(result = result,
                                                folder_name= "develop",
                                                out_sddraft = draft_file,
                                                service_name = 'RiskMatrixDev',
                                                server_type = 'ARCGIS_SERVER',
                                                connection_file_path = server_conn,
                                                copy_data_to_server = False,
                                                showMessages = "Info")

    print("Service Definition Draft is ready.")

    # Analyse the return from creating the service definition draft
    if (draft_file_return['errors']):
        print("error message = " + (str(draft_file_return['errors']) or 'None'))
    else:
        print("warning message = " + (str(draft_file_return['warnings']) or 'None'))

    # Stage the service
    definition_file =os.path.join(sc, 'gpservice1.sd')
    arcpy.StageService_server(draft_file, definition_file)
    print("Service Staged.")

    # Upload service definition
    arcpy.UploadServiceDefinition_server(definition_file, server_conn)
    print("Service published.")

except arcpy.ExecuteError:
    print("Publishing error:", arcpy.GetMessages(2))