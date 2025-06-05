import pandas as pd 
from datetime import datetime

def get_feature_df(feature_file_name, start_date = None, end_date = None):
    ## open and read feature data file
    with open(feature_file_name, "r") as f:
        featureContent = f.read()


    lineNum = 0
    column_name = []
    for line in featureContent.splitlines():
        lineNum += 1
        if lineNum == 1:
            column_name = get_column_name(line)
            featureData = pd.DataFrame(columns = column_name)
            continue
        currLineTime = get_time_from_feature_line(line)
        
        if start_date is not None and is_before_startDate(currLineTime, start_date): # skip lines before startDate
            print(currLineTime)
            continue  
        elif end_date is not None and is_after_endDate(currLineTime, end_date): # exit for loop if line is after endDate
            return featureData
            break
        
        # append one row to the featureData dataframe
        newRawRow = get_newRow_from_line(line, column_name) # returns a data frame
        featureData = pd.concat([featureData, newRawRow], ignore_index = True)

    return featureData

def get_time_from_feature_line(line):
    timestamp = line.split(',')[0]
    return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f") 

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
    
def get_column_name(line):
    header = line.split(',')
    return header

def get_newRow_from_line(line, column_name):
    value = line.split(',')
    featureData = pd.DataFrame([value], columns = column_name)
    return featureData