import labelData as labelData
import plotData as plotData
import processRaw as processRaw
from state_tracker import *
import randomForest as randomForest
import processFeature as processFeature
import knn as knn
 

# GLOBAL VARIABLES
TM_RAW_SENSOR_COLS = ["timestamp", "sensorID", "sensorValue", "message"]
TM_FEATURE_COLS = ["startTime", "endTime", "bathCount", "bathTimeMax", "bathTimeAvg"]
LABELED_FEATURE_COLS = ["startTime", "endTime", "bathCount", "bathTimeMax", "bathTimeAvg", "Date", "UTILabel"]

rawFileName = "./tm003.2018.txt"
sampleDuration = 1 # one day
featureFileName = "feature.csv"
labeledFeatureFileName = 'feature_label.csv'
groundTruthFileName = 'GroundTruth - Sheet1.csv'

feature_col_to_use = LABELED_FEATURE_COLS
feature_col_to_use.remove("startTime")
feature_col_to_use.remove("endTime")
feature_col_to_use.remove("Date")





#print(feature_col_to_use)
feature_df = processFeature.get_feature_df(labeledFeatureFileName)
#randomForest.train_random_forest(feature_df, feature_col_to_use)
knn.train_knn(feature_df, feature_col_to_use)


#plotData.plot_feature_file(featureFileName)

# labelData.label_feature_file_with_groudtruth(featureFileName = featureFileName, groundTruthFileName = groundTruthFileName, outputFileName = labeledFeatureFileName, featureCols = TM_FEATURE_COLS,labeledFeatureCols = LABELED_FEATURE_COLS)




# sampleData = processRaw.get_raw_df(rawFileName = rawFileName, rawDataCols = TM_RAW_SENSOR_COLS, startDate='2018-01-07', endDate = '2018-01-11')
#plotData.plot_bed_motion_data(input_df = sampleData)

# plotData.plot_bed_motion_light_data(input_df = sampleData)
#plotData.plot_light_data(input_df = sampleData)
