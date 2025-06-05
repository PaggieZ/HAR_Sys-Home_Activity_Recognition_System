import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import medfilt, find_peaks
from datetime import time

class sensor_data_preprocessor:

    def __init__(self, sample_data_df):
        self.sample_df = sample_data_df

    def resample_motion(self, sensor_location="BathroomAToilet"):
        self.sample_df['timestamp'] = pd.to_datetime(self.sample_df['timestamp'])

        # filter dataframe by location
        df_filtered = self.sample_df[
            (self.sample_df['sensorID'].str.contains(sensor_location, case=False)) 
        ]
        # filter dataframe by sensor type
        df_filtered = df_filtered[(self.sample_df['message'].str.contains("Control4-Motion", case=False))]

        if len(df_filtered) == 0:
            return None
        
        df_filtered["sensorValue"] = df_filtered["sensorValue"].map({"ON": 1, "OFF": 0})
        df_filtered.set_index('timestamp', inplace=True)

        df_resampled = df_filtered.resample('10s').ffill().reset_index()
        
        return df_resampled

    def resample_light(self, sensor_location="BedroomAArea"):
        self.sample_df['timestamp'] = pd.to_datetime(self.sample_df['timestamp'])

        # filter dataframe by location
        df_filtered = self.sample_df[
            (self.sample_df['sensorID'].str.contains(sensor_location, case=False)) 
        ]
        # filter dataframe by sensor type
        df_filtered = df_filtered[(self.sample_df['message'].str.contains("Control4-LightSensor", case=False))]


        if len(df_filtered) == 0:
            return None

        # auto fill data before the first timestamp
        first_timestamp = df_filtered['timestamp'].iloc[0]
        if first_timestamp.time() != pd.Timestamp('00:00:00').time():
            newRow = df_filtered.head(1)
            newRow['sensorValue'] = 0
            newRow['timestamp'] = first_timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
            # Append the new row at the beginning
            df_filtered = newRow._append(df_filtered, ignore_index=True)

        # fill data after the last timestamp
        last_timestamp = df_filtered['timestamp'].iloc[-1]
        if last_timestamp.time() < pd.Timestamp('23:59:59').time():
            newRow = df_filtered.tail(1)
            newRow['sensorValue'] = 0
            newRow['timestamp'] = first_timestamp.replace(hour=23, minute=59, second=59, microsecond=999999)
            # Append the new row at the end
            df_filtered = df_filtered._append(newRow, ignore_index=True)

        df_filtered.set_index('timestamp', inplace=True)
        # resample at 1 minute
        df_resampled = df_filtered.resample('1T').ffill().reset_index()
        
        return df_resampled
    
    def apply_filters_motion(self, df, column):
        if column not in df.columns:
            raise ValueError(f"Column '{column}' does not exist in the DataFrame.")

        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)
        #df[column + '_rolling_mean_10s'] = df[column].rolling(window=1, min_periods=1).max()
        #df[column + '_rolling_mean_50'] = df[column].rolling(window=5, min_periods=1).max()
        #df[column + '_rolling_mean_100s'] = df[column].rolling(window=10, min_periods=1).max()
        df[column + '_rolling_max_200s'] = df[column].rolling(window=20, min_periods=1).max()
        return df

    def apply_filters_light(self, df, column):
        if column not in df.columns:
            raise ValueError(f"Column '{column}' does not exist in the DataFrame.")

        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)
        df[column + '_rolling_mean'] = df[column].rolling(window=5, min_periods=1).mean()
        #df[column + '_exp_smoothing'] = df[column].ewm(alpha=0.3).mean()
        #df[column + '_median_filter'] = medfilt(df[column], kernel_size=3)
        #df[column + '_gaussian_noise_reduction'] = df[column].apply(
        #    lambda x: np.mean([x, np.random.normal(x, 0.1)])
        #)
        return df

    def visualize_resampled_data(self, df):
        df["sensorValue"] = df["sensorValue"].astype(float)
        plt.plot(df['timestamp'], df["sensorValue"])
        plt.show()
        return

    def visualize_filters_motion(self, df, column):
        if column not in df.columns:
            raise ValueError(f"Column '{column}' does not exist in the DataFrame.")

        filtered_sensorVal_col = df.columns.str.contains(column+"_")
        filtered_sensorVal_col = df.columns[filtered_sensorVal_col]
        
        num_filters = len(filtered_sensorVal_col)
        fig, axes = plt.subplots(num_filters, 1, figsize=(12, 6 * num_filters), sharex=True)
        fig.suptitle(f"Filtering Techniques Applied to {column}", fontsize=16, y=0.92)

        #OG_motionVal = df["sensorValue"].map({"ON": '1', "OFF": '0'})
        #print(OG_motionVal)

        axes.plot(df['timestamp'], df["sensorValue"], label='Original Data', linestyle='dashed', alpha=0.7)
        axes.plot(df['timestamp'], df["sensorValue_rolling_mean_200s"], label=filtered_sensorVal_col)


        axes.set_title("sensorValue_rolling_max_200s")

        axes.set_xlabel('Timestamp')
        axes.set_ylabel(column)
        axes.legend()
        axes.grid()

        # Store the filtered DataFrame

        '''
        for i, col in enumerate(filtered_df.columns):
            axes[i].plot(df['timestamp'], df["sensorValue"], label='Original Data', linestyle='dashed', alpha=0.7)
            axes[i].plot(df['timestamp'], filtered_df[col], label=col)
            axes[i].set_title(col)
            axes[i].set_xlabel('Timestamp')
            axes[i].set_ylabel(column)
            axes[i].legend()
            axes[i].grid()

            # Store the filtered DataFrame
            filtered_dataframes[col] = df[['timestamp', col]].copy()
        '''
        plt.tight_layout()
        plt.show()



    def visualize_filters_light(self, df, column):
        if column not in df.columns:
            raise ValueError(f"Column '{column}' does not exist in the DataFrame.")

        filtered_sensorVal_col = df.columns.str.contains(column+"_")
        filtered_sensorVal_col = df.columns[filtered_sensorVal_col]
        
        num_filters = len(filtered_sensorVal_col)
        fig, axes = plt.subplots(num_filters, 1, figsize=(12, 6 * num_filters), sharex=True)
        fig.suptitle(f"Filtering Techniques Applied to {column}", fontsize=16, y=0.92)

        #OG_motionVal = df["sensorValue"].map({"ON": '1', "OFF": '0'})
        #print(OG_motionVal)

        axes.plot(df['timestamp'], df["sensorValue"], label='Original Data', linestyle='dashed', alpha=0.7)
        axes.plot(df['timestamp'], df["sensorValue_rolling_mean"], label=filtered_sensorVal_col)
        axes.set_title("sensorValue_rolling_mean")
        axes.set_xlabel('Timestamp')
        axes.set_ylabel(column)
        axes.legend()
        axes.grid()

        # Store the filtered DataFrame

        '''
        for i, col in enumerate(filtered_df.columns):
            axes[i].plot(df['timestamp'], df["sensorValue"], label='Original Data', linestyle='dashed', alpha=0.7)
            axes[i].plot(df['timestamp'], filtered_df[col], label=col)
            axes[i].set_title(col)
            axes[i].set_xlabel('Timestamp')
            axes[i].set_ylabel(column)
            axes[i].legend()
            axes[i].grid()

            # Store the filtered DataFrame
            filtered_dataframes[col] = df[['timestamp', col]].copy()
        '''
        plt.tight_layout()
        plt.show()

    def calculate_area_under_curve(self, dfs):
        areas = {}
        for filter_name, df in dfs.items():
            df = df.sort_values('timestamp')
            timestamps = (df['timestamp'] - df['timestamp'].min()).dt.total_seconds()

            for col in df.columns:
                if col == 'timestamp':
                    continue

                area = np.trapz(df[col], x=timestamps)
                areas[f"{filter_name} - {col}"] = area
        return areas

    def get_AUC(self, input_df, col):
        input_df['timestamp'] = pd.to_datetime(input_df['timestamp'])
        # Detect the transition from 0 to a peak (0 -> non-zero)
        input_df['zero_to_peak'] = (input_df[col] == 0) & (input_df[col].shift(-1) > 0)
        #  the transition from a peak to 0 (non-zero -> 0)
        input_df['peak_to_zero'] = (input_df[col] > 0) & (input_df[col].shift(-1) == 0)
        # Find the timestamps of the valleys (start and end of peak periods)
        peak_df = input_df.loc[input_df['zero_to_peak'], ['timestamp']].reset_index(drop=True)
        peak_df = peak_df.rename(columns={'timestamp': 'start_of_peak'})
        peak_df['end_of_peak'] = input_df.loc[input_df['peak_to_zero'], 'timestamp'].reset_index(drop=True)

        
        AUC_arr = []
        
        for index, row in peak_df.iterrows():
            startTime = pd.to_datetime(row['start_of_peak'])
            endTime = pd.to_datetime(row['end_of_peak'])
            peakRange_df = input_df[(input_df['timestamp'] >= startTime) & (input_df['timestamp'] <= endTime)]
            peakRange_df["sensorValue"] = peakRange_df["sensorValue"].astype(float)
            AUC = peakRange_df['sensorValue'].sum()
            AUC_arr.append(AUC)
        peak_df["AUC"] = AUC_arr
        

        '''
        # Show the valley timestamps (start and end of peaks)
        print("Start of Peaks (0 to Peak):")
        print(peak_df['start_of_peak'])
        print("\nEnd of Peaks (Peak to 0):")
        print(peak_df['end_of_peak'])
        print(peak_df['AUC'])

        # Optional: Plot the data
        plt.plot(input_df['timestamp'], input_df[col], label='Sensor Value')
        plt.scatter(peak_df['start_of_peak'], input_df.loc[input_df['zero_to_peak'], col], color='green', label='Start of Peak (0 -> Peak)')
        plt.scatter(peak_df['end_of_peak'], input_df.loc[input_df['peak_to_zero'], col], color='red', label='End of Peak (Peak -> 0)')
        plt.xlabel('Timestamp')
        plt.ylabel(col)
        plt.title('Peak Transitions')
        plt.legend()
        plt.xticks(rotation=45)
        plt.show()
        '''
        return peak_df

    def get_wakeTime(self, peak_df):
        try:
            maxRow = peak_df.loc[peak_df['AUC'].idxmax()]
            return maxRow['start_of_peak']
        except Exception as e:
            return None
    
    def get_sleepTime(self, peak_df):
        try:
            maxRow = peak_df.loc[peak_df['AUC'].idxmax()]
        except Exception as e:
            return None

        # if there is only one peak
        if peak_df.shape[0] == 1:
            return maxRow['end_of_peak']
        timeAfterDaylight = maxRow['end_of_peak']
        timeAfterDaylight = pd.to_datetime(timeAfterDaylight)
        filtered_peak_df = peak_df[(peak_df['start_of_peak'] >= timeAfterDaylight)]

        if len(filtered_peak_df) == 0:    
            return None
        maxRow = filtered_peak_df.loc[filtered_peak_df['AUC'].idxmax()]
        return maxRow['end_of_peak']

