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

# Set font to support Chinese characters
plt.rcParams['font.sans-serif'] = ['SimHei']  # Set a Chinese font that supports Chinese characters
plt.rcParams['axes.unicode_minus'] = False  # Ensure that minus sign is displayed correctly

# Convert 'total_price' column to numeric type
data['total_price'] = pd.to_numeric(data['total_price'])
data['area'] = pd.to_numeric(data['area'])

""" # Perform one-hot encoding for the "location" feature
data = pd.get_dummies(data, columns=['location'])

# Select the 'area' column and one-hot encoded 'location' columns for the features
X = data[['area'] + list(data.columns[data.columns.str.startswith('location_')])] """

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

""" # Create a DataFrame with actual and predicted values
results = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
results_sorted = results.sort_values('Actual')

# Visualize the actual vs. predicted values
plt.figure(figsize=(10, 6))
plt.scatter(results_sorted['Actual'], results_sorted['Predicted'], color='blue')
plt.plot([results_sorted['Actual'].min(), results_sorted['Actual'].max()], [results_sorted['Actual'].min(), results_sorted['Actual'].max()], linestyle='--', color='red')
plt.xlabel('Actual Total Price')
plt.ylabel('Predicted Total Price')
plt.title('Actual vs. Predicted Total Price')
plt.show() """

# Visualize the actual vs. predicted values
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, color='blue')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], linestyle='--', color='red')
plt.xlabel('Actual Total Price')
plt.ylabel('Predicted Total Price')
plt.title('Actual vs. Predicted Total Price')
plt.grid(True)
plt.tight_layout()
# Save the plot in a specific directory
plt.savefig('./lianjia_secondhand/pic_of_pred/predict0.png')

""" # Get the list of location columns (assuming they are one-hot encoded)
location_columns = data.columns[data.columns.str.startswith('location_')]

# Iterate over each location column
for location_col in location_columns:
    location_name = location_col.split('_')[-1]  # Extract the location name from the column name
    
    # Filter the data for the current location
    location_data = data[data[location_col] == 1]
    
    # Extract the features and target variable for the current location
    X_location = location_data[['area'] + list(location_data.columns[location_data.columns.str.startswith('location_')])]
    y_location = location_data['total_price']
    
    # Make predictions for the current location
    y_pred_location = model.predict(X_location)
    
    # Visualize the area vs. predicted total price for the current location
    plt.figure(figsize=(10, 6))
    plt.scatter(location_data['area'], y_pred_location, color='blue', label='Predicted Total Price')
    plt.xlabel('Area')
    plt.ylabel('Predicted Total Price')
    plt.title(f'Area vs. Predicted Total Price in {location_name}')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    # Save the plot for the current location in a specific directory
    plt.savefig(f'./lianjia_secondhand/pic_of_anal/{location_name}_predict.png') """
    
# Get the list of columns (assuming they are one-hot encoded)
columns = data.columns[data.columns.str.startswith(('b_type_', 'configuration_', 'renovation_', 'floor_', 'orientation_', 'location_'))]

# Iterate over each column
for col in columns:
    column_name = col.split('_')[-1]  # Extract the column name from the column name
    
    # Filter the data for the current column
    data_col = data[data[col] == 1]
    
    # Extract the features and target variable for the current column
    X_col = data_col[['area'] + list(data_col.columns[data.columns.str.startswith(('b_type_', 'configuration_', 'renovation_', 'floor_', 'orientation_', 'location_'))])]
    y_col = data_col['total_price']
    
    # Make predictions for the current column
    y_pred_col = model.predict(X_col)
    
    # Visualize the area vs. predicted total price for the current column
    plt.figure(figsize=(10, 6))
    plt.scatter(data_col['area'], y_pred_col, color='blue', label='Predicted Total Price')
    plt.xlabel('Area')
    plt.ylabel('Predicted Total Price')
    plt.title(f'Area vs. Predicted Total Price in {column_name}')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    # Save the plot for the current column in a specific directory
    plt.savefig(f'./lianjia_secondhand/pic_of_anal/{column_name}_predict.png')


# Close the MySQL connection
connection.close()