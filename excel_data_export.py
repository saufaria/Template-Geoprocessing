import arcpy
import os
from openpyxl import load_workbook
import json

#------------------------------Global Functions---------------------------    
# Transfor the distance from meters to kilometers
def distancesToKM(objList):
    objectsList = []
    values = objList
    for value in values:
        value["distance"] = round(value["distance"]/1000,2)
        objectsList.append(value)
    return objectsList

# Returns the nearest item in given list
def getMinDistanceObject(objList):
    distanceList = []
    for item in objList:
        distanceList.append(item["distance"])
    item = distanceList.index(min(distanceList))
    return objList[item]

# Filter only applied in MAB risk
def filterMabZones(param):
    tampCentList = []
    transList = []
    for value in param:
        if value["zone"] == "centrale" or value["zone"] == "tampon":
            tampCentList.append(value)
        elif value["zone"] == "transition":    
            transList.append(value)
    return {"tampon":tampCentList,"trans":transList}

# Returns the items inside a given distance
# optional param minDistance was created to exclude Renewal parcs projects
def filterByDistance(objList,distance, minDistance=0.5):
    objects = []
    objectsList = []
    for value in objList:
        if value["distance"] < distance and value["distance"] > minDistance:
            objectsList.append(value)
    return {"number":len(objectsList),"entities":objectsList}      

#------------------------------------------------THEMES--------------------------------------------------------
# Fill Faune/Flore tab in excel
def fauneFlore(data, wb):
    wbNature = wb["FauneFlore"]
    nationalReserves=[]           
    for risk in data["entities"]:  
        if risk["risk"] == "Rnn":
            if risk["number_of_entities"] > 0:
                for rnn in risk["entities"]:
                    nationalReserves.append(rnn)
        if risk["risk"] == "Rnr":
            if risk["number_of_entities"] > 0:
                for rnr in risk["entities"]:
                    nationalReserves.append(rnr)
        if risk["risk"] == "Rb_onf":
            if risk["number_of_entities"] > 0:
                for rb in risk["entities"]:
                    nationalReserves.append(rb)
        if len(nationalReserves) > 0:
            objList = distancesToKM(nationalReserves)
            minRN = getMinDistanceObject(objList)
            wbNature["D25"] = minRN["distance"]
            wbNature["E25"] = minRN["url_fiche"]
            nationalReserves=[]         
        if risk["risk"] == "Apb":
            if risk["number_of_entities"] > 0:
                objList = distancesToKM(risk["entities"])
                apb = getMinDistanceObject(objList)
                wbNature["D24"] = apb["distance"]
                wbNature["E24"] = apb["url_fiche"]                       
        if risk["risk"] == "Cdl":
            if risk["number_of_entities"] > 0:
                objList = distancesToKM(risk["entities"])
                cdl = getMinDistanceObject(objList)
                wbNature["D26"] = cdl["distance"]
                wbNature["E26"] = cdl["url_fiche"]
        if risk["risk"] == "Cen":
            if risk["number_of_entities"] > 0:
                objList = distancesToKM(risk["entities"])
                cen = getMinDistanceObject(objList)
                wbNature["D27"] = cen["distance"]
                wbNature["E27"] = cen["url_fiche"]
        if risk["risk"] == "Mab":
            if risk["number_of_entities"] > 0:
                objList = distancesToKM(risk["entities"])
                zonesFilter = filterMabZones(objList)
                tampon = getMinDistanceObject(zonesFilter['tampon'])
                wbNature["D28"] = tampon["distance"]
                wbNature["E28"] = tampon["url_fiche"]
                trans = getMinDistanceObject(zonesFilter['trans'])
                wbNature["D29"] = trans["distance"]
                wbNature["E29"] = trans["url_fiche"]
        if risk["risk"] == "ParcNational_coeur":
            if risk["number_of_entities"] > 0:
                objList = distancesToKM(risk["entities"])
                pnc = getMinDistanceObject(objList)
                wbNature["D30"] = pnc["distance"]
                wbNature["E30"] = pnc["url_fiche"]
        if risk["risk"] == "ParcNational_adhesion":
            if risk["number_of_entities"] > 0:
                objList = distancesToKM(risk["entities"])
                pna = getMinDistanceObject(objList)
                wbNature["D31"] = pna["distance"]
                wbNature["E31"] = pna["url_fiche"]
        if risk["risk"] == "Zps":
            if risk["number_of_entities"] > 0:
                objList = distancesToKM(risk["entities"])
                zps = getMinDistanceObject(objList)
                wbNature["D32"] = zps["distance"]
                wbNature["E32"] = zps["url_fiche"]
        if risk["risk"] == "Sic_zsc":
            if risk["number_of_entities"] > 0:
                objList = distancesToKM(risk["entities"])
                sic = getMinDistanceObject(objList)
                wbNature["D33"] = sic["distance"]
                wbNature["E33"] = sic["url_fiche"]
        if risk["risk"] == "Zico":
            if risk["number_of_entities"] > 0:
                objList = distancesToKM(risk["entities"])
                zico = getMinDistanceObject(objList)
                wbNature["D35"] = zico["distance"]
        if risk["risk"] == "Ramsar":
            if risk["number_of_entities"] > 0:
                objList = distancesToKM(risk["entities"])
                ramsar = getMinDistanceObject(objList)
                wbNature["D36"] = ramsar["distance"]
                wbNature["E36"] = ramsar["url_fiche"]
        if risk["risk"] == "Pnr":
            if risk["number_of_entities"] > 0:
                objList = distancesToKM(risk["entities"])
                pnr = getMinDistanceObject(objList)
                wbNature["D37"] = pnr["distance"]
                wbNature["E37"] = pnr["url_fiche"]
        if risk["risk"] == "Znieff1_inpn":
            if risk["number_of_entities"] > 0:
                objList = distancesToKM(risk["entities"])
                znief1 = getMinDistanceObject(objList)
                wbNature["D38"] = znief1["distance"]
                wbNature["E38"] = znief1["url_fiche"]
        if risk["risk"] == "Znieff2_inpn":
            if risk["number_of_entities"] > 0:
                objList = distancesToKM(risk["entities"])
                znief2 = getMinDistanceObject(objList)
                wbNature["D39"] = znief2["distance"]
                wbNature["E39"] = znief2["url_fiche"]                  

