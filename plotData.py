from datetime import datetime, timedelta
import pandas as pd 
import matplotlib.pyplot as plt

def plot_raw_data(input_df):
    if input_df.empty:
        return
    
    df = input_df
    df["sensorValue"] = df["sensorValue"].map({"ON": 1, "OFF": 0}).fillna(df["sensorValue"])  # Map ON/OFF to 1/0, keep numerical values intact
    
    unique_sensors = df["sensorID"].unique()
    unique_sensor_types = df["message"].unique() 
    
    # Create subplots
    num_subplots = len(unique_sensor_types)
    fig, axs = plt.subplots(num_subplots, 1, figsize=(12, 4 * num_subplots), sharex=True)

    if num_subplots == 1:  # Handle case with one sensor type
        axs = [axs]

    for ax, sensor_type in zip(axs, unique_sensor_types):
        for sensor_id in unique_sensors:
            sensor_data = df[(df["sensorID"] == sensor_id) & (df["message"] == sensor_type)]
            if not sensor_data.empty:
                ax.step(sensor_data["timestamp"], sensor_data["sensorValue"], label=sensor_id, where="post")
        ax.set_title(f"Sensor Type: {sensor_type}")
        ax.set_ylabel("State (On/Off)")
        ax.legend(loc="upper right")
        ax.grid(True)
    
    plt.xlabel("Time")
    plt.tight_layout()
    plt.show()



def plot_feature_file(featureFileName):
    '''
    The next graphs generates when you closed
    '''
    data = pd.read_csv(featureFileName)

    # Clean column names to remove leading/trailing spaces
    data.columns = data.columns.str.strip()

    # Convert startTime to datetime for proper plotting
    data['startTime'] = pd.to_datetime(data['startTime'])

    fig, axes = plt.subplots(3, 1, figsize=(12, 12), sharex=True)

    # Plot Bath Max Time
    axes[0].plot(data['startTime'], data['bathTimeMax'], label='Bath Max Time', marker='o', color='b')
    axes[0].set_title('Bath Max Time Over Time')
    axes[0].set_ylabel('Bath Max Time')
    axes[0].grid(True)

     # Plot Bath Avg Time
    axes[1].plot(data['startTime'], data['bathTimeAvg'], label='Bath Avg Time', marker='o', color='g')
    axes[1].set_title('Bath Avg Time Over Time')
    axes[1].set_ylabel('Bath Avg Time')
    axes[1].grid(True)

    # Plot Bath Count
    axes[2].plot(data['startTime'], data['bathCount'], label='Bath Count', marker='o', color='r')
    axes[2].set_title('Bath Count Over Time')
    axes[2].set_xlabel('Time')
    axes[2].set_ylabel('Bath Count')
    axes[2].grid(True)

    # Show the plot
    plt.tight_layout()
    plt.show()


def plot_ground_truth_file(groundTruthFileName):
    """
    Reads ground truth CSV file, sorts it by date and time, and plots sensor data.

    Parameters:
    groundTruthFileName (str): The name of the ground truth file (.csv).
    """
    try:
        df = pd.read_csv(groundTruthFileName)

        if "Date" not in df.columns or "Time" not in df.columns:
            print("Error: The file must contain 'Date' and 'Time' columns.")
            return

        # Combine Date and Time into a single DateTime column
        df["DateTime"] = pd.to_datetime(df["Date"] + " " + df["Time"], errors='coerce')
        df = df.dropna(subset=["DateTime"]) 
        df = df.sort_values(by="DateTime")

        print("Data range: ", df["DateTime"].min(), "to", df["DateTime"].max())
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")
        try:
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)
        except Exception as e:
            print(f"Invalid date format: {e}")
            return

        # filter data within the  range
        mask = (df["DateTime"] >= start_date) & (df["DateTime"] <= end_date)
        filtered_df = df[mask]

        if filtered_df.empty:
            print("No data available within the specified date range.")
            return

        filtered_df["State"] = filtered_df["Sensor data"].map({"ON": 1, "OFF": 0})

        unique_locations = filtered_df["Sensor location"].unique()
        plt.figure(figsize=(12, 8))

        for idx, location in enumerate(unique_locations):
            location_data = filtered_df[filtered_df["Sensor location"] == location]
            plt.step(
                location_data["DateTime"], 
                location_data["State"] + idx, 
                label=location, 
                where='post'
            )

        plt.xlabel("Time")
        plt.ylabel("State (On/Off)")
        plt.title(f"Sensor Data for Patient {filtered_df['Patient_ID'].iloc[0]}")
        plt.yticks(
            ticks=range(len(unique_locations)), 
            labels=unique_locations
        )
        plt.legend(loc="upper right")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Error processing the ground truth file: {e}")


