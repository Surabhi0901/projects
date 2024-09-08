# Importing important libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap
import dash
from dash import dcc, html
import plotly.express as px
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Reading the data

df = pd.read_csv(r'C:\Users\sy090\Downloads\PROJECTS\chicago_crime_data_analyzer\Sample Crime Dataset - Sheet1.csv')
#print(df.head())

# Plotting for visualization

df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y %H:%M')

df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day
df['Hour'] = df['Date'].dt.hour

crime_trends_year = df.groupby('Year').size()

plt.figure(figsize=(10, 5))
plt.plot(crime_trends_year, marker='o')
plt.title('Crime Trends Over Years')
plt.xlabel('Year')
plt.ylabel('Number of Crimes')
plt.grid(True)
plt.show()

crime_trends_hour = df.groupby('Hour').size()

plt.figure(figsize=(10, 5))
plt.plot(crime_trends_hour, marker='o', color='red')
plt.title('Peak Crime Hours')
plt.xlabel('Hour of the Day')
plt.ylabel('Number of Crimes')
plt.grid(True)
plt.show()

crime_data_geo = df.dropna(subset=['Latitude', 'Longitude'])

m = folium.Map(location=[41.8781, -87.6298], zoom_start=11)

heat_data = [[row['Latitude'], row['Longitude']] for index, row in crime_data_geo.iterrows()]
HeatMap(heat_data).add_to(m)

m.save(r'C:\\Users\\sy090\\Downloads\\PROJECTS\\chicago_crime_data_analyzer\\chicago_crime_heatmap.html')

crime_by_district = df.groupby('District').size()
crime_by_ward = df.groupby('Ward').size()

plt.figure(figsize=(12, 6))
crime_by_district.plot(kind='bar', color='skyblue')
plt.title('Crime Rates by District')
plt.xlabel('District')
plt.ylabel('Number of Crimes')
plt.grid(True)
plt.show()

plt.figure(figsize=(12, 6))
crime_by_ward.plot(kind='bar', color='orange')
plt.title('Crime Rates by Ward')
plt.xlabel('Ward')
plt.ylabel('Number of Crimes')
plt.grid(True)
plt.show()

primary_type_counts = df['Primary Type'].value_counts()

plt.figure(figsize=(14, 7))
primary_type_counts.plot(kind='bar', color='skyblue')
plt.title('Distribution of Crime Types')
plt.xlabel('Primary Type')
plt.ylabel('Frequency')
plt.xticks(rotation=90)
plt.grid(True)
plt.show()

description_counts = df['Description'].value_counts()

plt.figure(figsize=(14, 7))
description_counts[:20].plot(kind='bar', color='orange')  # Display top 20 descriptions
plt.title('Distribution of Crime Descriptions (Top 20)')
plt.xlabel('Description')
plt.ylabel('Frequency')
plt.xticks(rotation=90)
plt.grid(True)
plt.show()

severe_crimes = ['HOMICIDE', 'ASSAULT', 'ROBBERY', 'CRIM SEXUAL ASSAULT', 'BATTERY']
less_severe_crimes = ['THEFT', 'FRAUD', 'CRIMINAL DAMAGE', 'NARCOTICS', 'OTHER OFFENSE']

df['Severity'] = df['Primary Type'].apply(lambda x: 'Severe' if x in severe_crimes else ('Less Severe' if x in less_severe_crimes else 'Other'))

severity_counts = df['Severity'].value_counts()

plt.figure(figsize=(8, 5))
severity_counts.plot(kind='bar', color=['red', 'green', 'blue'])
plt.title('Distribution of Severe vs. Less Severe Crimes')
plt.xlabel('Severity')
plt.ylabel('Frequency')
plt.xticks(rotation=0)
plt.grid(True)
plt.show()

severe_crime_counts = df[df['Severity'] == 'Severe']['Primary Type'].value_counts()

