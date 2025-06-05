import pandas as pd
from sensor_data_preprocessor import sensor_data_preprocessor
from processRaw import get_raw_df  

rawFileName = "./tm003.2018.txt"
raw_data_columns = ["timestamp", "sensorID", "sensorValue", "message"]

start_date = "2018-01-02"
end_date = "2018-01-03"

raw_df = get_raw_df(rawFileName, raw_data_columns, start_date, end_date)

preprocessor = sensor_data_preprocessor(raw_df)

resampled_df = preprocessor.resample_light(sensor_location="BedroomAArea")

filtered_df = preprocessor.apply_filters_light(resampled_df, "sensorValue")

# preprocessor.visualize_filters_light(filtered_df, "sensorValue")

peak_df = preprocessor.get_AUC(filtered_df, "sensorValue_rolling_mean")

wakeTime = preprocessor.get_wakeTime(peak_df)
print(wakeTime)
sleepTime = preprocessor.get_sleepTime(peak_df)
print(sleepTime)

preprocessor.visualize_light_and_wakeSleepTime(wakeTime, sleepTime, filtered_df, "sensorValue")