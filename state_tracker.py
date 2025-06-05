from datetime import time, timedelta, date, datetime
import numpy as np
IDLE = 0
IN_BATHROOM = 1
LEAVING_BATHROOM = 2
MOVING_AWAY = 3

# class ActivityStateTracker:
#     '''
#     Tracks the bathroom activity of a patient
#     '''
#     def __init__(self, initial_state, threshold_min=1, threshold_max=90, threshold_light=10, threshold_temp=25, nighttime_hr=20, nighttime_min=0, daytime_hr=7, daytime_min=0):
#         '''
#         nighttime_hr: (0-24)
#         nightime_min: (0-60)
#         '''
#         self.state = initial_state
#         self.nighttime = time(nighttime_hr, nighttime_min, 0, 0)
#         self.daytime = time(daytime_hr, daytime_min)
#         self.start_time = None
#         self.light_sensor_count = 0
#         self.count = 0 
#         self.bath_light_is_on = False
#         self.trip_times_dict = {"Day": [], "Night": []}
#         self.is_shower = False
#         self.threshold_min = threshold_min
#         self.threshold_max = threshold_max
#         self.threshold_light = threshold_light
#         self.threshold_temp = threshold_temp
#         self.area = None
#         self.bathroom_sensor_count_dict = {
#             "Motion-Toilet": 0, 
#             "Motion-Sink": 0, 
#             "Motion-Area": 0,
#             "Light-Toilet": 0, 
#             "Light-Sink": 0, 
#             "Light-Area": 0,
#         }

#     def input(self, dataframe_row):
        
#         sensor_timestamp, sensor_id, sensor_value, sensor_message = self.read_dataframe_info(dataframe_row=dataframe_row)

#         if self.state == IDLE:
            
#             self.is_shower = False

#             if 'bathroom' in sensor_id.lower() and 'LightSensor' in sensor_message and int(sensor_value) > self.threshold_light:
#                 self.bath_light_is_on = True
#                 self.state = IN_BATHROOM
#                 self.start_time = sensor_timestamp
            
#             elif 'Bathroom' in sensor_id and 'Motion' in sensor_message and sensor_value == 'ON':
#                 self.state = IN_BATHROOM
#                 self.start_time = sensor_timestamp

#             else:
#                 self.state = IDLE
            
#         elif self.state == IN_BATHROOM:
            
#             self.update_sensor_count_dict(sensor_timestamp, sensor_id, sensor_value, sensor_message)
#             self.light_sensor_count = 0 
#             self.count = 0 

#             if 'bathroom' in sensor_id.lower() and 'LightSensor' in sensor_message and int(sensor_value) > self.threshold_light:
#                 self.bath_light_is_on = True

#             if 'bathroom' in sensor_id.lower() and 'LightSensor' in sensor_message and self.bath_light_is_on and int(sensor_value) <= self.threshold_light:
#                 self.state = LEAVING_BATHROOM
#                 self.light_sensor_count = 1

#             elif 'bathroom' in sensor_id.lower() and 'Temperature' in sensor_message and float(sensor_value) >= self.threshold_temp:
#                 self.is_shower = True
            
#             elif ('Hallway' in sensor_id or 'Bedroom' in sensor_id) and 'Motion' in sensor_message and sensor_value == 'ON':
#                 self.state = MOVING_AWAY
#                 self.count = 1

#             else:
#                 self.state = IN_BATHROOM

#         elif self.state == LEAVING_BATHROOM:

#             today_nighttime = self.get_today_nighttime(sensor_timestamp=sensor_timestamp)
#             today_daytime = self.get_today_daytime(sensor_timestamp=sensor_timestamp)
#             is_night = False

#             if 'Bathroom' in sensor_id and 'LightSensor' in sensor_message and int(sensor_value) <= self.threshold_light:
#                 self.light_sensor_count += 1
            
#             if self.light_sensor_count >= 1 and self.is_shower == False:
#                 if sensor_timestamp < today_daytime + timedelta(hours=1) or sensor_timestamp >= today_nighttime - timedelta(hours=1):
#                     is_night = True
#                 self.add_bathroom_trip(current_timestamp=sensor_timestamp, is_night=is_night)
#                 self.state = IDLE
            
#             elif self.light_sensor_count >= 1 and self.is_shower == True:
#                 self.state = IDLE

#             elif 'Bathroom' in sensor_id and 'LightSensor' in sensor_message and int(sensor_value) > self.threshold_light:
#                 self.state = IN_BATHROOM