plt.figure(figsize=(12, 6))
severe_crime_counts.plot(kind='bar', color='red')
plt.title('Distribution of Severe Crime Types')
plt.xlabel('Severe Crime Type')
plt.ylabel('Frequency')
plt.xticks(rotation=90)
plt.grid(True)
plt.show()

arrest_rates = df.groupby('Primary Type')['Arrest'].mean()

plt.figure(figsize=(14, 7))
arrest_rates.plot(kind='bar', color='green')
plt.title('Arrest Rates by Crime Type')
plt.xlabel('Crime Type')
plt.ylabel('Arrest Rate')
plt.grid(True)
plt.show()

domestic_crimes = df[df['Domestic'] == True].shape[0]
non_domestic_crimes = df[df['Domestic'] == False].shape[0]

labels = ['Domestic', 'Non-Domestic']
sizes = [domestic_crimes, non_domestic_crimes]
colors = ['#ff9999','#66b3ff']
plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
plt.title('Domestic vs. Non-Domestic Crimes')
plt.show()

df['Month'] = df['Date'].dt.month
df['Season'] = df['Month'].apply(lambda x: 'Winter' if x in [12, 1, 2] else
                                                         ('Spring' if x in [3, 4, 5] else
                                                          ('Summer' if x in [6, 7, 8] else 'Fall')))
seasonal_trends = df.groupby('Season').size()

plt.figure(figsize=(10, 5))
seasonal_trends.plot(kind='bar', color=['blue', 'green', 'orange', 'brown'])
plt.title('Seasonal Crime Trends')
plt.xlabel('Season')
plt.ylabel('Number of Crimes')
plt.xticks(rotation=0)
plt.grid(True)
plt.show()

crime_type_seasonal = df.groupby(['Season', 'Primary Type']).size().unstack().fillna(0)

crime_type_seasonal.plot(kind='bar', stacked=True, figsize=(14, 7), colormap='tab20')
plt.title('Seasonal Trends of Different Crime Types')
plt.xlabel('Season')
plt.ylabel('Number of Crimes')
plt.xticks(rotation=0)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.show()

location_counts = df['Block'].value_counts()

plt.figure(figsize=(14, 7))
location_counts[:20].plot(kind='bar', color='purple')
plt.title('Top 20 Crime Locations')
plt.xlabel('Block')
plt.ylabel('Number of Crimes')
plt.xticks(rotation=90)
plt.grid(True)
plt.show()

if 'Offender ID' in df.columns:
    offender_counts = df.groupby('Offender ID').size()
    repeat_offenders = offender_counts[offender_counts > 1]
    recidivism_rate = len(repeat_offenders) / len(offender_counts)
    print(f'Recidivism Rate: {recidivism_rate:.2%}')

    plt.figure(figsize=(10, 5))
    offender_counts[offender_counts > 1].hist(bins=range(1, 11), color='teal', edgecolor='black')
    plt.title('Distribution of Offenses Per Offender')
    plt.xlabel('Number of Offenses')
    plt.ylabel('Number of Offenders')
    plt.grid(True)
    plt.show()
else:
    print("Recidivism analysis requires 'Offender ID' data, which is not available in the current dataset.")

# Data Preprocessing

#print("Before preprocessing the data")
#print(df.isnull().sum())

columns_to_drop = ['X Coordinate', 'Y Coordinate', 'Location Description', 'Location', 'Updated On', 'ID', 'Case Number', 'Description']
df = df.drop(columns = columns_to_drop)

columns_to_fill_w_median = ['Latitude', 'Longitude', 'Ward', 'Community Area']
imputer = SimpleImputer(strategy='median')
df_imputed = imputer.fit_transform(df[columns_to_fill_w_median])
df_imputed = pd.DataFrame(df_imputed, columns=columns_to_fill_w_median)
df_modified = df.drop(columns=columns_to_fill_w_median)
df = pd.concat([df_imputed, df_modified ], axis=1)
df.to_csv('crime_data.csv', index=False)

