from connect_to_rds import create_postgres_engine
import sqlalchemy

def generate_table(engine, target_schema:str, target_table:str,mode:str):
    
    schema_query = """
        CREATE SCHEMA IF NOT EXISTS {0};
        GRANT ALL PRIVILEGES ON SCHEMA {0} TO PUBLIC;
    """.format(target_schema)

    drop_table_query = """
        DROP TABLE IF EXISTS {}.{};
    """.format(target_schema, target_table)

    create_table_query = """
        CREATE TABLE IF NOT EXISTS {0}.{1} (
            {2}
        );
        GRANT ALL PRIVILEGES ON {0}.{1} TO PUBLIC;
    """.format(target_schema, target_table, get_table_definition(target_table))

    truncate_table_query = """
        TRUNCATE {}.{};
    """.format(target_schema, target_table)

    engine.execute(schema_query)
    if mode.lower()=='replace':
        engine.execute(drop_table_query)
    if mode.lower()=='truncate':
        engine.execute(truncate_table_query)
    engine.execute(create_table_query)


def get_table_definition(target_table:str):

    data_model_dict = {
        'pulsepoint':"""
        Status_At_Load VARCHAR NULL
        ,Incident_ID VARCHAR NULL
        ,CALL_RECEIVED_DATETIME TIMESTAMP NULL
        ,Latitude NUMERIC NULL
        ,Longitude NUMERIC NULL
        ,FullDisplayAddress VARCHAR NULL
        ,Incident_Type VARCHAR NULL
        ,Unit VARCHAR NULL
        ,Unit_Status_Transport VARCHAR NULL
        """
        ,'vision_zero': """
            OBJECTID VARCHAR NULL
            ,GLOBALID   VARCHAR NULL 
            ,REQUESTID VARCHAR NULL
            ,REQUESTTYPE VARCHAR NULL
            ,REQUESTDATE TIMESTAMP NULL
            ,STATUS VARCHAR NULL
            ,STREETSEGID VARCHAR NULL
            ,COMMENTS VARCHAR NULL
            ,USERTYPE VARCHAR NULL
            ,geometry geometry
            """
        ,'crashes_raw':"""
            OBJECTID VARCHAR NULL
            ,CRIMEID VARCHAR NULL
            ,CCN VARCHAR NULL
            ,REPORTDATE TIMESTAMP NULL
            ,ROUTEID VARCHAR NULL
            ,MEASURE VARCHAR NULL
            ,_OFFSET VARCHAR NULL
            ,STREETSEGID VARCHAR NULL
            ,ROADWAYSEGID VARCHAR NULL
            ,FROMDATE TIMESTAMP NULL
            ,TODATE TIMESTAMP NULL
            ,MARID VARCHAR NULL
            ,ADDRESS VARCHAR NULL
            ,LATITUDE VARCHAR NULL
            ,LONGITUDE VARCHAR NULL
            ,XCOORD VARCHAR NULL
            ,YCOORD VARCHAR NULL
            ,WARD VARCHAR NULL
            ,EVENTID VARCHAR NULL
            ,MAR_ADDRESS VARCHAR NULL
            ,MAR_SCORE VARCHAR NULL
            ,MAJORINJURIES_BICYCLIST INT NULL
            ,MINORINJURIES_BICYCLIST INT NULL
            ,UNKNOWNINJURIES_BICYCLIST INT NULL
            ,FATAL_BICYCLIST INT NULL
            ,MAJORINJURIES_DRIVER INT NULL
            ,MINORINJURIES_DRIVER INT NULL
            ,UNKNOWNINJURIES_DRIVER INT NULL
            ,FATAL_DRIVER INT NULL
            ,MAJORINJURIES_PEDESTRIAN INT NULL
            ,MINORINJURIES_PEDESTRIAN INT NULL
            ,UNKNOWNINJURIES_PEDESTRIAN INT NULL
            ,FATAL_PEDESTRIAN INT NULL
            ,TOTAL_VEHICLES INT NULL
            ,TOTAL_BICYCLES INT NULL
            ,TOTAL_PEDESTRIANS INT NULL
            ,PEDESTRIANSIMPAIRED INT NULL
            ,BICYCLISTSIMPAIRED INT NULL
            ,DRIVERSIMPAIRED INT NULL
            ,TOTAL_TAXIS INT NULL
            ,TOTAL_GOVERNMENT INT NULL
            ,SPEEDING_INVOLVED INT NULL
            ,NEARESTINTROUTEID VARCHAR NULL
            ,NEARESTINTSTREETNAME VARCHAR NULL
            ,OFFINTERSECTION VARCHAR NULL
            ,INTAPPROACHDIRECTION VARCHAR NULL
            ,LOCATIONERROR VARCHAR NULL
            ,LASTUPDATEDATE TIMESTAMP NULL
            ,MPDLATITUDE VARCHAR NULL
            ,MPDLONGITUDE VARCHAR NULL
            ,MPDGEOX VARCHAR NULL
            ,MPDGEOY VARCHAR NULL
            ,BLOCKKEY VARCHAR NULL
            ,SUBBLOCKKEY VARCHAR NULL
            ,FATALPASSENGER INT NULL
            ,MAJORINJURIESPASSENGER INT NULL
            ,MINORINJURIESPASSENGER INT NULL
            ,UNKNOWNINJURIESPASSENGER INT NULL
            ,geometry geometry null
            """
        ,'all311':"""
            OBJECTID VARCHAR NULL
            ,SERVICECODE VARCHAR NULL
            ,SERVICECODEDESCRIPTION VARCHAR NULL
            ,SERVICETYPECODEDESCRIPTION VARCHAR NULL
            ,ORGANIZATIONACRONYM VARCHAR NULL
            ,SERVICECALLCOUNT VARCHAR NULL
            ,ADDDATE VARCHAR NULL
            ,RESOLUTIONDATE TIMESTAMP NULL
            ,SERVICEDUEDATE TIMESTAMP NULL
            ,SERVICEORDERDATE TIMESTAMP NULL
            ,INSPECTIONFLAG VARCHAR NULL
            ,INSPECTIONDATE VARCHAR NULL
            ,INSPECTORNAME VARCHAR NULL
            ,SERVICEORDERSTATUS VARCHAR NULL
            ,STATUS_CODE VARCHAR NULL
            ,SERVICEREQUESTID VARCHAR NULL
            ,PRIORITY VARCHAR NULL
            ,STREETADDRESS VARCHAR NULL
            ,XCOORD VARCHAR NULL
            ,YCOORD VARCHAR NULL
            ,LATITUDE VARCHAR NULL
            ,LONGITUDE VARCHAR NULL
            ,CITY VARCHAR NULL
            ,STATE VARCHAR NULL
            ,ZIPCODE VARCHAR NULL
            ,MARADDRESSREPOSITORYID VARCHAR NULL
            ,WARD VARCHAR NULL
            ,DETAILS VARCHAR NULL
            ,geometry geometry null
        """
        ,'address_points':"""
            OBJECTID_12 VARCHAR NULL
            ,OBJECTID VARCHAR NULL
            ,SITE_ADDRESS_PK VARCHAR NULL
            ,ADDRESS_ID VARCHAR NULL
            ,ROADWAYSEGID VARCHAR NULL
            ,STATUS VARCHAR NULL
            ,SSL VARCHAR NULL
            ,TYPE_ VARCHAR NULL
            ,ENTRANCETYPE VARCHAR NULL
            ,ADDRNUM VARCHAR NULL
            ,ADDRNUMSUFFIX VARCHAR NULL
            ,STNAME VARCHAR NULL
            ,STREET_TYPE VARCHAR NULL
            ,QUADRANT VARCHAR NULL
            ,CITY VARCHAR NULL
            ,STATE VARCHAR NULL
            ,FULLADDRESS VARCHAR NULL
            ,SQUARE VARCHAR NULL
            ,SUFFIX VARCHAR NULL
            ,LOT VARCHAR NULL
            ,NATIONALGRID VARCHAR NULL
            ,ZIPCODE4 VARCHAR NULL
            ,XCOORD VARCHAR NULL
            ,YCOORD VARCHAR NULL
            ,STATUS_ID VARCHAR NULL
            ,METADATA_ID VARCHAR NULL
            ,OBJECTID_1 VARCHAR NULL
            ,ASSESSMENT_NBHD VARCHAR NULL
            ,ASSESSMENT_SUBNBHD VARCHAR NULL
            ,CFSA_NAME VARCHAR NULL
            ,HOTSPOT VARCHAR NULL
            ,CLUSTER_ VARCHAR NULL
            ,POLDIST VARCHAR NULL
            ,ROC VARCHAR NULL
            ,PSA VARCHAR NULL
            ,SMD VARCHAR NULL
            ,CENSUS_TRACT VARCHAR NULL
            ,VOTE_PRCNCT VARCHAR NULL
            ,WARD VARCHAR NULL
            ,ZIPCODE VARCHAR NULL
            ,ANC VARCHAR NULL
            ,NEWCOMMSELECT06 VARCHAR NULL
            ,NEWCOMMCANDIDATE VARCHAR NULL
            ,CENSUS_BLOCK VARCHAR NULL
            ,CENSUS_BLOCKGROUP VARCHAR NULL
            ,FOCUS_IMPROVEMENT_AREA VARCHAR NULL
            ,SE_ANNO_CAD_DATA VARCHAR NULL
            ,LATITUDE VARCHAR NULL
            ,LONGITUDE VARCHAR NULL
            ,ACTIVE_RES_UNIT_COUNT VARCHAR NULL
            ,RES_TYPE VARCHAR NULL
            ,ACTIVE_RES_OCCUPANCY_COUNT VARCHAR NULL
            ,WARD_2002 VARCHAR NULL
            ,WARD_2012 VARCHAR NULL
            ,ANC_2002 VARCHAR NULL
            ,ANC_2012 VARCHAR NULL
            ,SMD_2002 VARCHAR NULL
            ,SMD_2012 VARCHAR NULL
            ,geometry    geometry
"""
,'census_blocks':"""
        OBJECTID VARCHAR NULL
        ,BLKGRP VARCHAR NULL
        ,BLOCK VARCHAR NULL
        ,GEOID VARCHAR NULL
        ,GEOID10 VARCHAR NULL
        ,ALAND10 VARCHAR NULL
        ,AWATER10 VARCHAR NULL
        ,TOTAL_POP INT NULL
        ,TOTAL_POP_ONE_RACE INT NULL
        ,POP_WHITE INT NULL
        ,POP_BLACK INT NULL
        ,POP_NATIVE INT NULL
        ,POP_ASIAN INT NULL
        ,POP_PACIFIC_ISLANDER INT NULL
        ,POP_OTHER_RACE INT NULL
        ,POP_BLACK_OTHER INT NULL
        ,POP_NATIVE_OTHER INT NULL
        ,POP_ASIAN_OTHER INT NULL
        ,POP_PACIFIC_ISLANDER_OTHER INT NULL
        ,POP_HISPANIC INT NULL
        ,POP_WHITE_NON_HISPANIC INT NULL
        ,POP_NON_HISPANIC_BLACK INT NULL
        ,POP_NON_HISPANIC_NATIVE INT NULL
        ,POP_NON_HISPANIC_ASIAN INT NULL
        ,POP_NON_HISPANIC_PACIFIC_ISLANDER INT NULL
        ,POP_NON_HISPANIC_OTHER INT NULL
        ,POP_NON_HISPANIC_BLACK_OTHER INT NULL
        ,POP_NON_HISPANIC_NATIVE_OTHER INT NULL
        ,POP_NON_HISPANIC_ASIAN_OTHER INT NULL
        ,POP_NON_HISPANIC_PACIFIC_ISLANDER_OTHER INT NULL
        ,ADULT_TOTAL_POP INT NULL
        ,ADULT_POP_WHITE INT NULL
        ,ADULT_POP_BLACK INT NULL
        ,ADULT_POP_NATIVE INT NULL
        ,ADULT_POP_ASIAN INT NULL
        ,ADULT_POP_PACIFIC_ISLANDER INT NULL
        ,ADULT_POP_OTHER_RACE INT NULL
        ,ADULT_POP_BLACK_OTHER INT NULL
        ,ADULT_POP_NATIVE_OTHER INT NULL
        ,ADULT_POP_ASIAN_OTHER INT NULL
        ,ADULT_POP_PACIFIC_ISLANDER_OTHER INT NULL
        ,ADULT_POP_HISPANIC INT NULL
        ,ADULT_POP_WHITE_NON_HISPANIC INT NULL
        ,ADULT_POP_NON_HISPANIC_BLACK INT NULL
        ,ADULT_POP_NON_HISPANIC_NATIVE INT NULL
        ,ADULT_POP_NON_HISPANIC_ASIAN INT NULL
        ,ADULT_POP_NON_HISPANIC_PACIFIC_ISLANDER INT NULL
        ,ADULT_POP_NON_HISPANIC_OTHER INT NULL
        ,ADULT_POP_NON_HISPANIC_BLACK_OTHER INT NULL
        ,ADULT_POP_NON_HISPANIC_NATIVE_OTHER INT NULL
        ,ADULT_POP_NON_HISPANIC_ASIAN_OTHER INT NULL
        ,ADULT_POP_NON_HISPANIC_PACIFIC_ISLANDER_OTHER INT NULL
        ,TOTAL_HOUSING_UNITS INT NULL
        ,TOTAL_OCCUPIED_HOUSING_UNITS INT NULL
        ,TOTAL_VACANT_HOUSING_UNITS INT NULL
        ,ACRES VARCHAR NULL
        ,Shape_Length VARCHAR NULL
        ,Shape_Area VARCHAR NULL
        ,SQMILES VARCHAR NULL
        ,geometry geometry
"""
,'crash_details':"""
    OBJECTID VARCHAR NULL
    ,CRIMEID VARCHAR NULL
    ,CCN VARCHAR NULL
    ,PERSONID VARCHAR NULL
    ,PERSONTYPE VARCHAR NULL
    ,AGE NUMERIC NULL
    ,FATAL VARCHAR NULL
    ,MAJORINJURY VARCHAR NULL
    ,MINORINJURY VARCHAR NULL
    ,VEHICLEID VARCHAR NULL
    ,INVEHICLETYPE VARCHAR NULL
    ,TICKETISSUED VARCHAR NULL
    ,LICENSEPLATESTATE VARCHAR NULL
    ,IMPAIRED VARCHAR NULL
    ,SPEEDING VARCHAR NULL
    ,geometry geometry

"""
,'roadway_blocks':"""
    OBJECTID VARCHAR NULL
    ,ROUTEID VARCHAR NULL
    ,FROMMEASURE NUMERIC NULL
    ,TOMEASURE NUMERIC NULL
    ,ROUTENAME VARCHAR NULL
    ,ROADTYPE VARCHAR NULL
    ,BLOCKKEY VARCHAR NULL
    ,TOTALTRAVELLANES NUMERIC NULL
    ,TOTALPARKINGLANES NUMERIC NULL
    ,TOTALRAISEDBUFFERS NUMERIC NULL
    ,TOTALTRAVELLANEWIDTH NUMERIC NULL
    ,TOTALCROSSSECTIONWIDTH NUMERIC NULL
    ,TOTALPARKINGLANEWIDTH NUMERIC NULL
    ,TOTALRAISEDBUFFERWIDTH NUMERIC NULL
    ,TOTALTRAVELLANESINBOUND NUMERIC NULL
    ,TOTALTRAVELLANESOUTBOUND NUMERIC NULL
    ,TOTALTRAVELLANESBIDIRECTIONAL NUMERIC NULL
    ,TOTALTRAVELLANESREVERSIBLE NUMERIC NULL
    ,SUMMARYDIRECTION VARCHAR NULL
    ,BIKELANE_PARKINGLANE_ADJACENT VARCHAR NULL
    ,BIKELANE_THROUGHLANE_ADJACENT VARCHAR NULL
    ,BIKELANE_POCKETLANE_ADJACENT VARCHAR NULL
    ,BIKELANE_CONTRAFLOW VARCHAR NULL
    ,BIKELANE_CONVENTIONAL VARCHAR NULL
    ,BIKELANE_DUAL_PROTECTED VARCHAR NULL
    ,BIEKLANE_DUAL_BUFFERED VARCHAR NULL
    ,BIKELANE_PROTECTED VARCHAR NULL
    ,BIKELANE_BUFFERED VARCHAR NULL
    ,RIGHTTURN_EXCLUSIVE VARCHAR NULL
    ,LEFTTURN_EXCLUSIVE VARCHAR NULL
    ,DOUBLEYELLOW_LINE VARCHAR NULL
    ,SECTIONFLAGS VARCHAR NULL
    ,LOC_ERROR VARCHAR NULL
    ,MIDMEASURE NUMERIC NULL
    ,AADT NUMERIC NULL
    ,AADT_YEAR NUMERIC NULL
    ,FHWAFUNCTIONALCLASS NUMERIC NULL
    ,HPMSID VARCHAR NULL
    ,HPMSSECTIONTYPE NUMERIC NULL
    ,ID VARCHAR NULL
    ,IRI NUMERIC NULL
    ,IRI_DATE TIMESTAMP NULL
    ,NHSCODE NUMERIC NULL
    ,OWNERSHIP VARCHAR NULL
    ,PCI_CONDCATEGORY VARCHAR NULL
    ,PCI_LASTINSPECTED TIMESTAMP NULL
    ,PCI_SCORE NUMERIC NULL
    ,QUADRANT VARCHAR NULL
    ,SIDEWALK_IB_PAVTYPE VARCHAR NULL
    ,SIDEWALK_IB_WIDTH VARCHAR NULL
    ,SIDEWALK_OB_PAVTYPE VARCHAR NULL
    ,SIDEWALK_OB_WIDTH VARCHAR NULL
    ,SPEEDLIMITS_IB NUMERIC NULL
    ,SPEEDLIMITS_IB_ALT VARCHAR NULL
    ,SPEEDLIMITS_OB NUMERIC NULL
    ,SPEEDLIMITS_OB_ALT VARCHAR NULL
    ,STREETNAME VARCHAR NULL
    ,STREETTYPE VARCHAR NULL
    ,BLOCK_NAME VARCHAR NULL
    ,ADDRESS_RANGE_HIGH NUMERIC NULL
    ,ADDRESS_RANGE_LOW NUMERIC NULL
    ,ADDRESS_RANGE_RIGHT_HIGH NUMERIC NULL
    ,ADDRESS_RANGE_LEFT_HIGH NUMERIC NULL
    ,ADDRESS_RANGE_RIGHT_LOW NUMERIC NULL
    ,MAR_ID NUMERIC NULL
    ,ADDRESS_RANGE_LEFT_LOW NUMERIC NULL
    ,BLOCKID VARCHAR NULL
    ,DCFUNCTIONALCLASS NUMERIC NULL
    ,NHSTYPE VARCHAR NULL
    ,SNOWROUTE_DDOT VARCHAR NULL
    ,SNOWROUTE_DPW VARCHAR NULL
    ,SNOWSECTION_DDOT VARCHAR NULL
    ,SNOWZONE_DDOT VARCHAR NULL
    ,SNOWZONE_DPW VARCHAR NULL
    ,LEFTTURN_CURBLANE_EXCL VARCHAR NULL
    ,LEFTTURN_CURBLANE_EXCL_LEN NUMERIC NULL
    ,RIGHTTURN_CURBLANE_EXCL VARCHAR NULL
    ,RIGHTTURN_CURBLANE_EXCL_LEN NUMERIC NULL
    ,TOTALBIKELANES NUMERIC NULL
    ,TOTALBIKELANEWIDTH NUMERIC NULL
    ,RPPDIRECTION VARCHAR NULL
    ,RPPSIDE VARCHAR NULL
    ,SLOWSTREETINFO VARCHAR NULL
    ,SHAPELEN NUMERIC NULL
    ,SHAPE VARCHAR NULL
    ,geometry geometry
"""
,'roadway_subblocks':"""
    OBJECTID VARCHAR NULL
    ,ROUTEID VARCHAR NULL
    ,FROMMEASURE NUMERIC NULL
    ,TOMEASURE NUMERIC NULL
    ,ROUTENAME VARCHAR NULL
    ,ROADTYPE VARCHAR NULL
    ,SUBBLOCKKEY VARCHAR NULL
    ,TOTALTRAVELLANES NUMERIC NULL
    ,TOTALPARKINGLANES NUMERIC NULL
    ,TOTALRAISEDBUFFERS NUMERIC NULL
    ,TOTALTRAVELLANEWIDTH NUMERIC NULL
    ,TOTALCROSSSECTIONWIDTH NUMERIC NULL
    ,TOTALPARKINGLANEWIDTH NUMERIC NULL
    ,TOTALTRAVELLANESINBOUND NUMERIC NULL
    ,TOTALTRAVELLANESOUTBOUND NUMERIC NULL
    ,TOTALTRAVELLANESBIDIRECTIONAL NUMERIC NULL
    ,TOTALTRAVELLANESREVERSIBLE NUMERIC NULL
    ,SUMMARYDIRECTION VARCHAR NULL
    ,BIKELANE_PARKINGLANE_ADJACENT VARCHAR NULL
    ,BIKELANE_THROUGHLANE_ADJACENT VARCHAR NULL
    ,BIKELANE_POCKETLANE_ADJACENT VARCHAR NULL
    ,BIKELANE_CONTRAFLOW VARCHAR NULL
    ,BIKELANE_CONVENTIONAL VARCHAR NULL
    ,BIKELANE_DUAL_PROTECTED VARCHAR NULL
    ,BIKELANE_DUAL_BUFFERED VARCHAR NULL
    ,BIKELANE_PROTECTED VARCHAR NULL
    ,BIKELANE_BUFFERED VARCHAR NULL
    ,RIGHTTURN_EXCLUSIVE VARCHAR NULL
    ,LEFTTURN_EXCLUSIVE VARCHAR NULL
    ,DOUBLEYELLOW_LINE VARCHAR NULL
    ,SECTIONFLAGS VARCHAR NULL
    ,LOC_ERROR VARCHAR NULL
    ,MIDMEASURE NUMERIC NULL
    ,AADT NUMERIC NULL
    ,FHWAFUNCTIONALCLASS NUMERIC NULL
    ,HPMSID VARCHAR NULL
    ,HPMSSECTIONTYPE NUMERIC NULL
    ,ID VARCHAR NULL
    ,IRI NUMERIC NULL
    ,IRI_DATE TIMESTAMP NULL
    ,NHSCODE NUMERIC NULL
    ,OWNERSHIP VARCHAR NULL
    ,PCI_CONDCATEGORY VARCHAR NULL
    ,PCI_LASTINSPECTED TIMESTAMP NULL
    ,PCI_SCORE VARCHAR NULL
    ,SIDEWALK_IB_PAVTYPE VARCHAR NULL
    ,SIDEWALK_IB_WIDTH VARCHAR NULL
    ,SIDEWALK_OB_PAVTYPE VARCHAR NULL
    ,SIDEWALK_OB_WIDTH VARCHAR NULL
    ,SPEEDLIMITS_IB NUMERIC NULL
    ,SPEEDLIMITS_IB_ALT VARCHAR NULL
    ,SPEEDLIMITS_OB NUMERIC NULL
    ,SPEEDLIMITS_OB_ALT VARCHAR NULL
    ,SUBBLOCKID VARCHAR NULL
    ,BLOCKID VARCHAR NULL
    ,BLOCKKEY VARCHAR NULL
    ,DCFUNCTIONALCLASS NUMERIC NULL
    ,NHSTYPE VARCHAR NULL
    ,QUADRANT NUMERIC NULL
    ,STREETNAME VARCHAR NULL
    ,STREETTYPE VARCHAR NULL
    ,SNOWROUTE_DPW VARCHAR NULL
    ,SNOWZONE_DPW VARCHAR NULL
    ,SNOWROUTE VARCHAR NULL
    ,SNOWSECTION VARCHAR NULL
    ,SNOWZONE VARCHAR NULL
    ,LEFTTURN_CURBLANE_EXCL VARCHAR NULL
    ,LEFTTURN_CURBLANE_EXCL_LEN NUMERIC NULL
    ,RIGHTTURN_CURBLANE_EXCL VARCHAR NULL
    ,RIGHTTURN_CURBLANE_EXCL_LEN NUMERIC NULL
    ,TOTALBIKELANES NUMERIC NULL
    ,TOTALBIKELANEWIDTH NUMERIC NULL
    ,RPPDIRECTION VARCHAR NULL
    ,RPPSIDE VARCHAR NULL
    ,SLOWSTREETINFO VARCHAR NULL
    ,SHAPELEN NUMERIC NULL
    ,TOTALRAISEDBUFFERWIDTH VARCHAR NULL
    ,AADT_YEAR NUMERIC NULL
    ,geometry geometry
"""
,'roadway_blockface':"""
    OBJECTID VARCHAR NUll
    ,ROUTEID VARCHAR NUll
    ,SIDE VARCHAR NUll
    ,MEAS_FROM NUMERIC NULL
    ,MEAS_TO NUMERIC NULL
    ,BLOCKFACEKEY VARCHAR NUll
    ,_OFFSET NUMERIC NULL
    ,SHAPELEN NUMERIC NULL
    ,SHAPE geometry
    ,geometry geometry
    """
,'roadway_intersection_approach':"""
    OBJECTID VARCHAR NUll
    ,ROUTEID VARCHAR NUll
    ,FROMMEASURE NUMERIC NULL
    ,TOMEASURE NUMERIC NULL
    ,ROUTENAME VARCHAR NUll
    ,ROADTYPE VARCHAR NUll
    ,APPROACHID VARCHAR NUll
    ,TOTALTRAVELLANES NUMERIC NULL
    ,TOTALPARKINGLANES NUMERIC NULL
    ,TOTALRAISEDBUFFERS NUMERIC NULL
    ,TOTALTRAVELLANEWIDTH NUMERIC NULL
    ,TOTALCROSSSECTIONWIDTH NUMERIC NULL
    ,TOTALPARKINGLANEWIDTH NUMERIC NULL
    ,TOTALRAISEDBUFFERWIDTH NUMERIC NULL
    ,TOTALTRAVELLANESINBOUND NUMERIC NULL
    ,TOTALTRAVELLANESOUTBOUND NUMERIC NULL
    ,TOTALTRAVELLANESBIDIRECTIONAL NUMERIC NULL
    ,TOTALTRAVELLANESREVERSIBLE NUMERIC NULL
    ,SUMMARYDIRECTION VARCHAR NUll
    ,BIKELANE_PARKINGLANE_ADJACENT VARCHAR NUll
    ,BIKELANE_THROUGHLANE_ADJACENT VARCHAR NUll
    ,BIKELANE_POCKETLANE_ADJACENT VARCHAR NUll
    ,BIKELANE_CONTRAFLOW VARCHAR NUll
    ,BIKELANE_CONVENTIONAL VARCHAR NUll
    ,BIKELANE_DUAL_PROTECTED VARCHAR NUll
    ,BIKELANE_DUAL_BUFFERED VARCHAR NUll
    ,BIKELANE_PROTECTED VARCHAR NUll
    ,BIKELANE_BUFFERED VARCHAR NUll
    ,RIGHTTURN_EXCLUSIVE VARCHAR NUll
    ,LEFTTURN_EXCLUSIVE VARCHAR NUll
    ,DOUBLEYELLOW_LINE VARCHAR NUll
    ,SECTIONFLAGS VARCHAR NUll
    ,LOC_ERROR VARCHAR NUll
    ,MIDMEASURE NUMERIC NULL
    ,INTERSECTIONID VARCHAR NUll
    ,AADT NUMERIC NULL
    ,AADT_YEAR NUMERIC NULL
    ,APPROACH_CARD_DIRECTION VARCHAR NUll
    ,APPROACH_INT_DIRECTION VARCHAR NUll
    ,APPROACH_LEG_ANGLE VARCHAR NUll
    ,FHWAFUNCTIONALCLASS VARCHAR NUll
    ,HMPSID VARCHAR NUll
    ,HPMSSECTIONTYPE VARCHAR NUll
    ,ID VARCHAR NUll
    ,IRI VARCHAR NUll
    ,IRI_DATE TIMESTAMP NULL
    ,NHSCODE VARCHAR NUll
    ,OWNERSHIP VARCHAR NUll
    ,PCI_CONDCATEGORY VARCHAR NUll
    ,PCI_LASTINSPECTED TIMESTAMP NULL
    ,PCI_SCORE NUMERIC NULL
    ,QUADRANT NUMERIC NULL
    ,SIDEWALK_IB_PAVTYPE VARCHAR NUll
    ,SIDEWALK_IB_WIDTH VARCHAR NULL
    ,SIDEWALK_OB_PAVTYPE VARCHAR NUll
    ,SIDEWALK_OB_WIDTH  VARCHAR NULL
    ,SPEEDLIMITS_IB NUMERIC NULL
    ,SPEEDLIMITS_IB_ALT VARCHAR NUll
    ,SPEEDLIMITS_OB NUMERIC NULL
    ,SPEEDLIMITS_OB_ALT VARCHAR NUll
    ,STREETNAME VARCHAR NUll
    ,STREETTYPE VARCHAR NUll
    ,SUBBLOCKID VARCHAR NUll
    ,BLOCKID VARCHAR NUll
    ,BLOCKKEY VARCHAR NUll
    ,DCFUNCTIONALCLASS VARCHAR NUll
    ,NHSTYPE VARCHAR NUll
    ,SUBBLOCKKEY VARCHAR NUll
    ,ANGLE VARCHAR NUll
    ,DIRECTIONALITY VARCHAR NUll
    ,INTERSECTIONDIRECTION VARCHAR NUll
    ,SNOWROUTE_DPW VARCHAR NUll
    ,SNOWZONE_DPW VARCHAR NUll
    ,SNOWROUTE VARCHAR NUll
    ,SNOWSECTION VARCHAR NUll
    ,SNOWZONE VARCHAR NUll
    ,LEFTTURN_CURBLANE_EXCL VARCHAR NUll
    ,LEFTTURN_CURBLANE_EXCL_LEN NUMERIC NULL
    ,RIGHTTURN_CURBLANE_EXCL VARCHAR NUll
    ,RIGHTTURN_CURBLANE_EXCL_LEN NUMERIC NULL
    ,TOTALBIKELANES NUMERIC NULL
    ,TOTALBIKELANEWIDTH NUMERIC NULL
    ,RPPDIRECTION VARCHAR NUll
    ,RPPSIDE VARCHAR NUll
    ,SLOWSTREETINFO VARCHAR NUll
    ,GLOBALID VARCHAR NUll
    ,SHAPELEN  NUMERIC NULL
    ,SHAPE geometry
    ,geometry geometry
    """


    }
    return data_model_dict[target_table]
