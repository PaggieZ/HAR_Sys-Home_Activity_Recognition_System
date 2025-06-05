
# import labelData as labelData
import plotData as plotData
import processRaw as processRaw
import processAL
from state_tracker import *
import labelData as labelData
import processFeature as processFeature
import randomForest as randomForest


# GLOBAL VARIABLES
# column names of raw sensor data
# use \t as seperator
TM_RAW_SENSOR_COLS = ["timestamp", "sensorID", "sensorValue", "message"]
# column names of AL model output
# use \t as seperator
# note for all AL model out, must first run through a script to change seperators from ' ' to '/t'
TM_AL_SENSOR_COLS = ['timestamp', 'sensorID', 'newSensorID', 'sensorValue', 'activity' ]

# column names of labeled feature file when only had 3 features
#LABELED_FEATURE_COLS = ["startTime", "endTime", "bathCount", "bathTimeMax", "bathTimeAvg", "UTILabel"]

# column names of feature file with 19 features
# startTime, endTime, day_night_max_duration, day_night_avg_duration, day_max_duration, day_avg_duration, night_max_duration, night_avg_duration, day_trip_count, night_trip_count, all_trip_count, Motion-Toilet, Motion-Sink, Motion-Area, Light-Toilet, Light-Sink, Light-Area, Wake-Up-Hr,Wake-Up-Minute,Sleep-Hr,Sleep-Minute
TM_FEATURE_COLS = ["startTime", "endTime",  
                    "day_night_max_duration", "day_night_avg_duration", 
                    "day_max_duration", "day_avg_duration",   
                    "night_max_duration", "night_avg_duration",  
                    "day_trip_count", "night_trip_count", "all_trip_count", 
                    "Motion-Toilet", "Motion-Sink",  "Motion-Area",  
                    "Light-Toilet", "Light-Sink",  "Light-Area", "Wake-Up-Hr", "Wake-Up-Minute", "Sleep-Hr", "Sleep-Minute"]  

#startTime,endTime,day_night_max_duration,day_night_avg_duration,day_max_duration,day_avg_duration,night_max_duration,night_avg_duration,day_trip_count,night_trip_count,all_trip_count,Motion-Toilet,Motion-Sink,Motion-Area,Wake-Up-Hr,Wake-Up-Minute,Sleep-Hr,Sleep-Minute,Date,UTILabel
TM_AL_FEATURE_COLS = ["startTime", "endTime",  
                    "day_night_max_duration", "day_night_avg_duration", 
                    "day_max_duration", "day_avg_duration",   
                    "night_max_duration", "night_avg_duration",  
                    "day_trip_count", "night_trip_count", "all_trip_count", 
                    "Motion-Toilet", "Motion-Sink",  "Motion-Area", "Wake-Up-Hr", "Wake-Up-Minute", "Sleep-Hr", "Sleep-Minute"]  

# must include UTILabel
AL_TRAIN_COLS = ["day_night_max_duration", "day_night_avg_duration", 
                    "day_max_duration", "day_avg_duration",   
                    "night_max_duration", "night_avg_duration",  
                    "day_trip_count", "night_trip_count", "all_trip_count", 
                    "Motion-Toilet", "Motion-Sink",  "Motion-Area", "Wake-Up-Hr", "Sleep-Hr", "UTILabel"]

TM_TRAIN_COLS = ["day_night_max_duration", "day_night_avg_duration", 
                    "day_max_duration", "day_avg_duration",   
                    "night_max_duration", "night_avg_duration",  
                    "day_trip_count", "night_trip_count", "all_trip_count", 
                    "Motion-Toilet", "Motion-Sink",  "Motion-Area",  
                    "Light-Toilet", "Light-Sink",  "Light-Area", "Wake-Up-Hr", "Sleep-Hr", "UTILabel"]

sampleDuration = 1 # analyze the raw sensor day by 1 day

############# COMMENT OUT ONE OR THE OTHER #############################

## process raw data, extract features, and store in a feature file
# If extracting features from raw data: 
# rawFileName = "./tm013.20190501-20200501_20250127.060846.txt"
# featureFileName = "feature_tm013_21_dynamic_ws.csv"
# processRaw.extract_features(rawFileName = rawFileName, sampleDuration = sampleDuration, featureFileName = featureFileName, rawDataCols = TM_RAW_SENSOR_COLS, featureDataCols = TM_FEATURE_COLS)

# If extracing features from data annotated by Dr.Cook's AL model: 
rawFileName = "./tm003_AL_reformatted 201709.txt"
#featureFileName = "features_tm003_18_AL_1hrsleep.csv"
featureFileName = "feature_tm003_21_dynamic_ws_updated-2025-02-23 copy.csv"
# processAL.extract_features(rawFileName= rawFileName, sampleDuration = sampleDuration, featureFileName = featureFileName, rawDataCols = TM_AL_SENSOR_COLS, featureDataCols= TM_AL_FEATURE_COLS, startDate="2017-09-01", endDate="2018-09-01")

## label the extracted features
groundTruthFileName = "./GroundTruth - Sheet1.csv"
#labeledFeatureFileName = "labeled_feature_AL_20170901 copy.csv"
labeledFeatureFileName = "labeled_feature_Team_20170901.csv"
#labelData.label_feature_file_with_groudtruth(featureFileName, groundTruthFileName, labeledFeatureFileName)

## run random forest model
feature_df = processFeature.get_feature_df(labeledFeatureFileName)
feature_df.replace([None, ""], 0, inplace=True)
#feature_df.head(10).to_csv('output.csv', mode = 'w')

randomForest.train_random_forest(feature_df, TM_TRAIN_COLS)