#         maxRow = filtered_peak_df.loc[filtered_peak_df['AUC'].idxmax()]
#         return maxRow['start_of_peak']

    def visualize_light_and_wakeSleepTime(self, wakeTime, sleepTime, df, column):
        if column not in df.columns:
            raise ValueError(f"Column '{column}' does not exist in the DataFrame.")

        filtered_sensorVal_col = df.columns.str.contains(column+"_")
        filtered_sensorVal_col = df.columns[filtered_sensorVal_col]
        
        num_filters = len(filtered_sensorVal_col)
        fig, axes = plt.subplots(num_filters, 1, figsize=(12, 6 * num_filters), sharex=True)
        fig.suptitle(f"Filtering Techniques Applied to {column}", fontsize=16, y=0.92)

        #OG_motionVal = df["sensorValue"].map({"ON": '1', "OFF": '0'})
        #print(OG_motionVal)

        axes.plot(df['timestamp'], df["sensorValue"], label='Original Data', linestyle='dashed', alpha=0.7)
        axes.plot(df['timestamp'], df["sensorValue_rolling_mean"], label=filtered_sensorVal_col)
        axes.axvline(x=wakeTime, color='r', linestyle='--', linewidth=2, label='wake time')
        axes.axvline(x=sleepTime, color='g', linestyle='--', linewidth=2, label='sleep time')        
        axes.set_title("sensorValue_rolling_mean")
        axes.set_xlabel('Timestamp')
        axes.set_ylabel(column)
        axes.legend()
        axes.grid()

        # Store the filtered DataFrame

        '''
        for i, col in enumerate(filtered_df.columns):
            axes[i].plot(df['timestamp'], df["sensorValue"], label='Original Data', linestyle='dashed', alpha=0.7)
            axes[i].plot(df['timestamp'], filtered_df[col], label=col)
            axes[i].set_title(col)
            axes[i].set_xlabel('Timestamp')
            axes[i].set_ylabel(column)
            axes[i].legend()
            axes[i].grid()

            # Store the filtered DataFrame
            filtered_dataframes[col] = df[['timestamp', col]].copy()
        '''
        plt.tight_layout()
        plt.show()

    def upsample_activity(self, activity="Toilet"):
        try:
            self.sample_df['timestamp'] = pd.to_datetime(self.sample_df['timestamp'])
        except Exception as e:
            self.sample_df = self.sample_df

        # Create a new row with the same structure as df_filtered
        first_row = self.sample_df.iloc[[0]]
        timestamp = first_row["timestamp"]
        first_row["timestamp"] = timestamp[0].replace(hour = 0, minute = 0, second = 0)
        first_row["activity"] = "Sleep"
        #first_row_datetime = first_row["timestamp"].replace(hour = 0, minute = 0, second = 0)

        #new_first_row = pd.DataFrame({"timestamp": first_row_datetime, "sensorID": first_row["sensorID"], "newSensorID": first_row["newSensorID"],  "sensorValue": first_row["sensorValue"], "activity": first_row["activity"]})
        df_filtered = pd.concat([first_row, self.sample_df], ignore_index = True)
        
        last_row = self.sample_df.iloc[[-1]].reset_index(drop=True)
        timestamp = last_row["timestamp"]
        last_row["timestamp"] = timestamp[0].replace(hour = 23, minute = 59, second = 59)
        #last_row_datetime = last_row["timestamp"].replace(hour = 23, minute = 59, second = 59)
        #new_last_row = pd.DataFrame({"timestamp": last_row_datetime, "sensorID": last_row["sensorID"], "newSensorID": last_row["newSensorID"],  "sensorValue": last_row["sensorValue"], "activity": last_row["activity"]})
        df_filtered = pd.concat([df_filtered, last_row], ignore_index = True)
        
        df_filtered["sensorValue"] = df_filtered["activity"].map(lambda x: 1 if x == activity else 0)
        df_filtered.set_index('timestamp', inplace=True)

        df_resampled = df_filtered.resample('1s').ffill()
        
        #df_resampled = df_resampled.bfill()
        df_resampled = df_resampled.reset_index()
        
        return df_resampled

    def apply_filters_activity(self, df, column, activity="Toilet", threshold=0.8):
        if column not in df.columns:
            raise ValueError(f"Column '{column}' does not exist in the DataFrame.")

        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)
        #df[column + '_rolling_mean_10s'] = df[column].rolling(window=1, min_periods=1).max()
        #df[column + '_rolling_mean_50'] = df[column].rolling(window=5, min_periods=1).max()
        #df[column + '_rolling_mean_100s'] = df[column].rolling(window=10, min_periods=1).max()

        if activity == "Toilet":
            df[column + '_rolling_max_200s'] = df[column].rolling(window=20, min_periods=1).max()
        else: 
            df[column + '_rolling_mean_1hr'] = df[column].rolling(window=360, min_periods=1).mean()
            # 80% of 1hr = 48 minutes 
            df[column + '_rolling_mean_1hr'] = df[column + '_rolling_mean_1hr'].map(lambda x: 1 if x >= threshold else 0)
        return df

    def get_AL_sleep_wake_time(self, df):
        '''
        "Sleep" dataframe 
        - last column = 1 for sensor readings with activity label "Sleep"
        - last column = 0 for sensor readings for any other activity label
        '''

        ## Get the last "Sleep" sensor reading before 2pm 
        ## Get the first "Sleep" sensor reading after 2pm
        cols = df.columns
        current_day = df.iloc[0]['timestamp'].date()
        morning = time(14, 0, 0, 0)
        morning = pd.Timestamp.combine(date=current_day, time=morning)

        night = time(19, 0, 0, 0)
        night = pd.Timestamp.combine(date=current_day, time=night)
        # auc_df = self.get_AUC(input_df=df, col=cols[-1])
        # print(auc_df)
        
        df_before_morning = df[df['timestamp'] < morning]
        df_after_night = df[df['timestamp'] > night]
        try:
            wake_up_idx = df_before_morning[df_before_morning[cols[-1]] == 1].index.max()
            wake_time = df_before_morning.loc[wake_up_idx]['timestamp'].to_pydatetime().time() 
        except Exception as e:
            wake_time = None

        try:        
            sleep_idx = df_after_night[df_after_night[cols[-1]] == 1].index.min()
            sleep_time = df_after_night.loc[sleep_idx]['timestamp'].to_pydatetime().time()
        except Exception as e: 
            print(f"Error: {e}")
            sleep_time = None 

        return sleep_time, wake_time

        # return None, None


