import serial
import sys
import select
import time as tt
from serial.tools import list_ports
import plotData as plotData
import processRaw as processRaw
from state_tracker import *
import labelData as labelData
import processFeature as processFeature
import randomForest as randomForest
import warnings
import pandas as pd

warnings.simplefilter("ignore")

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

TM_TRAIN_COLS = ["day_night_max_duration", "day_night_avg_duration", 
                    "day_max_duration", "day_avg_duration",   
                    "night_max_duration", "night_avg_duration",  
                    "day_trip_count", "night_trip_count", "all_trip_count", 
                    "Motion-Toilet", "Motion-Sink",  "Motion-Area",  
                    "Light-Toilet", "Light-Sink",  "Light-Area", "Wake-Up-Hr", "Sleep-Hr", "UTILabel"]

sampleDuration = 1 # analyze the raw sensor day by 1 day



available_ports = list(list_ports.comports())
for port in available_ports:
  print(f"Found {port.device}")
# serName = "/dev/rfcomm0"
serName = available_ports[0].device
ser = serial.Serial(serName)
print("Initializing serial port...")
tt.sleep(3)
#print("After 3 seconds")
print("Checking port...")
print(ser.isOpen())
print("Ready")
ser.write(b"Raspberry Pi Listening")


def check_input():
  return select.select([sys.stdin], [], [], 0)[0]

def getPrediction(labeledFeatureFileName, date):
  ## run random forest model
  feature_df = processFeature.get_feature_df(labeledFeatureFileName)
  feature_df.replace([None, ""], 0, inplace=True)
  model = randomForest.train_random_forest(feature_df, TM_TRAIN_COLS)
  prediction = randomForest.getDayUTIPrediction(model = model, labeledFeatureFile = labeledFeatureFileName, date = date, col_to_use=TM_TRAIN_COLS)
  if prediction == '0':
    prediction = "False"
  else:
    prediction = "True"
  return prediction

def getSleepTime(labeledFeatureFileName, date):
  # Load the CSV file with headers and parse startTime as datetime
  df = pd.read_csv(labeledFeatureFileName, parse_dates=["startTime"])
  # Find the index of the matching row
  match_date = pd.to_datetime(date).date()
  match_index = df[df["startTime"].dt.date == match_date].index

  # Get the matching row and the one above it
  first_index = max(match_index[0] - 1, 0)  # Prevent out-of-bounds

  # Extract Sleep time from previous row
  sleep_hr = df.loc[first_index, "Sleep-Hr"]
  sleep_min = df.loc[first_index, "Sleep-Minute"]
    # Extract Wake time from matching row
  wake_hr = df.loc[match_index[0], "Wake-Up-Hr"]
  wake_min = df.loc[match_index[0], "Wake-Up-Minute"]

  bath_trip_count = df.loc[match_index[0], "all_trip_count"]
  
  totalSleepMin = (24 - sleep_hr - 1) * 60
  totalSleepMin = totalSleepMin + (60 - sleep_min)
  totalSleepMin = totalSleepMin + (wake_hr * 60) + wake_min

  duration_hr = totalSleepMin // 60
  duration_min = totalSleepMin % 60

  duration_hr_str = str(duration_hr)
  duration_min_str = str(duration_min)
  if duration_hr < 10:
    duration_hr_str = "0" + duration_hr_str

  if duration_min < 10:
    duration_min_str = "0" + duration_min_str

  return (duration_hr_str + ":" + duration_min_str), bath_trip_count

#print(getSleepTime("DemoLabeledFeature.csv", "2017-11-02"))


