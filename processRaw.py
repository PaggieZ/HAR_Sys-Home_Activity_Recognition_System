from datetime import datetime, timedelta
import pandas as pd 
import matplotlib.pyplot as plt
from state_tracker import *
import plotData as plotData
from sensor_data_preprocessor import *


def extract_features(rawFileName, sampleDuration, featureFileName, rawDataCols, featureDataCols, startDate = None, endDate = None):
    '''
    Input: 
    1. rawFileName: file name of raw sensor data txt
    2. sampleDuration: window duration (number of days)
    3. featureFileName: file name of output csv/excel file
    4. startDate: start date of data ('YYYY-MM-DD'), is None when not specified
    5. endDate: end date of data ('YYYY-MM-DD'), is None when not specified

    Output file column:
    1. "startTime" of the sample point 
    2. "endTime" of the sample point
    3. "day_night_max_duration": longest bathroom visit in day+night combined 
    4. "day_night_avg_duration": avg bathroom visit in day+night combined 
    5. "day_max_duration": longest bathroom visit during daytime 
    6. "day_avg_duration": avg bathroom visit during daytime 
    7. "night_max_duration": longest bathroom visit during nighttime
    8. "night_avg_duration": avg bathroom visit during nighttime 
    9. "day_trip_count": number of daytime bathroom trips (filtered)
    10. "night_trip_count": number of nighttime bathroom trisp (filtered)
    11. "all_trip_count": total number of trips in the day 
    12. "Motion-Toilet": number of times the toilet motion sensor is activated 
    13. "Motion-Sink": number of times the bathroom sink motion sensor is activated 
    14. "Motion-Area": number of times the bathroom area motion sensor is activated
    15. "Light-Toilet": number of times the toilet light sensor fluctuates during the bathroom trip 
    16. "Light-Sink": number of times the bathroom sink light sensor fluctuates during the bathroom trip 
    17. "Light-Area": number of times the bathroom area light sensor fluctuates during the bathroom trip 

    The extract_features() function will take in the raw sensor data, seperate the raw
    sensor data based on the "sampleDuration", then calculate all the outputs and store the results in the 
    store the results in the "feature file".
    '''''''''

    ## open and read raw data file
    with open(rawFileName, "r") as f:
        rawContent = f.read()

    ## loop through the raw content, seperate sensor data by sampleDuration, calculate features, populate feature file
    # need to skip the first four lines of data, related to Zigbee
    sampleData = pd.DataFrame(columns = rawDataCols) # a data frame, stores lines of sensor data within a sample period
     
    isNewSamplePeriod = True # true when the curr line has the first sensor data for a sample period 
    startTime = 0 # start time of a sample period
    lineNum = 0 
    prevTime=None
    for line in rawContent.splitlines():
        lineNum += 1
        if lineNum <= 4:
            continue
        currLineTime = get_time_from_line(line)

        # initialize variables at the start of new sample period
        if isNewSamplePeriod:
            startTime = currLineTime
            sampleData = pd.DataFrame(columns = rawDataCols)
            isNewSamplePeriod = False
        
        if startDate is not None and is_before_startDate(currLineTime, startDate): # skip lines before startDate
            isNewSamplePeriod = True
            print(currLineTime)
            continue  
        elif endDate is not None and is_after_endDate(currLineTime, endDate): # exit for loop if line is after endDate
            break
        
        
        # update isNewSamplePeriod
        isNewSamplePeriod = get_isNewSamplePeriod(currLineTime, startTime, sampleDuration)

        ## get all sensor data for the current sample period
        if not isNewSamplePeriod: # if at the begining or the middle of the sample period
            # append one row to the sampleData dataframe
            newRawRow = get_newRow_from_line(line) # returns a data frame
            sampleData = pd.concat([sampleData, newRawRow], ignore_index = True)
            prevTime = currLineTime
            
        else: # if at the end of the sample period

            # plotData.plot_raw_data(sampleData)
            
            endTime = prevTime
            newFeatureRow = get_feature_row(sampleData, startTime, endTime) # returns a data frame
            if newFeatureRow is None:
                continue
            newFeatureRow.to_csv(featureFileName, mode =  'a', index = False, header = False)
            

def get_newRow_from_line(line):
    '''
    convert a single line from raw sensor data into a data frame
    '''
    cols = line.split('\t')
    timestamp = get_time_from_line(line)
    sensorID = [cols[1]]
    sensorValue = [cols[2]]
    message = [cols[3]]
    newRow = pd.DataFrame({"timestamp": timestamp, "sensorID": sensorID, "sensorValue": sensorValue, "message": message})
    return newRow