#print("\nAfter preprocessing the data")
#print(df.isnull().sum())

# Developing the model for predicting future crime incidents based on historical data, time, location, and other relevant factors

df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y %H:%M')
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day
df['Hour'] = df['Date'].dt.hour
df['DayOfWeek'] = df['Date'].dt.dayofweek
df['WeekOfYear'] = df['Date'].dt.isocalendar().week
df['Block'] = df['Block'].astype('category').cat.codes
df['Primary Type'] = df['Primary Type'].astype('category').cat.codes
df['IUCR'] = df['IUCR'].astype('category').cat.codes
df['FBI Code'] = df['FBI Code'].astype('category').cat.codes

X1 = df[['Year', 'Month', 'Day', 'Hour', 'DayOfWeek', 'Latitude', 'Longitude', 'Block', 'Beat', 'District', 'Ward', 'Community Area', 'Arrest', 'Domestic', 'IUCR', 'FBI Code']]
y1 = df['Primary Type']

X_train1, X_test1, y_train1, y_test1 = train_test_split(X1, y1, test_size=0.2, random_state=42)

models = {
    "Linear Regression": LinearRegression(),
    "Decision Tree Regressor": DecisionTreeRegressor(),
    "Random Forest Regressor": RandomForestRegressor(),
    "Gradient Boosting Regressor": GradientBoostingRegressor(),
    "XGBoost Regressor": XGBRegressor(),
    "KNeighbors Regressor": KNeighborsRegressor()
}

print("Model for predicting future crime incidents based on historical data, time, location, and other relevant factors")
for name, model in models.items():
    model.fit(X_train1, y_train1)
    y_pred1 = model.predict(X_test1)
    mse1 = mean_squared_error(y_test1, y_pred1)
    rmse1 = mse1 ** 0.5
    r2_1 = r2_score(y_test1, y_pred1)
    print(f"Model: {name}")
    print(f"Root Mean Squared Error (RMSE): {rmse1}")
    print(f"R2 Score: {r2_1}")
    print("----------")

# Initializing the Dash app

app = dash.Dash(__name__)

fig = px.bar(crime_by_district, x=crime_by_district.index, y=crime_by_district.values, labels={'x': 'District', 'y': 'Number of Crimes'}, title='Crime Rates by District')

app.layout = html.Div(children=[
    html.H1(children='Chicago Crime Data Dashboard'),
    dcc.Graph(
        id='crime-by-district',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)

'''
df['Crime Count'] = 1
#grouped_data = df.groupby(['Year', 'Month', 'Day', 'Hour', 'DayOfWeek', 'WeekOfYear', 'Latitude', 'Longitude']).agg({'Crime Count': 'sum'}).reset_index()
grouped_data = df.groupby(['Year', 'Month', 'Day', 'Hour', 'DayOfWeek', 'WeekOfYear', 'Latitude', 'Longitude']).size().reset_index(name='CrimeCount')
grouped_data['LogCrimeCount'] = np.log1p(grouped_data['Crime Count'])

X2 = grouped_data[['Year', 'Month', 'Day', 'Hour', 'DayOfWeek', 'WeekOfYear', 'Latitude', 'Longitude']]
#y2 = grouped_data['Crime Count']
y2 = grouped_data['LogCrimeCount']

X_train2, X_test2, y_train2, y_test2 = train_test_split(X2, y2, test_size=0.2, random_state=42)

print("\nModel for assessing the risk of different areas and times for specific types of crimes to help in resource allocation for law enforcement")
for name, model in models.items():
    model.fit(X_train2, y_train2)
    y_pred2 = model.predict(X_test2)
    mse2 = mean_squared_error(y_test2, y_pred2)
    rmse2 = mse2 ** 0.5
    r2_2 = r2_score(y_test2, y_pred2)
    print(f"Model: {name}")
    print(f"Root Mean Squared Error (RMSE): {rmse2}")
    print(f"R2 Score: {r2_2}")
    print("----------")
'''