#             elif ('Hallway' in sensor_id or 'Bedroom' in sensor_id) and 'Motion' in sensor_message and sensor_value == 'ON':
#                 self.state = MOVING_AWAY
#                 self.count = 1

#             else:
#                 self.state = LEAVING_BATHROOM

#         elif self.state == MOVING_AWAY:

#             today_nighttime = self.get_today_nighttime(sensor_timestamp=sensor_timestamp)
#             today_daytime = self.get_today_daytime(sensor_timestamp=sensor_timestamp)
#             is_night = False
            
#             if ('Hallway' in sensor_id or 'Bedroom' in sensor_id) and ('Motion' in sensor_message or 'LightSensor' in sensor_message):
#                 self.count += 1

#             if self.count >= 3:
#                 if sensor_timestamp < today_daytime + timedelta(hours=1) or sensor_timestamp >= today_nighttime - timedelta(hours=1):
#                     is_night = True
#                 self.state = IDLE
#                 self.add_bathroom_trip(current_timestamp=sensor_timestamp, is_night=is_night) 

#             elif 'Bathroom' in sensor_id and 'LightSensor' in sensor_message and int(sensor_value) <= self.threshold_light:
#                 self.light_sensor_count += 1
#                 self.state = LEAVING_BATHROOM

#             elif 'Bathroom' in sensor_id and (('Motion' in sensor_message and sensor_value == 'ON') or ('LightSensor' in sensor_message and int(sensor_value) > self.threshold_light)):
#                 self.state = IN_BATHROOM

#             else: 
#                 self.state = MOVING_AWAY


#     def update_sensor_count_dict(self, sensor_timestamp, sensor_id, sensor_value, sensor_message):
        
#         # if "Bathroom" in sensor_id and "Toilet" in sensor_id and "LightSensor" in sensor_message and int(sensor_value) > self.threshold_light:
#         #     self.bathroom_sensor_count_dict["Light-Toilet"] += 1
#         if "Bathroom" in sensor_id and "Toilet" in sensor_id and "LightSensor" in sensor_message:
#             self.bathroom_sensor_count_dict["Light-Toilet"] += 1
#         elif "Bathroom" in sensor_id and "Toilet" in sensor_id and "Motion" in sensor_message and sensor_value == "ON":
#             self.bathroom_sensor_count_dict["Motion-Toilet"] += 1
#         elif "Bathroom" in sensor_id and "Sink" in sensor_id and "LightSensor" in sensor_message:
#             self.bathroom_sensor_count_dict["Light-Sink"] += 1
#         elif "Bathroom" in sensor_id and "Sink" in sensor_id and "Motion" in sensor_message and sensor_value == "ON":
#             self.bathroom_sensor_count_dict["Motion-Sink"] += 1
#         elif "Bathroom" in sensor_id and "Area" in sensor_id and "LightSensor" in sensor_message:
#             self.bathroom_sensor_count_dict["Light-Area"] += 1
#         elif "Bathroom" in sensor_id and "Area" in sensor_id and "Motion" in sensor_message and sensor_value == "ON":
#             self.bathroom_sensor_count_dict["Motion-Area"] += 1

#     def get_today_nighttime(self, sensor_timestamp):

#         today_date = sensor_timestamp.date()
#         return datetime.combine(today_date, self.nighttime)  

#     def get_today_daytime(self, sensor_timestamp):

#         today_date = sensor_timestamp.date()
#         print(f"Processing time: {sensor_timestamp}")
#         return datetime.combine(today_date, self.daytime) 
    
#     def reset_sensor_count_dict(self):

#         for key, value in self.bathroom_sensor_count_dict.items():
#             self.bathroom_sensor_count_dict[key] = 0
    

#     def add_bathroom_trip(self, current_timestamp, is_night=False):

#         this_trip_time = (current_timestamp - self.start_time).total_seconds() / 60 
#         if is_night:
#             self.trip_times_dict["Day"].append((this_trip_time))
#         else:
#             self.trip_times_dict["Night"].append((this_trip_time))
    

#     def read_dataframe_info(self, dataframe_row):
#         '''
#         Input: dataframe row
#         Output: timestamp, id, value, and message of this sensor reading
#         '''
#         sensor_id = dataframe_row['sensorID']
#         sensor_message = dataframe_row['message']
#         sensor_timestamp = dataframe_row['timestamp']
#         sensor_value = dataframe_row['sensorValue']

#         return sensor_timestamp, sensor_id, sensor_value, sensor_message
        