def get_feature_row(sampleData, startTime, endTime):
    '''
    compute and store values in the feature file
    '''
    features_dict = {
        'startTime': startTime, 
        'endTime': endTime, 
    }

    # calculate feature values
    stats_dict, durations_dict = count_bath_features(sampleData)
    
    if stats_dict is None or durations_dict is None:
        return None

    features_dict.update(stats_dict)

    # nightActivityCount = find_nightActivityCount(sampleData)
    # newRow = pd.DataFrame({"startTime": startTime, "endTime": endTime, "bathCount": bathCount, "bathTimeMax": bathTimeMax, "bathTimeAvg": bathTimeAvg, "nightActivityCount": nightActivityCount})
    newRow = pd.DataFrame([features_dict])

    return newRow

def get_isNewSamplePeriod(currLineTime, startTime, sampleDuration):
    # currLineTime and startTime are datetime objects

    delta = timedelta(days=sampleDuration)
    
    endTime = datetime(startTime.year, startTime.month, startTime.day) + delta
    if currLineTime < endTime:
        return False
    else:
        return True

def is_before_startDate(currLineTime, startDate):
    '''
    return True/False
    '''''''''
    startDatetime = datetime(int(startDate.split('-')[0]), int(startDate.split('-')[1]), int(startDate.split('-')[2]))
    if currLineTime < startDatetime:
        return True
    else:
        return False
   
def is_after_endDate(currLineTime, endDate):
    '''
    return True/False
    '''''''''
    endDatetime = datetime(int(endDate.split('-')[0]), int(endDate.split('-')[1]), int(endDate.split('-')[2]))
    if currLineTime > endDatetime:
        return True
    else:
        return False      

def get_time_from_line(line): 
    '''
    Parses line for timestamp
    '''''''''    
    timestamp = line.split('\t')[0]
    try:
        return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
    except:
        return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

    

    

def count_bath_features(sampleData, threshold_min=1, max_temp=37, threshold_light=5):

    '''
    input  -- data frame consisting of sample data within the sample period
           -- threshold: minimum number of minutes to be considered a bathroom trip (helps combat noise)
           -- max_temp: lowest temperature at which toilet trips are considered shower trips (Celsius) 
    output --  "day_night_max_duration": longest bathroom visit in day+night combined 
           -- "day_night_avg_duration": avg bathroom visit in day+night combined 
           -- "day_max_duration": longest bathroom visit during daytime 
           -- "day_avg_duration": avg bathroom visit during daytime 
           -- "night_max_duration": longest bathroom visit during nighttime
           -- "night_avg_duration": avg bathroom visit during nighttime 
           -- "day_trip_count": number of daytime bathroom trips (filtered)
           -- "night_trip_count": number of nighttime bathroom trisp (filtered)
           -- "all_trip_count": total number of trips in the day 
           -- "Motion-Toilet": number of times the toilet motion sensor is activated 
           -- "Motion-Sink": number of times the bathroom sink motion sensor is activated 
           -- "Motion-Area": number of times the bathroom area motion sensor is activated
           -- "Light-Toilet": number of times the toilet light sensor fluctuates during the bathroom trip 
           -- "Light-Sink": number of times the bathroom sink light sensor fluctuates during the bathroom trip 
           -- "Light-Area": number of times the bathroom area light sensor fluctuates during the bathroom trip 
    '''''''''

    #preprocessor = sensor_data_preprocessor(sampleData)
    #resampled_df = preprocessor.resample_motion(sensor_location="BathroomAArea")
    #filtered_df = preprocessor.apply_filters_motion(resampled_df, "sensorValue")
    #preprocessor.visualize_filters_motion(filtered_df, "sensorValue")     
   
    # Apply filter, calculate area, and determine night and sleep time
    preprocessor = sensor_data_preprocessor(sampleData)
    resampled_df = preprocessor.resample_light(sensor_location="BedroomAArea")
    if resampled_df is None:
        wakeTime_hr = 7 
        wakeTime_min = 0
        sleepTime_hr = 21
        sleepTime_min = 0
    else:
        filtered_df = preprocessor.apply_filters_light(resampled_df, "sensorValue")
        peak_df = preprocessor.get_AUC(filtered_df, "sensorValue_rolling_mean")
        wakeTime = preprocessor.get_wakeTime(peak_df)
        sleepTime = preprocessor.get_sleepTime(peak_df)
        try:
            sleepTime_hr = int(sleepTime.hour)
            sleepTime_min = int(sleepTime.minute)
        except Exception as e:
            sleepTime_hr = 21
            sleepTime_min = 0                
        
        try:
            wakeTime_hr = int(wakeTime.hour)
            wakeTime_min = int(wakeTime.minute)
        except Exception as e:
            wakeTime_hr = 7
            wakeTime_min = 0


    # Apply rolling max filter to bathroom toilet motion sensor data
    resampled_df = preprocessor.resample_motion(sensor_location='BathroomAToilet')
    if resampled_df is None: 
        return None, None
    filtered_df = preprocessor.apply_filters_motion(resampled_df, "sensorValue")
    
    # Count bathroom trips and durations 
    Bathroom_State_Tracker = BathroomStateTracker(IDLE, nighttime_hr=sleepTime_hr, nighttime_min=sleepTime_min, 
                                                    daytime_hr=wakeTime_hr, daytime_min=wakeTime_min)    
    for i in range (0, filtered_df.shape[0]):
        Bathroom_State_Tracker.input(filtered_df.loc[i])


    trip_stats_dict, trip_times_dict = Bathroom_State_Tracker.get_trip_stats()
    
    # Determine bathroom sensor activation counts 
    motion_toilet_count = len(sampleData[(sampleData['sensorID'].str.contains('Bathroom')) & 
                                         (sampleData['sensorID'].str.contains('Toilet')) &
                                         (sampleData['message'].str.contains('Motion')) &
                                         (sampleData['sensorValue'] == 'ON')])

    light_toilet_count = len(sampleData[(sampleData['sensorID'].str.contains('Bathroom')) & 
                                         (sampleData['sensorID'].str.contains('Toilet')) &
                                         (sampleData['message'].str.contains('Light'))])

    motion_sink_count = len(sampleData[(sampleData['sensorID'].str.contains('Bathroom')) & 
                                         (sampleData['sensorID'].str.contains('Sink')) &
                                         (sampleData['message'].str.contains('Motion')) &
                                         (sampleData['sensorValue'] == 'ON')])

    light_sink_count = len(sampleData[(sampleData['sensorID'].str.contains('Bathroom')) & 
                                         (sampleData['sensorID'].str.contains('Sink')) &
                                         (sampleData['message'].str.contains('Light'))])

    motion_area_count = len(sampleData[(sampleData['sensorID'].str.contains('Bathroom')) & 
                                         (sampleData['sensorID'].str.contains('Area')) &
                                         (sampleData['message'].str.contains('Motion')) &
                                         (sampleData['sensorValue'] == 'ON')])

    light_area_count = len(sampleData[(sampleData['sensorID'].str.contains('Bathroom')) & 
                                         (sampleData['sensorID'].str.contains('Area')) &
                                         (sampleData['message'].str.contains('Light'))])

    bathroom_sensor_count_dict = {
            "Motion-Toilet": motion_toilet_count, 
            "Motion-Sink": motion_sink_count, 
            "Motion-Area": motion_area_count,
            "Light-Toilet": light_toilet_count, 
            "Light-Sink": light_sink_count, 
            "Light-Area": light_area_count,
        }

    trip_stats_dict.update(bathroom_sensor_count_dict)
    trip_stats_dict['Wake-Up-Hr'] = wakeTime_hr
    trip_stats_dict['Wake-Up-Minute'] = wakeTime_min
    trip_stats_dict['Sleep-Hr'] = sleepTime_hr
    trip_stats_dict['Sleep-Minute'] = sleepTime_min

    return trip_stats_dict, trip_times_dict


