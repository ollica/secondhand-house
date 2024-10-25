import pymysql
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np

# Connect to MySQL database
connection = pymysql.connect(host='localhost', user='root', password='2001', database='house')

# Fetch data from MySQL
query = "SELECT * FROM lianjia_data"
data = pd.read_sql_query(query, connection)

# Perform one-hot encoding for the "b_type", "configuration", "renovation", "floor", "orientation", and "location" features
data = pd.get_dummies(data, columns=['b_type', 'configuration', 'renovation', 
                                     'floor', 'orientation', 'location'])

# Select the original columns and one-hot encoded columns for the features
X = data[['area'] + 
         [col for col in data.columns 
          if col.startswith(('b_type_', 'configuration_', 'renovation_', 'floor_', 'orientation_', 'location_'))]]

# Define the target variable
y = data['total_price']

# Assuming X, y are prepared and split into X_train, X_test, y_train, y_test
# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Print the shapes of the training and testing sets
print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)
print("y_train shape:", y_train.shape)
print("y_test shape:", y_test.shape)

# Train a Random Forest Regressor model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions on the testing data
y_pred = model.predict(X_test)

# Evaluate the model using Mean Squared Error
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)