'''
Created on Mar 3, 2014
Modified: 2015-02-10 by DAT
Updated: 2015-06-19 by DAT

@author: kyleg
'''

import os
from arcpy import (AcceptConnections, Append_management, CalculateField_management, Copy_management,
                    CopyFeatures_management, Dissolve_management, DisconnectUser, env,
                    Erase_analysis, ListUsers, MakeFeatureLayer_management,
                    FeatureToLine_management, Exists, Delete_management,
                    SelectLayerByAttribute_management, SelectLayerByLocation_management,
                    Union_analysis)  # @UnusedImport
                    
tempFeaturesGDB = r'\\gisdata\ArcGIS\GISdata\GDB\CCL_Scratch_Boundary.gdb'
mainFeaturesGDB = r'Database Connections\SDEPROD_GIS.sde'
mainFeaturesUser = r'GIS.Administrative_Boundary\GIS.CITY_LIMITS'
mainFeaturesFullPath = os.path.join(mainFeaturesGDB, mainFeaturesUser)
inMemoryFeaturesGDB = r'in_memory'


def DisconnectHarshly_SDEPROD():
    admin_workspace = r"Database Connections\SDEPROD_SDE.sde"
    env.workspace = admin_workspace
    users = ListUsers(admin_workspace) #
    print users
    DisconnectUser(admin_workspace, "All")
    AcceptConnections(admin_workspace, False)


def AllowConnections_SDEPROD():
    admin_workspace = r"Database Connections\SDEPROD_SDE.sde"
    env.workspace = admin_workspace
    AcceptConnections(admin_workspace, True)


def CityLimitsMod():
    env.overwriteOutput = True
    env.workspace = tempFeaturesGDB
    
    ModFile = r'CITY_LIMITS_MODS_KDOT_1'
    TaxFile = r'CITY_LIMITS_KDOR_1'
    KDOTCity = r'CITY_LIMITS_1'
    CityTemp = r'CITY_TEMP'
    CityOutlines = r'CITY_LIMITS_LN_1'
    
    featureList = [ModFile, TaxFile, KDOTCity, CityTemp, CityOutlines]
    
    for featureName in featureList:
        mainFeatureLocation = mainFeaturesFullPath + featureName
        tempFeatureLocation = os.path.join(tempFeaturesGDB, featureName)
        
        try:
            Delete_management(tempFeatureLocation)
        except:
            pass
            
        Copy_management(mainFeatureLocation, tempFeatureLocation)
    
    tempFeatureModFile = os.path.join(tempFeaturesGDB, ModFile)
    tempFeatureTaxFile = os.path.join(tempFeaturesGDB, TaxFile)
    tempFeatureCityTemp = os.path.join(tempFeaturesGDB, CityTemp)
    tempFeatureKDOTCity = os.path.join(tempFeaturesGDB, KDOTCity)
    tempFeatureCityOutlines = os.path.join(tempFeaturesGDB, CityOutlines)
    
    CityLimitsAdd = "CITY_LIMITS_MODS_ADD"
    CityLimitsSub = "CITY_LIMITS_MODS_SUBTRACT"
    
    todaysLoadDate = str(datetime.datetime.now())[0:4] + str(datetime.datetime.now())[5:7] + str(datetime.datetime.now())[8:10]
    
    CalculateField_management(tempFeatureModFile,"LOAD_DATE", todaysLoadDate, "PYTHON_9.3", "#")
    MakeFeatureLayer_management(tempFeatureModFile, CityLimitsAdd,"MODTYPE = 'ADD'", "#", "#")
    MakeFeatureLayer_management(tempFeatureModFile, CityLimitsSub,"MODTYPE = 'SUBTRACT'", "#", "#")
    
    DisconnectHarshly_SDEPROD()
    AllowConnections_SDEPROD()
    
    Append_management(CityLimitsAdd, tempFeatureCityTemp, "NO_TEST", "#", "#")
    
    Erase_analysis(tempFeatureTaxFile, CityLimitsSub, tempFeatureCityTemp)
    
    dissolveFieldList = ["CITYNUMBER", "CITY", "COUNTY", "DIST", "TYPE", "POPCENSUS", "POPCURRENT", "ID1"]
    statisticsFieldList = [["LOAD_DATE", "MAX"]]
    
    Dissolve_management(tempFeatureCityTemp, tempFeatureKDOTCity, dissolveFieldList, statisticsFieldList, "MULTI_PART", "DISSOLVE_LINES")
    
    FeatureToLine_management(tempFeatureKDOTCity, tempFeatureCityOutlines, "0.01 Feet", "ATTRIBUTES")
    
    # Will have to copy the data from the tempFeaturesGDB to the mainFeaturesGDB eventually
    # but wait on that for now to make sure that the correct data is actually
    # generated in the tempFeaturesGDB.
    # Might need to get SDE to copy over the GIS.Dataset\GIS.<layer> features, if that's
    # a possibility.


