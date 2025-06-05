from datetime import datetime, timedelta
import pandas as pd 
import matplotlib.pyplot as plt

import pandas as pd
import os


def label_feature_file_with_groudtruth(featureFileName, groundTruthFileName, outputFileName):
    
    # Load the feature data
    feature_data = pd.read_csv(featureFileName)
    gt_data = pd.read_csv(groundTruthFileName)

    # Remove whitespaces
    feature_data.columns = feature_data.columns.str.strip()
    gt_data.columns = gt_data.columns.str.strip()
    
    # Convert 'Date' column in ground truth to datetime format
    gt_data['Date'] = pd.to_datetime(gt_data['Date'])
    feature_data['Date'] = pd.to_datetime(feature_data['startTime']).dt.date

    # Compare the columns
    feature_data['UTILabel'] = feature_data['Date'].apply(
        lambda x: 1 if x in gt_data['Date'].dt.date.values else 0
    )

    # Save the updated feature file
    feature_data.to_csv(outputFileName, index=False, mode = 'w')