import matplotlib
# matplotlib.use('TkAgg')  # Use TkAgg backend
# import pandas as pd
# import matplotlib.pyplot as plt
# import os
# from matplotlib.backends.backend_tkagg import (
#     FigureCanvasTkAgg,
#     NavigationToolbar2Tk
# )
# import tkinter as tk


def plot_labeled_file(featureFileName, outputFileName='feature_label.csv'):
    feature_data = pd.read_csv(featureFileName)  # Read the feature file with proper headers

    # Plot the data (scatter plot between bathCount, bathMax, and bathMin)
    plt.figure(figsize=(10, 6))
    plt.scatter(feature_data['bathCount'], feature_data['bathMax'], label='Bath Max', color='blue', alpha=0.6)
    plt.scatter(feature_data['bathCount'], feature_data['bathMin'], label='Bath Min', color='red', alpha=0.6)

    # Adding labels and title
    plt.title('Bath Count vs Bath Max/Min')
    plt.xlabel('Bath Count')
    plt.ylabel('Value')
    plt.legend()

    # Save the plot as PNG
    plot_path = '/Users/akirali/Desktop/bluetooth/Smart-Home-Behavior-Detection/plot_labeled_feature.png'
    plt.savefig(plot_path, dpi=300)
    print(f"Plot saved at: {plot_path}")

    # Show the plot
    plt.show()
### If above doesnt work use below code in terminal
#
# # Create the scatter plot
# plt.figure(figsize=(10, 6))
# plt.scatter(df['bathCount'], df['bathMax'], label='Bath Max', color='blue', alpha=0.6)
# plt.scatter(df['bathCount'], df['bathMin'], label='Bath Min', color='red', alpha=0.6)
#
# # Add labels and title
# plt.title('Bath Count vs Bath Max/Min')
# plt.xlabel('Bath Count')
# plt.ylabel('Value')
# plt.legend()
# # Display the plot
# plt.show()

def cor_motion_light():
    '''
    correlation between motion and light sensor data.
    '''
    pass


def plot_motion_data(input_df):
    if input_df.empty:
        return
    
    motion_df = input_df[input_df["message"] == "Control4-Motion"]
    print(motion_df)

    motion_df["sensorValue"] = motion_df["sensorValue"].map({"ON": 1, "OFF": 0}).fillna(motion_df["sensorValue"])  # Map ON/OFF to 1/0, keep numerical values intact
    print(motion_df)

    unique_sensors = motion_df["sensorID"].unique()

    for sensor_id in unique_sensors:
        sensor_data = motion_df[(motion_df["sensorID"] == sensor_id)]
        if not sensor_data.empty:
            plt.step(sensor_data["timestamp"], sensor_data["sensorValue"], label=sensor_id, where="post")
    
    plt.title("Motion Raw Data")
    plt.ylabel("State (On/Off)")
    plt.legend(loc="upper right")
    plt.grid(True)
    
    plt.xlabel("Time")
    plt.tight_layout()
    plt.show()

def plot_light_data(input_df):
    if input_df.empty:
        return
    
    motion_df = input_df[input_df["message"] == "Control4-LightSensor"]


    unique_sensors = motion_df["sensorID"].unique()

    for sensor_id in unique_sensors:
        sensor_data = motion_df[(motion_df["sensorID"] == sensor_id)]
        if not sensor_data.empty:
            plt.step(sensor_data["timestamp"], sensor_data["sensorValue"], label=sensor_id, where="post")
    
    plt.title("Light Raw Data")
    plt.ylabel("State (On/Off)")
    plt.legend(loc="upper right")
    plt.grid(True)
    
    plt.xlabel("Time")
    plt.tight_layout()
    plt.show()