def Custom_Erase(inFeature1, inFeature2, outFeature):
    # Instead of erase, might try a union, then selection for only the features
    # that do not have their centers within the 2nd feature class,
    # or that are not entirely within the 2nd feature class,
    # then output the selected features.
    # MakeFeatureLayer, Union, SelectByLocation, CopyFeatures.
    tempUnionFeatureClass = r'in_memory\UnionTemp'
    unionList = list()
    unionList.append(inFeature1)
    unionList.append(inFeature2)
    
    Union_analysis(unionList, tempUnionFeatureClass, "ALL")
    
    tempUnionLayer = MakeFeatureLayer_management(tempUnionFeatureClass, "UnionLayer")
    tempFeature2 = MakeFeatureLayer_management(inFeature2, "Feature2")
    
    SelectLayerByLocation_management(tempUnionLayer, "HAVE_THEIR_CENTER_IN", tempFeature2)
    SelectLayerByLocation_management(tempUnionLayer, "WITHIN", tempFeature2, "0 Feet", "ADD_TO_SELECTION")
    CopyFeatures_management(tempUnionLayer, r'\\gisdata\ArcGIS\GISdata\GDB\CCL_Scratch_Boundary.gdb\TempUnionSelection')
    SelectLayerByAttribute_management(tempUnionLayer, "SWITCH_SELECTION")
    CopyFeatures_management(tempUnionLayer, r'\\gisdata\ArcGIS\GISdata\GDB\CCL_Scratch_Boundary.gdb\TempUnionSelectionSwitch')
    CopyFeatures_management(tempUnionLayer, outFeature)


def CityLimitsMod_OLD():
    env.overwriteOutput = True
    env.workspace = mainFeaturesLocation
    modfile = r'Database Connections\SDEPROD_GIS.sde\GIS.CITY_LIMITS_MODS_KDOT_1'
    taxfile = r'Database Connections\SDEPROD_GIS.sde\GIS.CITY_LIMITS_KDOR_1'
    cityLimitsAdd = "CITY_LIMITS_MODS_ADD"
    cityLimitsSub = "CITY_LIMITS_MODS_SUBTRACT"
    CalculateField_management(modfile,"LOAD_DATE","str(datetime.datetime.now( ))[0:4]+str(datetime.datetime.now( ))[5:7]+str(datetime.datetime.now( ))[8:10]","PYTHON_9.3","#")
    MakeFeatureLayer_management(modfile, cityLimitsAdd,"MODTYPE = 'ADD'","#","#")
    MakeFeatureLayer_management(modfile, cityLimitsSub,"MODTYPE = 'SUBTRACT'","#","#")
    KDOTcity = r'Database Connections\SDEPROD_GIS.sde\GIS.CITY_LIMITS_1'
    CityTemp = r'Database Connections\SDEPROD_GIS.sde\GIS.CITY_TEMP'
    CityOutlines = r'Database Connections\SDEPROD_GIS.sde\GIS.CITY_LIMITS_LN_1'
    
    DisconnectHarshly_SDEPROD()
    AllowConnections_SDEPROD()
    
    if Exists(CityTemp):
        print "CityTemp exists"
        Delete_management(CityTemp)
    else:
        print "I don't think CityTemp exists."
        pass
    
    # Instead of erase, might try a union, then selection for only the features
    # that do not have their centers within the 2nd feature class,
    # then output the selected features.
    # MakeFeatureLayer, Union, SelectByLocation, CopyFeatures.
    Erase_analysis(taxfile, cityLimitsSub, CityTemp, "0 Feet")
    Append_management(cityLimitsAdd, CityTemp,"NO_TEST","#","#")
    Dissolve_management(CityTemp, KDOTcity,"CITYNUMBER;CITY;COUNTY;DIST;TYPE;POPCENSUS;POPCURRENT;ID1","LOAD_DATE MAX","MULTI_PART","DISSOLVE_LINES")
    FeatureToLine_management(KDOTcity, CityOutlines,"0.01 Feet","ATTRIBUTES")


if __name__ == '__main__':
    try:
        CityLimitsMod()
        print "updated city limits in SDEPROD"
    finally:
        AllowConnections_SDEPROD()

else:
    pass