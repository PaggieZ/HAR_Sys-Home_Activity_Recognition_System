from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import imblearn
import numpy as np

def train_random_forest(labeled_feature_df, col_to_use):
    test_size = 0.4

    # drop UTILabel col
    feature_df = labeled_feature_df[col_to_use].drop("UTILabel", axis=1)
    UTILabel_df = labeled_feature_df["UTILabel"]

    # Split the data into training and test sets
    feature_train, feature_test, UTILabel_train, UTILabel_test = train_test_split(feature_df, UTILabel_df, test_size = test_size, stratify = UTILabel_df)
    count = UTILabel_train.value_counts()
    print("UTILabel_train before SMOTE")
    print(count)

    count = UTILabel_test.value_counts()
    print("UTILabel_test")
    print(count)



    ## handle imbalanced dataset (for TM003, there are 10 total UTI positive days)
    # over sample the minority class (positive UTI)
    oversample = imblearn.over_sampling.SMOTE(sampling_strategy = 1)
    feature_train, UTILabel_train = oversample.fit_resample(feature_train, UTILabel_train)

    count = UTILabel_train.value_counts()
    print("UTILabel_train after SMOTE")
    print(count)



    # initialize model
    model = RandomForestClassifier()
    # fit the model to training
    model.fit(feature_train, UTILabel_train)

    # Now that the model is fitted, evaluate how well it is performing
    predictions = model.predict(feature_test)
    unique_values, counts = np.unique(predictions, return_counts=True)

    # Display results
    print("Prediction")
    print("Unique values:", unique_values)
    print("Counts:", counts)

    print(classification_report(UTILabel_test, predictions))