# Fill Paysage tab in excel
def landscape(data,wb):
    wbLandscape = wb["Paysage"]
    drealSites = []
    for risk in data["entities"]:
        if risk["risk"] == "SitesUnesco":
            if risk["number_of_entities"] > 0:
                objList = distancesToKM(risk["entities"])
                entity = getMinDistanceObject(objList)
            if entity["distance"] < 30:
                wbLandscape["D11"] =entity['distance']
                wbLandscape["E11"] = f'=HYPERLINK("{entity["url_fiche"]}", "{entity["name"]}")'
        if risk["risk"] == "ZonageUnesco":
            if risk["number_of_entities"] > 0:
                objList = distancesToKM(risk["entities"])
                entity = getMinDistanceObject(objList)
            if entity["distance"] < 30:
                wbLandscape["D12"] =entity['distance']
                wbLandscape["E12"] = f'=HYPERLINK("{entity["url_fiches"]}", "{entity["nom_bien"]}")'
        if risk["risk"] == "MonumentHistoriqueMomentum":
            if risk["number_of_entities"] > 0:
                objList = distancesToKM(risk["entities"])
                filter5km = filterByDistance(objList,5,0)
                monuments5km = ''
                for item in filter5km["entities"]:
                    monuments5km+=f'{item["nom"]}\n '
                filter10km = filterByDistance(objList,10,0)
                monuments10km = ''
                for item in filter10km["entities"]:
                    monuments10km+=f'{item["nom"]}\n '
                wbLandscape["D17"] =filter5km['number']
                wbLandscape["E17"] = monuments5km
                wbLandscape["D18"] =filter10km['number']
                wbLandscape["E18"] = monuments10km
        # -------Removed due unused data in excel------------
        # if risk["risk"] == "MonumentHistoriqueMerimee":
        #     if risk["number_of_entities"] > 0:
        #         entity = getMinDistanceObject(risk["entities"])
        #         wbLandscape["D12"] =entity['distance']
        #         wbLandscape["E12"] = entity["nom"]
        if risk["risk"] == "PatrimoineRemarquable":
            if risk["number_of_entities"] > 0:
                objList = distancesToKM(risk["entities"])
                entity = getMinDistanceObject(objList)
                wbLandscape["D14"] = entity['distance']
                wbLandscape["E14"] = entity['libelle']
        if risk["risk"] == "DrealInscrit":
            if risk["number_of_entities"] > 0:
                for entity in risk["entities"]:
                    drealSites.append(entity)
        if risk["risk"] == "DrealClasse":
            if risk["number_of_entities"] > 0:
                for entity in risk["entities"]:
                    drealSites.append(entity)
            drealSitesKM = distancesToKM(drealSites)
            entity = getMinDistanceObject(drealSitesKM)
            wbLandscape["D13"] =entity['distance']
            wbLandscape["E13"] = f'=HYPERLINK("{entity["url"]}", "{entity["nom"]}")'
        if risk["risk"] == "ParcsEoliens":
            if risk["number_of_entities"] > 0:
                objList = distancesToKM(risk["entities"])
                wbLandscape["D24"] = filterByDistance(objList,5,0)["number"]
                wbLandscape["D25"] = filterByDistance(objList,10,0)["number"]
        if risk["risk"] == "Pnr":
            if risk["number_of_entities"] > 0:
                objList = distancesToKM(risk["entities"])
                pnr2km = filterByDistance(objList,2,0)["number"]
                if pnr2km > 0:
                    wbLandscape["D19"] = "OUI"
# Reads an excel file in the geoprocessing scratch folder and saves the changes into another file to be send to user
def exportExcel(json_data):
    wb = load_workbook('matrice.xlsm',read_only=False, keep_vba=True, keep_links=True)
    for theme in json_data:
        if theme["theme"] == "NATURE":
            fauneFlore(theme, wb)
        if theme["theme"] == "LANDSCAPE":
            landscape(theme, wb)
    wb.save(arcpy.env.scratchFolder+ "/" + 'outfile.xlsm')
    file = os.path.join(arcpy.env.scratchFolder+ "/" + 'outfile.xlsm')
    return file