import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
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
data['unit_price'] = pd.to_numeric(data['unit_price'])
data['area'] = pd.to_numeric(data['area'])

# Visualize data
# Example: Bar chart for total price by location
plt.figure(figsize=(12, 6))
#Comparing the average value of a numerical variable across different categories.
sns.barplot(x='location', y='total_price', data=data, ci=None)
plt.title('Total Price of Houses by Location')
plt.xlabel('Location')
plt.ylabel('Total Price')
plt.savefig('./lianjia_secondhand/pic_of_anal/total_price.png')

# Example: Scatter plot for unit price vs area
plt.figure(figsize=(8, 8))
sns.scatterplot(x='area', y='unit_price', data=data)
plt.title('Area vs Unit Price')
plt.xlabel('Area')
plt.ylabel('Unit Price')
plt.savefig('./lianjia_secondhand/pic_of_anal/unit_price.png')

# Perform cluster analysis
# Select features for clustering
X = data[['total_price', 'unit_price', 'area']]

# Standardize the features
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Perform KMeans clustering
kmeans = KMeans(n_clusters=4, random_state=43)
data['cluster'] = kmeans.fit_predict(X_scaled)

# Visualize clustering results
# Example: Pie chart for distribution of clusters
plt.figure(figsize=(6, 6))
data['cluster'].value_counts().plot.pie(autopct='%1.1f%%')
plt.title('Cluster Distribution')
plt.savefig('./lianjia_secondhand/pic_of_anal/cluster.png')

# Scatter plot to show clusters based on area vs. total price
plt.figure(figsize=(10, 6))
sns.scatterplot(x='area', y='total_price', hue='cluster', data=data, palette='viridis')
plt.title('Clusters based on Area vs. Total Price')
plt.xlabel('Area')
plt.ylabel('Total Price')
plt.legend(title='Cluster')
plt.grid(True)
plt.tight_layout()
plt.savefig('./lianjia_secondhand/pic_of_anal/area_total_price_clusters.png')


# Scatter plot to show clusters based on area vs. total price
plt.figure(figsize=(10, 6))
sns.scatterplot(x='area', y='unit_price', hue='cluster', data=data, palette='viridis')
plt.title('Clusters based on Area vs. Unit Price')
plt.xlabel('Area')
plt.ylabel('Unit Price')
plt.legend(title='Cluster')
plt.grid(True)
plt.tight_layout()
plt.savefig('./lianjia_secondhand/pic_of_anal/area_unit_price_clusters.png')

# Example: Line graph for total price by cluster
plt.figure(figsize=(8, 6))
sns.lineplot(x='cluster', y='total_price', data=data)
plt.title('Total Price by Cluster')
plt.xlabel('Cluster')
plt.ylabel('Total Price')
# Invert y-axis and show plot
plt.savefig('./lianjia_secondhand/pic_of_anal/cluster-t.png')

# Example: Line graph for unit price by cluster
plt.figure(figsize=(8, 6))
sns.lineplot(x='cluster', y='unit_price', data=data)
plt.title('Unit Price by Cluster')
plt.xlabel('Cluster')
plt.ylabel('Unit Price')
# Invert y-axis and show plot
plt.savefig('./lianjia_secondhand/pic_of_anal/cluster-u.png')

# Example: Line graph for area by cluster
plt.figure(figsize=(8, 6))
sns.lineplot(x='cluster', y='area', data=data)
plt.title('Area by Cluster')
plt.xlabel('Cluster')
plt.ylabel('Area')
# Invert y-axis and show plot
plt.savefig('./lianjia_secondhand/pic_of_anal/cluster-a.png')

# Close the MySQL connection
connection.close()