def find_nightActivityFreq(sampleData, night_start_hour, night_start_min=0, night_start_sec=0):
    '''
    input:
    -- sampleData: sample data within the sample period
    -- night_start_hour: integer start hour of evening [0-23]
    -- night_start_min: integer start minute of evening [0-59]
    -- night_start_sec: integer start second of evening [0-59]
    output:
    -- nightActivityFreq : number of activities after a time at night (needs more discussion)'''
    ''''''
    night_activity_count = 0

    # Define the starting time for night activities
    night_start_time = time(night_start_min, night_start_min, night_start_sec)

    for i in range(0, sampleData.shape[0]):

        if sampleData.loc[i, 'time'] >= night_start_time:
            night_activity_count += 1
    
    return night_activity_count

def battery_per(sensor):
    pass

    return sampleData

def get_raw_df(rawFileName, rawDataCols, startDate = None, endDate = None):
    '''
    Input: 
    1. rawFileName: file name of raw sensor data txt
    2. sampleDuration: window duration (number of days)
    3. startDate: start date of data ('YYYY-MM-DD'), is None when not specified
    4. endDate: end date of data ('YYYY-MM-DD'), is None when not specified

    Output:
    1. a dataframe with raw sensor data
    '''''''''
    
    ## open and read raw data file
    with open(rawFileName, "r") as f:
        rawContent = f.read()

    ## loop through the raw content, seperate sensor data by sampleDuration, calculate features, populate feature file
    # need to skip the first four lines of data, related to Zigbee
    sampleData = pd.DataFrame(columns = rawDataCols) # a data frame, stores lines of sensor data within a sample period
     
    lineNum = 0 
    for line in rawContent.splitlines():
        lineNum += 1
        if lineNum <= 4:
            continue
        currLineTime = get_time_from_line(line)
        
        if startDate is not None and is_before_startDate(currLineTime, startDate): # skip lines before startDate
            print(currLineTime)
            continue  
        elif endDate is not None and is_after_endDate(currLineTime, endDate): # exit for loop if line is after endDate
            return sampleData
            break
        
        # append one row to the sampleData dataframe
        newRawRow = get_newRow_from_line(line) # returns a data frame
        sampleData = pd.concat([sampleData, newRawRow], ignore_index = True)

    return sampleData
  