'''
PI_SEND_START%[date: DD:MM:YYYY HH:MM:SS];
[sleep duration: HH:MM];[total toilet trips];[UTI result];
[sensor with low batteries]
&[dates for sleep: MM/DD/YYYY,MM/DD/YYYY x7];[duration: HH:MM,HH:MM x7]
&[dates for toilet trip: MM/DD/YYYY,MM/DD/YYYY x7];[trip count: int,int x7]
&[sensor names: a,b x5];[battery level for each sensor: int, int x5]%PI_SEND_END
'''
def getData(date):
  '''
  outStr = "PI_SEND_START%01/10/2018 15:28:30;" \
        "00:00;5;True;" \
        "HALLWAYA,BEDROOMAAREA" \
        "&01/01/2018,01/02/2018,01/03/2018;08:00,00:00,01:10" \
        "&01/01/2018,01/02/2018;3,5" \
        "&HALLWAYA,OFFICEAAREA,BEDROOMAAREA;0,80,20%PI_SEND_END"
  '''
  print("Predicting UTI...")
  labeledFeatureFileName = "DemoLabeledFeature.csv"
  sleepDuration, bath_trip_count = getSleepTime(labeledFeatureFileName, date)
  prediction = getPrediction(labeledFeatureFileName, date)
  
  outStr = "PI_SEND_START%"
  outStr = outStr + date + ";"
  outStr = outStr + sleepDuration + ";"
  outStr = outStr + str(bath_trip_count) + ";"
  outStr = outStr + prediction + ";"
  outStr = outStr + "HALLWAYA,BEDROOMAAREA&"

  date_arr = [date]
  sleepDuration_arr = [sleepDuration]
  bathTrip_arr = [str(bath_trip_count)]

  print("Reading past features...")
  df = pd.read_csv(labeledFeatureFileName, parse_dates=["startTime"])
  currDate = date
  for i in range(6):
    # Find the index of the matching row
    match_date = pd.to_datetime(currDate).date()
    match_index = df[df["startTime"].dt.date == match_date].index
    # Get the matching row and the one above it
    first_index = max(match_index[0] - 1, 0)  # Prevent out-of-bounds
    # Extract Sleep time from previous row
    prevDate = df.loc[first_index, "Date"]
    sleepDuration, bath_trip_count = getSleepTime(labeledFeatureFileName, prevDate)
    date_arr = [str(prevDate)] + date_arr
    sleepDuration_arr = [sleepDuration] + sleepDuration_arr
    bathTrip_arr = [str(bath_trip_count)] + bathTrip_arr
    currDate = prevDate

  date_str = ",".join(date_arr)
  outStr = outStr + date_str + ";"

  sleepDuration_str = ",".join(sleepDuration_arr)
  outStr = outStr + sleepDuration_str + "&"

  outStr = outStr + date_str + ";"

  bathTrip_str = ",".join(bathTrip_arr)
  outStr = outStr + bathTrip_str + "&"

  outStr = outStr + "HALLWAYA,OFFICEAAREA,BEDROOMAAREA;0,80,20%PI_SEND_END"
  
  
  outStr = outStr + "\n"
  return outStr

#print(getData("2017-11-02"))


def processRawSensorData():
  # rawFileName = "./DemoRawSensorData.txt"
  rawFileName = "./SmallDemoRaw.txt"
  featureFileName = "SmallDemoFeature.csv"
  processRaw.extract_features(rawFileName = rawFileName, sampleDuration = sampleDuration, featureFileName = featureFileName, rawDataCols = TM_RAW_SENSOR_COLS, featureDataCols = TM_FEATURE_COLS)
  ## label the extracted features
  groundTruthFileName = "./GroundTruth - Sheet1.csv"
  #labeledFeatureFileName = "DemoLabeledFeature.csv"
  labeledFeatureFileName = "SmallDemoLabeledFeature.csv"
  print()
  print("** labeling ground truth...")
  labelData.label_feature_file_with_groudtruth(featureFileName, groundTruthFileName, labeledFeatureFileName)
  print("PROCESS done")
  print()


while True:
  if ser.in_waiting > 0:
    data = ser.readline()
    print(f"Received: {data.decode('utf-8').strip()}")

    if data.decode() == "GET_DATA\n":
      print("Received GET_DATA")
      tt.sleep(0.5)
      data = ser.readline()
      print("Date: " + data.decode())
      '''
      str = "PI_SEND_START%01/10/2018 15:28:30;" \
        "00:00;5;True;" \
        "HALLWAYA,BEDROOMAAREA" \
        "&01/01/2018,01/02/2018,01/03/2018;08:00,00:00,01:10" \
        "&01/01/2018,01/02/2018;3,5" \
        "&HALLWAYA,OFFICEAAREA,BEDROOMAAREA;0,80,20%PI_SEND_END"
      '''
      # only send date into getData
      data = data.decode().strip()
      print(data)
      strData = getData(data)
      
      print(strData)
      ser.write(strData.encode())
      print("*** DATA sent")
 
  if check_input():
    # read user input
    user_input = sys.stdin.readline().strip()
    if user_input == "SEND_STR": # if user want to send string
      user_input = input("String to send: ") # read the data that is about to be sent
      print(f"You entered: {user_input}")
      ser.write(user_input.encode())
      print("input sent")
    elif user_input == "PROCESS": # feature extraction, GT label
      processRawSensorData()
    elif user_input == "SEND_DATA": # Pi user send data to phone, need to run model
      date = input("Date: ") # read date
      outStr = getData(date)
      ser.write(outStr.encode())
      print("data sent")


  tt.sleep(1)