#     def filter_trip_times(self):
#         '''
#         Filter out short trips that may be considered too short
#         '''
#         self.trip_times_dict["Day"] = [time for time in self.trip_times_dict["Day"] if time > self.threshold_min and time < self.threshold_max]
#         self.trip_times_dict["Night"] = [time for time in self.trip_times_dict["Night"] if time > self.threshold_min and time < self.threshold_max]

#     def get_trip_stats(self):
#         '''
#         Return number of bathroom trips, longest trip time, and average duration  
#         '''

#         all_trips = []
#         all_trips.extend(self.trip_times_dict["Day"])
#         all_trips.extend(self.trip_times_dict["Night"])
        
#         if len(all_trips) != 0:
#             day_night_max_duration = max(all_trips)
#             day_night_avg_duration = sum(all_trips) / len(all_trips)
#         else: 
#             day_night_max_duration = float('nan')
#             day_night_avg_duration = float('nan')

#         if len(self.trip_times_dict["Day"]) != 0:
#             day_max_duration = max(self.trip_times_dict["Day"])
#             day_avg_duration = sum(self.trip_times_dict["Day"]) / len(self.trip_times_dict["Day"])
#         else:
#             day_max_duration = float('nan')
#             day_avg_duration = float('nan') 
        
#         if len(self.trip_times_dict["Night"]) != 0:
#             night_max_duration = max(self.trip_times_dict["Night"])
#             night_avg_duration = sum(self.trip_times_dict["Night"]) / len(self.trip_times_dict["Night"])
        
#         else: 
#             night_max_duration = float('nan')
#             night_avg_duration = float('nan')

#         stats_dict = {
#             "day_night_max_duration": day_night_max_duration, 
#             "day_night_avg_duration": day_night_avg_duration,
#             "day_max_duration": day_max_duration, 
#             "day_avg_duration": day_avg_duration, 
#             "night_max_duration": night_max_duration,
#             "night_avg_duration": night_avg_duration, 
#             "day_trip_count": len(self.trip_times_dict["Night"]),
#             "night_trip_count": len(self.trip_times_dict["Day"]),
#             "all_trip_count": len(all_trips),   
#         }

#         stats_dict.update(self.bathroom_sensor_count_dict)

#         durations_dict = {
#             "Day": self.trip_times_dict["Day"],
#             "Night": self.trip_times_dict["Night"], 
#             "All": all_trips, 
#         }

#         return stats_dict, durations_dict
    

#     def get_state(self):
#         return self.state


