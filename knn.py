import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
import networkx as nx
from sklearn.preprocessing import StandardScaler
from scipy.stats import chi2_contingency
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from mlxtend.plotting import plot_decision_regions 
from mpl_toolkits.mplot3d import Axes3D

def train_knn(labeled_feature_df, col_to_use):
    '''
    Input: 
    1. labeled_feature_df: dataframe of labeled features, the Ground truth column name is "UTILabel"
    2. col_to_use: name of columns used for KNN input, should exclude any time related columns

    The train_knn() function will take in a data frame containing features and ground truth,
    build data loaders with both test and train set. Use the train set to train a KNN model, 
    use the test set to test the trained model, and display a confusion matrix.
    '''''''''

    n_neighbors = 5
    alpha = 0.05  # significance level
    test_size = 0.2 # how many data will be used in test set, 0.2 means 20%, so 80% of data will be used as train set

    # drop UTILabel col
    feature_df = labeled_feature_df[col_to_use].drop("UTILabel", axis=1)
    UTILabel_df = labeled_feature_df["UTILabel"]

    # Standardize the features to have mean 0 and variance 1
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(feature_df)

    # Split the data into training and test sets
    # feature_train is features for train set
    # UTILabel_train is ground truth label for train set
    feature_train, feature_test, UTILabel_train, UTILabel_test = train_test_split(scaled_features, UTILabel_df, test_size = test_size)

    # Fit KNN model to the scaled data
    knn = KNeighborsClassifier(n_neighbors=n_neighbors)
    knn.fit(feature_train, UTILabel_train)

    # print the confusion matrix to evaluate the performance of the trained KNN
    print("KNN Confusin Matrix")
    predictions = knn.predict(feature_test)
    print(classification_report(UTILabel_test, predictions))

    ## display more graphs
    '''
    feature = feature_df.to_numpy().astype(np.float64)
    label = UTILabel_df.to_numpy().astype(int)
    # visualize decision region of the trained KNN model
    # Create a 3D scatter plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(feature[:, 0], feature[:, 1], feature[:, 2], c=label, cmap='coolwarm', edgecolor='k', s=50)
    ax.set_xlabel('Count')
    ax.set_ylabel('TimeMax')
    ax.set_zlabel('TimeAvg')
    plt.title('3D Feature Space')
    plt.show()
    '''

    '''
    ## plot using networkx
    # Get the nearest neighbors for each data point
    distances, indices = knn.kneighbors(feature_train)

    # Create a graph based on the neighbors
    G = nx.Graph()

    # Add nodes and edges based on KNN
    for i, neighbors in enumerate(indices):
        for neighbor in neighbors[1:]:
            G.add_edge(i, neighbor)


    # Set seed for reproducibility 
    np.random.seed(setseed)
    rep = nx.spring_layout(G, seed = setseed)

    ## for ploting KNN group with individual feature (not fully completed)
    # color_train = feature_train({bathCount: 'blue', bathTimeAvg: 'purple', bathTimeMax: 'pink'})

#     # # Visualize the KNN graph
    # plt.figure(figsize=(6, 6))
    # nx.draw(G, rep, with_labels=True, node_size=50, node_color= color_train, edge_color='gray', alpha=0.7)
    # plt.title('KNN Graph based on bathCount, bathMax, and bathAvg')
    # plt.show()

    # Color nodes by UTIL
    colors = UTILabel_train.values
    colors = ['green' if label == '0' else 'red' for label in colors ]  

    # Visualize with colored nodes
    plt.figure(figsize=(6, 6))
    nx.draw(G, rep, with_labels=True, node_size=50, node_color=colors, edge_color='gray', alpha=0.7)
    plt.title('KNN Graph with UTILabels')
    plt.show()
    '''

def chi2_test_for_features():
    
    # Use generated file form feature 
    feature_data = pd.read_csv('feature_label.csv')

    features = feature_data[['bathCount', 'bathTimeMax', 'bathTimeAvg']]
    labels = feature_data['UTILabel']

    # Discretize the continuous features into bins
    features_binned = pd.DataFrame()

    # Binning 'bathCount' into categories: Low, Medium, High
    features_binned['bathCount'] = pd.cut(features['bathCount'], bins=[0, 5, 10, 20], labels=['Low', 'Medium', 'High'])

    # Binning 'bathTimeMax' into categories: Low, Medium, High
    features_binned['bathTimeMax'] = pd.cut(features['bathTimeMax'], bins=[0, 50, 100, 150], labels=['Low', 'Medium', 'High'])

    # Binning 'bathTimeAvg' into categories: Low, Medium, High
    features_binned['bathTimeAvg'] = pd.cut(features['bathTimeAvg'], bins=[0, 10, 20, 30], labels=['Low', 'Medium', 'High'])

    # Contingency table for each feature with 'UTILabel'
    # This table shows the frequency of each combination of feature and UTILabel

    contingency_bathCount = pd.crosstab(features_binned['bathCount'], labels)
    contingency_bathTimeMax = pd.crosstab(features_binned['bathTimeMax'], labels)
    contingency_bathTimeAvg = pd.crosstab(features_binned['bathTimeAvg'], labels)

    # Perform the Chi-Square test on each contingency table
    chi2_bathCount, p_bathCount, dof_bathCount, expected_bathCount = chi2_contingency(contingency_bathCount)
    chi2_bathTimeMax, p_bathTimeMax, dof_bathTimeMax, expected_bathTimeMax = chi2_contingency(contingency_bathTimeMax)
    chi2_bathTimeAvg, p_bathTimeAvg, dof_bathTimeAvg, expected_bathTimeAvg = chi2_contingency(contingency_bathTimeAvg)

    # Print the results
    print("Chi-Square Test Results for 'bathCount' vs 'UTILabel'")
    print(f"Chi-Square Statistic: {chi2_bathCount}")
    print(f"P-Value: {p_bathCount}")
    print(f"Degrees of Freedom: {dof_bathCount}")
    print("Expected Frequencies:")
    print(expected_bathCount)

    print("\nChi-Square Test Results for 'bathTimeMax' vs 'UTILabel'")
    print(f"Chi-Square Statistic: {chi2_bathTimeMax}")
    print(f"P-Value: {p_bathTimeMax}")
    print(f"Degrees of Freedom: {dof_bathTimeMax}")
    print("Expected Frequencies:")
    print(expected_bathTimeMax)

    print("\nChi-Square Test Results for 'bathTimeAvg' vs 'UTILabel'")
    print(f"Chi-Square Statistic: {chi2_bathTimeAvg}")
    print(f"P-Value: {p_bathTimeAvg}")
    print(f"Degrees of Freedom: {dof_bathTimeAvg}")
    print("Expected Frequencies:")
    print(expected_bathTimeAvg)

    # Interpretation of results
    if p_bathCount < alpha:
        print("\nThere is a significant relationship between 'bathCount' and 'UTILabel'.")
    else:
        print("\nThere is no significant relationship between 'bathCount' and 'UTILabel'.")

    if p_bathTimeMax < alpha:
        print("There is a significant relationship between 'bathTimeMax' and 'UTILabel'.")
    else:
        print("There is no significant relationship between 'bathTimeMax' and 'UTILabel'.")

    if p_bathTimeAvg < alpha:
        print("There is a significant relationship between 'bathTimeAvg' and 'UTILabel'.")
    else:
        print("There is no significant relationship between 'bathTimeAvg' and 'UTILabel'.")