def plot_bath_motion_light_data(input_df):
    if input_df.empty:
        return
    
    motion_df = input_df[(input_df["message"] == "Control4-Motion") | (input_df["message"] == "Control4-LightSensor")]
    print(motion_df)

    bath_df = motion_df[motion_df["sensorID"].str.contains("Bathroom", case=False, na=False)]

    bath_df["sensorValue"] = bath_df["sensorValue"].map({"ON": float(50.0), "OFF": float(0.0)}).fillna(bath_df["sensorValue"])  # Map ON/OFF to 1/0, keep numerical values intact
    bath_df["sensorValue"] = pd.to_numeric(bath_df["sensorValue"], errors="coerce").fillna(0).astype(int)
    print(bath_df)

    # Convert timestamp column to datetime for better plotting
    bath_df["timestamp"] = pd.to_datetime(bath_df["timestamp"], errors="coerce")

    # Create subplots for dual visualization
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    # First subplot: Plotting by unique message
    unique_messages = bath_df["message"].unique()
    for message in unique_messages:
        sensor_data = bath_df[bath_df["message"] == message]
        axes[0].step(sensor_data["timestamp"], sensor_data["sensorValue"], label=message, where="post")

    axes[0].set_title("Sensor Values by Message")
    axes[0].set_ylabel("Sensor Value")
    axes[0].legend()
    axes[0].grid(True)

    # Second subplot: Plotting by unique sensorID
    unique_sensors = bath_df["sensorID"].unique()
    for sensor_id in unique_sensors:
        sensor_data = bath_df[bath_df["sensorID"] == sensor_id]
        axes[1].step(sensor_data["timestamp"], sensor_data["sensorValue"], label=sensor_id, where="post")

    axes[1].set_title("Sensor Values by Sensor ID")
    axes[1].set_ylabel("Sensor Value")
    axes[1].set_xlabel("Timestamp")
    axes[1].legend()
    axes[1].grid(True)

    # Improve plot appearance
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_bed_motion_data(input_df):
    if input_df.empty:
        return
    
    motion_df = input_df[input_df["message"] == "Control4-Motion"]
    print(motion_df)

    motion_df["sensorValue"] = motion_df["sensorValue"].map({"ON": 1, "OFF": 0}).fillna(motion_df["sensorValue"])  # Map ON/OFF to 1/0, keep numerical values intact
    print(motion_df)

    bed_df = motion_df[motion_df["sensorID"].str.contains("Bedroom", case=False, na=False)]

    unique_sensors = bed_df["sensorID"].unique()

    for sensor_id in unique_sensors:
        sensor_data = bed_df[(bed_df["sensorID"] == sensor_id)]
        if not sensor_data.empty:
            plt.step(sensor_data["timestamp"], sensor_data["sensorValue"], label=sensor_id, where="post")
    
    plt.title("Motion Raw Data")
    plt.ylabel("State (On/Off)")
    plt.legend(loc="upper right")
    plt.grid(True)
    
    plt.xlabel("Time")
    plt.tight_layout()
    plt.show()

def plot_bed_motion_light_data(input_df):
    if input_df.empty:
        return
    
    motion_df = input_df[(input_df["message"] == "Control4-Motion") | (input_df["message"] == "Control4-LightSensor")]
    print(motion_df)

    bath_df = motion_df[motion_df["sensorID"].str.contains("Bedroom", case=False, na=False)]

    bath_df["sensorValue"] = bath_df["sensorValue"].map({"ON": float(50.0), "OFF": float(0.0)}).fillna(bath_df["sensorValue"])  # Map ON/OFF to 1/0, keep numerical values intact
    bath_df["sensorValue"] = pd.to_numeric(bath_df["sensorValue"], errors="coerce").fillna(0).astype(int)
    print(bath_df)

    # Convert timestamp column to datetime for better plotting
    bath_df["timestamp"] = pd.to_datetime(bath_df["timestamp"], errors="coerce")

    # Create subplots for dual visualization
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    # First subplot: Plotting by unique message
    unique_messages = bath_df["message"].unique()
    for message in unique_messages:
        sensor_data = bath_df[bath_df["message"] == message]
        axes[0].step(sensor_data["timestamp"], sensor_data["sensorValue"], label=message, where="post")

    axes[0].set_title("Sensor Values by Message")
    axes[0].set_ylabel("Sensor Value")
    axes[0].legend()
    axes[0].grid(True)

    # Second subplot: Plotting by unique sensorID
    unique_sensors = bath_df["sensorID"].unique()
    for sensor_id in unique_sensors:
        sensor_data = bath_df[bath_df["sensorID"] == sensor_id]
        axes[1].step(sensor_data["timestamp"], sensor_data["sensorValue"], label=sensor_id, where="post")

    axes[1].set_title("Sensor Values by Sensor ID")
    axes[1].set_ylabel("Sensor Value")
    axes[1].set_xlabel("Timestamp")
    axes[1].legend()
    axes[1].grid(True)

    # Improve plot appearance
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_AL_sleep(input_df):
    if input_df.empty:
        return


    plt.plot(input_df["timestamp"], input_df["sensorValue"])
    
    plt.title("Motion Raw Data")
    plt.ylabel("State (On/Off)")
    plt.legend(loc="upper right")
    plt.grid(True)
    
    plt.xlabel("Time")
    plt.tight_layout()
    plt.show()