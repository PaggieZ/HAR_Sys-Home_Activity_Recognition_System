import pandas as pd
from sensor_data_preprocessor import sensor_data_preprocessor
from processRaw import get_raw_df  

rawFileName = "./tm003.2018.txt"
raw_data_columns = ["timestamp", "sensorID", "sensorValue", "message"]

start_date = "2018-01-01"
end_date = "2018-01-03"

raw_df = get_raw_df(rawFileName, raw_data_columns, start_date, end_date)

preprocessor = sensor_data_preprocessor(raw_df)

resampled_df = preprocessor.resample_motion(sensor_location="BathroomAArea")
print(resampled_df.columns)

filtered_df = preprocessor.apply_filters_motion(resampled_df, "sensorValue")

filtered_dataframes = preprocessor.visualize_filters_motion(filtered_df, "sensorValue")

# Debug
print("Filtered dataframes keys:", filtered_dataframes.keys())
#print("Filtered dataframes values:", filtered_dataframes.values())

areas = preprocessor.calculate_area_under_curve(filtered_dataframes)

# Debug
print("Area calculation results:", areas)

print("Area under the curve for each filter:")
for filter_name, area in areas.items():
    print(f"{filter_name}: {area:.2f}")

