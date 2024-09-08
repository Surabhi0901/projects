# Chicago Crime Data Analysis

## Project Overview

This project aims to analyze crime data in Chicago to identify patterns, trends, and hotspots, supporting strategic decision-making for law enforcement. By leveraging historical and recent crime data, we aim to provide actionable insights to improve resource allocation, reduce crime rates, and enhance public safety in Chicago.

## Dataset Description

The dataset contains records of reported crimes in Chicago, including:

- **ID**: Unique identifier for each crime incident.
- **Case Number**: Unique case number assigned to each incident.
- **Date**: Date and time when the crime occurred.
- **Block**: Block where the crime occurred.
- **IUCR**: Illinois Uniform Crime Reporting code assigned to the crime type.
- **Primary Type**: Primary classification of the crime.
- **Description**: Detailed description of the crime.
- **Location Description**: Description of the location where the crime occurred.
- **Arrest**: Indicates whether an arrest was made (TRUE/FALSE).
- **Domestic**: Indicates whether the crime was domestic-related (TRUE/FALSE).
- **Beat**: Police beat where the crime occurred.
- **District**: Police district where the crime occurred.
- **Ward**: Ward where the crime occurred.
- **Community Area**: Community area where the crime occurred.
- **FBI Code**: FBI code classification for the crime.
- **X Coordinate**: X coordinate of the crime location.
- **Y Coordinate**: Y coordinate of the crime location.
- **Year**: Year when the crime was reported.
- **Updated On**: Date when the record was last updated.
- **Latitude**: Latitude of the crime location.
- **Longitude**: Longitude of the crime location.
- **Location**: Combined latitude and longitude in a string format.

## Goals and Analysis

### Temporal Analysis

1. **Crime Trends Over Time**: Plot the number of crimes per year to identify trends.
2. **Peak Crime Hours**: Determine the times of day when crimes are most frequently reported.

### Geospatial Analysis

1. **Crime Hotspots**: Identify areas with high concentrations of crimes using heatmaps.
2. **District/Ward Analysis**: Compare crime rates across different districts and wards.

### Crime Type Analysis

1. **Distribution of Crime Types**: Analyze the frequency of different crime types.
2. **Severity Analysis**: Investigate the distribution of severe crimes versus less severe crimes.

### Arrest and Domestic Incident Analysis

1. **Arrest Rates**: Calculate the percentage of crimes that result in an arrest.
2. **Domestic vs. Non-Domestic Crimes**: Compare the characteristics and frequencies of domestic-related incidents versus non-domestic incidents.

### Location-Specific Analysis

1. **Location Description Analysis**: Investigate the most common locations for crimes.
2. **Comparison by Beat and Community Area**: Analyze crime data by beat and community area to identify localized crime patterns.

### Seasonal and Weather Impact

1. **Seasonal Trends**: Examine whether certain types of crimes are more prevalent in specific seasons.

### Repeat Offenders and Recidivism

1. **Repeat Crime Locations**: Identify locations that are repeatedly associated with criminal activity.
2. **Recidivism Rates**: Analyze recidivism rates if data on repeat offenders is available.

### Predictive Modeling and Risk Assessment

1. **Predictive Analysis**: Develop models to predict future crime incidents based on historical data, time, location, and other relevant factors.
2. **Risk Assessment**: Assess the risk of different areas and times for specific types of crimes to help in resource allocation for law enforcement.

### Visualization and Reporting

1. **Interactive Dashboards**: Create interactive dashboards to dynamically visualize and explore the data.
2. **Detailed Crime Reports**: Generate detailed reports highlighting key trends, hotspots, and critical insights.

## Code and Instructions

### Libraries Used

```python
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