class BathroomStateTracker:
    '''
    Tracks the bathroom activity of a patient
    '''
    def __init__(self, initial_state, nighttime_hr=21, nighttime_min=0, daytime_hr=7, daytime_min=0):
        '''
        nighttime_hr: (0-24)
        nightime_min: (0-60)
        daytime_hr: (0-24)
        daytime_min: (0-60)
        '''
        self.state = initial_state
        self.nighttime = time(nighttime_hr, nighttime_min, 0, 0)
        self.daytime = time(daytime_hr, daytime_min)
        self.start_time = None
        self.bath_light_is_on = False
        self.trip_times_dict = {"Day": [], "Night": []}
        self.bathroom_sensor_count_dict = {
            "Motion-Toilet": 0, 
            "Motion-Sink": 0, 
            "Motion-Area": 0,
            "Light-Toilet": 0, 
            "Light-Sink": 0, 
            "Light-Area": 0,
        }

    def input(self, dataframe_row):
        
        sensor_timestamp, sensor_id, sensor_value, sensor_message, sensor_filtered_value = self.read_dataframe_info(dataframe_row=dataframe_row)

        if self.state == IDLE:

            if sensor_filtered_value == 1:
                self.state = IN_BATHROOM
                self.start_time = sensor_timestamp
            
            else:
                self.state = IDLE
            
        elif self.state == IN_BATHROOM:

            today_nighttime = self.get_today_nighttime(sensor_timestamp=sensor_timestamp)
            today_daytime = self.get_today_daytime(sensor_timestamp=sensor_timestamp)
            is_night = False

            if sensor_filtered_value == 0: 
                
                if sensor_timestamp < today_daytime or sensor_timestamp >= today_nighttime:
                    is_night = True 
                self.add_bathroom_trip(current_timestamp=sensor_timestamp, is_night=is_night)
                self.state = IDLE
            
            else:
                self.state = IN_BATHROOM

    def get_today_nighttime(self, sensor_timestamp):

        today_date = sensor_timestamp.date()
        return datetime.combine(today_date, self.nighttime)  

    def get_today_daytime(self, sensor_timestamp):

        today_date = sensor_timestamp.date()
        return datetime.combine(today_date, self.daytime) 
    

    def add_bathroom_trip(self, current_timestamp, is_night=False):

        this_trip_time = (current_timestamp - self.start_time).total_seconds() / 60 
        if is_night:
            self.trip_times_dict["Night"].append((this_trip_time))
        else:
            self.trip_times_dict["Delay"].append((this_trip_time))
    

    def read_dataframe_info(self, dataframe_row):
        '''
        Input: dataframe row
        Output: timestamp, id, value, message, filtered value of this sensor reading
        '''
        cols = dataframe_row.index.values
        sensor_id = dataframe_row['sensorID']
        sensor_message = dataframe_row['message']
        sensor_timestamp = dataframe_row['timestamp']
        sensor_value = dataframe_row['sensorValue']
        sensor_filtered_value = dataframe_row[cols[-1]]

        return sensor_timestamp, sensor_id, sensor_value, sensor_message, sensor_filtered_value
        
    # def filter_trip_times(self):
    #     '''
    #     Filter out short trips that may be considered too short
    #     '''
    #     self.trip_times_dict["Day"] = [time for time in self.trip_times_dict["Day"] if time > self.threshold_min and time < self.threshold_max]
    #     self.trip_times_dict["Night"] = [time for time in self.trip_times_dict["Night"] if time > self.threshold_min and time < self.threshold_max]

    def get_trip_stats(self):
        '''
        Return number of bathroom trips, longest trip time, and average duration  
        '''

        all_trips = []
        all_trips.extend(self.trip_times_dict["Day"])
        all_trips.extend(self.trip_times_dict["Night"])
        
        if len(all_trips) != 0:
            day_night_max_duration = max(all_trips)
            day_night_avg_duration = sum(all_trips) / len(all_trips)
        else: 
            day_night_max_duration = float('nan')
            day_night_avg_duration = float('nan')

        if len(self.trip_times_dict["Day"]) != 0:
            day_max_duration = max(self.trip_times_dict["Day"])
            day_avg_duration = sum(self.trip_times_dict["Day"]) / len(self.trip_times_dict["Day"])
        else:
            day_max_duration = float('nan')
            day_avg_duration = float('nan') 
        
        if len(self.trip_times_dict["Night"]) != 0:
            night_max_duration = max(self.trip_times_dict["Night"])
            night_avg_duration = sum(self.trip_times_dict["Night"]) / len(self.trip_times_dict["Night"])
        
        else: 
            night_max_duration = float('nan')
            night_avg_duration = float('nan')

        stats_dict = {
            "day_night_max_duration": day_night_max_duration, 
            "day_night_avg_duration": day_night_avg_duration,
            "day_max_duration": day_max_duration, 
            "day_avg_duration": day_avg_duration, 
            "night_max_duration": night_max_duration,
            "night_avg_duration": night_avg_duration, 
            "day_trip_count": len(self.trip_times_dict["Day"]),
            "night_trip_count": len(self.trip_times_dict["Night"]),
            "all_trip_count": len(all_trips),   
        }

        durations_dict = {
            "Day": self.trip_times_dict["Day"],
            "Night": self.trip_times_dict["Night"], 
            "All": all_trips, 
        }

        return stats_dict, durations_dict
    

    def get_state(self):
        return self.state

class ToiletALTracker: 
    '''
    Tracks the bathroom activity of a patient using the data labeled by Dr. Cook's AL model
    Trained on GT data from CASAS
    '''
    def __init__(self, initial_state, nighttime_hr=21, nighttime_min=0, daytime_hr=7, daytime_min=0):
        '''
        nighttime_hr: (0-24)
        nightime_min: (0-60)
        daytime_hr: (0-24)
        daytime_min: (0-60)
        '''
        self.state = initial_state
        self.nighttime = time(nighttime_hr, nighttime_min, 0, 0)
        self.daytime = time(daytime_hr, daytime_min)
        self.start_time = None
        self.bath_light_is_on = False
        self.trip_times_dict = {"Day": [], "Night": []}
        self.bathroom_sensor_count_dict = {
            "Motion-Toilet": 0, 
            "Motion-Sink": 0, 
            "Motion-Area": 0,
        }

    def input(self, dataframe_row):
        
        sensor_timestamp, sensor_id, new_sensor_id, sensor_value, activity_label, sensor_filtered_value = self.read_dataframe_info(dataframe_row=dataframe_row)

        if self.state == IDLE:

            if sensor_filtered_value == 1:
                self.state = IN_BATHROOM
                self.start_time = sensor_timestamp
            
            else:
                self.state = IDLE
            
        elif self.state == IN_BATHROOM:

            today_nighttime = self.get_today_nighttime(sensor_timestamp=sensor_timestamp)
            today_daytime = self.get_today_daytime(sensor_timestamp=sensor_timestamp)
            is_night = False

            if sensor_filtered_value == 0: 
                
                if sensor_timestamp < today_daytime or sensor_timestamp >= today_nighttime:
                    is_night = True 
                self.add_bathroom_trip(current_timestamp=sensor_timestamp, is_night=is_night)
                self.state = IDLE
            
            else:
                self.state = IN_BATHROOM

    def get_today_nighttime(self, sensor_timestamp):

        today_date = sensor_timestamp.date()
        return datetime.combine(today_date, self.nighttime)  

    def get_today_daytime(self, sensor_timestamp):

        today_date = sensor_timestamp.date()
        return datetime.combine(today_date, self.daytime) 
    

    def add_bathroom_trip(self, current_timestamp, is_night=False):

        this_trip_time = (current_timestamp - self.start_time).total_seconds() / 60 
        if is_night:
            self.trip_times_dict["Night"].append((this_trip_time))
        else:
            self.trip_times_dict["Day"].append((this_trip_time))
    

    def read_dataframe_info(self, dataframe_row):
        '''
        Input: dataframe row
        Output: timestamp, id, value, message, filtered value of this sensor reading
        '''
        cols = dataframe_row.index.values
        sensor_id = dataframe_row['sensorID']
        new_sensor_id = dataframe_row['newSensorID']
        sensor_activity = dataframe_row['activity']
        sensor_timestamp = dataframe_row['timestamp']
        sensor_value = dataframe_row['sensorValue']
        sensor_filtered_value = dataframe_row[cols[-1]]

        return sensor_timestamp, sensor_id, new_sensor_id, sensor_value, sensor_activity, sensor_filtered_value
        
    # def filter_trip_times(self):
    #     '''
    #     Filter out short trips that may be considered too short
    #     '''
    #     self.trip_times_dict["Day"] = [time for time in self.trip_times_dict["Day"] if time > self.threshold_min and time < self.threshold_max]
    #     self.trip_times_dict["Night"] = [time for time in self.trip_times_dict["Night"] if time > self.threshold_min and time < self.threshold_max]

    def get_trip_stats(self):
        '''
        Return number of bathroom trips, longest trip time, and average duration  
        '''

        all_trips = []
        all_trips.extend(self.trip_times_dict["Day"])
        all_trips.extend(self.trip_times_dict["Night"])
        
        if len(all_trips) != 0:
            day_night_max_duration = max(all_trips)
            day_night_avg_duration = sum(all_trips) / len(all_trips)
        else: 
            day_night_max_duration = float('nan')
            day_night_avg_duration = float('nan')

        if len(self.trip_times_dict["Day"]) != 0:
            day_max_duration = max(self.trip_times_dict["Day"])
            day_avg_duration = sum(self.trip_times_dict["Day"]) / len(self.trip_times_dict["Day"])
        else:
            day_max_duration = float('nan')
            day_avg_duration = float('nan') 
        
        if len(self.trip_times_dict["Night"]) != 0:
            night_max_duration = max(self.trip_times_dict["Night"])
            night_avg_duration = sum(self.trip_times_dict["Night"]) / len(self.trip_times_dict["Night"])
        
        else: 
            night_max_duration = float('nan')
            night_avg_duration = float('nan')

        stats_dict = {
            "day_night_max_duration": day_night_max_duration, 
            "day_night_avg_duration": day_night_avg_duration,
            "day_max_duration": day_max_duration, 
            "day_avg_duration": day_avg_duration, 
            "night_max_duration": night_max_duration,
            "night_avg_duration": night_avg_duration, 
            "day_trip_count": len(self.trip_times_dict["Day"]),
            "night_trip_count": len(self.trip_times_dict["Night"]),
            "all_trip_count": len(all_trips),   
        }

        durations_dict = {
            "Day": self.trip_times_dict["Day"],
            "Night": self.trip_times_dict["Night"], 
            "All": all_trips, 
        }

        return stats_dict, durations_dict
    

    def get_state(self):
        return self.state
