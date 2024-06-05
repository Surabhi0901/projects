# How to run this: dtale-streamlit run c:/your-path/your-script.py

# Importing necessary libraries

import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
# from xgboost import XGBRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
# from xgboost import XGBClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
import matplotlib.pyplot as plt
from dtale.views import startup
from dtale.app import get_instance
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, mean_absolute_error, mean_squared_error, r2_score
from sklearn.naive_bayes import GaussianNB
import streamlit as st
from streamlit_option_menu import option_menu
from sklearn.impute import SimpleImputer
from dtale.views import startup
from dtale.app import get_instance
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import IsolationForest
from scipy.stats import skew, boxcox
from scipy.special import boxcox1p
import re
import pickle

# Initializing the session state

if 'df' not in st.session_state:
    st.session_state.df = None

if 'df_imputed_numeric' not in st.session_state:
    st.session_state.df_imputed_numeric = None

if 'data' not in st.session_state:
    st.session_state.data = None

# Setting up dtale

def save_to_dtale(df):
    startup(data_id="1", data=df)

def retrieve_from_dtale():
    return get_instance("1").data

# Setting up the page

st.set_page_config(page_title= "Copper Industry Data Modeling| By Surabhi Yadav",
                   page_icon= ":🏭:", 
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This app is created by *Surabhi Yadav!*"""})

with st.sidebar:
    selected = option_menu('MENU', ["Upload & Read","Data Preprocessing", "EDA", "Feature Engineering", "Model Development & Evaluation"], 
                           icons=["upload", "funnel-fill", "bar-chart-line-fill", "gear-fill", "search"], 
                           menu_icon="menu-up",
                           default_index=0,
                           orientation="vertical",
                           styles={"nav-link": {"font-size": "15px", "text-align": "centre", "margin": "0px", 
                                                "--hover-color": "#B87333"},
                                   "icon": {"font-size": "15px"},
                                   "container" : {"max-width": "6000px"},
                                   "nav-link-selected": {"background-color": "#B87333"}})
    

# Uploading and reading the data file 

if selected == "Upload & Read":

    st.header("File Upload and Display", divider='orange')

    st.subheader("Upload the dataset below")
    uploaded_file = st.file_uploader("Choose a CSV file", accept_multiple_files=False)
    show = st.button("Show the file uploaded", use_container_width=True)
    if show:
        st.session_state.df = pd.read_csv(uploaded_file)
        st.write("Filename:", uploaded_file.name)
        st.dataframe(st.session_state.df)

# Data Preprocessing

if selected == "Data Preprocessing":

    st.header("Data Preprocessing", divider='orange')

    #st.session_state.df.dropna()
    
    st.subheader("Before dealing with the null values")
    st.write("")
    st.write("")
    st.write(st.session_state.df.isnull().sum())

    #Removing null values or filling them out
    st.session_state.df['material_ref'].replace('00000', np.nan, inplace=True)
    numeric_columns = st.session_state.df.select_dtypes(include=['number']).columns.tolist()
    imputer = SimpleImputer(strategy='median')
    st.session_state.df_imputed_numeric = imputer.fit_transform(st.session_state.df[numeric_columns])
    st.session_state.df_imputed_numeric = pd.DataFrame(st.session_state.df_imputed_numeric, columns=numeric_columns)
    st.session_state.data = pd.concat([st.session_state.df_imputed_numeric, st.session_state.df.select_dtypes(exclude=['number'])], axis=1)

    categorical_columns = st.session_state.data.select_dtypes(include=['object']).columns.tolist()
    categorical_columns.remove('status')
    categorical_columns.remove('quantity tons')
    categorical_columns.remove('id')
    categorical_columns.remove('material_ref')

    #Treating outliers using Isolation Forest
    numerical_columns = st.session_state.data.select_dtypes(include=['number']).columns.tolist()
    numerical_columns.remove('item_date')
    numerical_columns.remove('delivery date')
    numerical_columns.remove('customer')
    numerical_columns.remove('country')
    numerical_columns.remove('application')
    numerical_columns.remove('selling_price')
    numerical_columns.remove('product_ref')
    iso = IsolationForest(contamination=0.1)
    yhat = iso.fit_predict(st.session_state.data[numerical_columns])
    mask = yhat != -1
    st.session_state.data = st.session_state.data[mask]

    #Checking skewness and apply transformations
    skewed_features = st.session_state.data[numerical_columns].apply(lambda x: skew(x.dropna())).sort_values(ascending=False)
    high_skew = skewed_features[abs(skewed_features) > 0.75]
    skewed_columns = high_skew.index

    for col in categorical_columns:
        top_categories = st.session_state.data[col].value_counts().nlargest(10).index
        st.session_state.data[col] = np.where(st.session_state.data[col].isin(top_categories), st.session_state.data[col], 'Other')

    label_encoders = {}
    for col in categorical_columns:
        label_encoders[col] = LabelEncoder()
        st.session_state.data[col] = label_encoders[col].fit_transform(st.session_state.data[col].astype(str))
     
    #Scaling numerical features
    scaler = StandardScaler()
    st.session_state.data[numerical_columns] = scaler.fit_transform(st.session_state.data[numerical_columns])

    if 'status' in st.session_state.data.columns:
        st.session_state.data = st.session_state.data.dropna(subset=['status'])
        #pattern = re.compile(r'Draft|Not lost for AM|Offerable|Offered|Revised|To be approved|Wonderful')
        #st.session_state.data = st.session_state.data[~st.session_state.data['status'].astype(str).str.contains(pattern, na=False)]
        st.session_state.data = st.session_state.data[st.session_state.data['status'].isin(['Won', 'Lost'])]
    
    if 'quantity tons' in st.session_state.data.columns:
        st.session_state.data = st.session_state.data[~st.session_state.data['quantity tons'].astype(str).str.contains('e', na=False)]
        
    if 'item_date' in st.session_state.data.columns:
        st.session_state.data = st.session_state.data[~st.session_state.data['item_date'].astype(str).str.contains('19950000.0', na=False)]
        st.session_state.data = st.session_state.data[~st.session_state.data['item_date'].astype(str).str.contains('20191919.0', na=False)]
        st.session_state.data = st.session_state.data[~st.session_state.data['item_date'].astype(str).str.contains('30310101.0', na=False)]
        
    if 'delivery date' in st.session_state.data.columns:
        st.session_state.data = st.session_state.data[~st.session_state.data['delivery date'].astype(str).str.contains('30310101.0', na=False)]
        st.session_state.data = st.session_state.data[~st.session_state.data['delivery date'].astype(str).str.contains('20212222.0', na=False)]
        
    
    st.session_state.data = pd.DataFrame(st.session_state.data)

    #Identifying columns to convert to numeric type
    columns_to_convert = ['quantity tons']

    for col in columns_to_convert:
        if col in st.session_state.data.columns:
            st.session_state.data[col] = pd.to_numeric(st.session_state.data[col], errors='coerce')
    
    st.subheader("After dealing with the null values")
    st.write("")
    st.write("")
    st.write(st.session_state.data.isnull().sum())
    #st.dataframe(st.session_state.data)

    # st.session_state.data.to_csv(r'C:\Users\sy090\Downloads\PROJECTS\copper_industry_data_modeling\preprocessed_data.csv', index=False)
    # st.session_state.data.to_csv(r'C:\Users\SAMEER YADAV\Downloads\Surabhi\copper_industry_data_modeling\preprocessed_data.csv', index=False)

# EDA

if selected == "EDA":

    st.header("EDA", divider='orange')

    st.subheader("Click on the button below to view general EDA")
    gen_eda = st.button("General EDA", use_container_width=True)
    if gen_eda:
        
        #Histogram and Boxplot: For exploring skewness and outliers respectively

        #Plotting the histogram of numerical columns
        st.write("")
        st.markdown("**Histogram Plots**")
        raw_numerical_columns = st.session_state.data.select_dtypes(include=['number']).columns.tolist()
        columns_to_drop = ['item_date', 'customer', 'country', 'product_ref', 'delivery date', 'id', 'material_ref']
        numerical_columns = [column for column in raw_numerical_columns if column not in columns_to_drop]

        nc_df = st.session_state.data.drop(columns=['item_date', 'customer', 'country', 'product_ref', 'delivery date', 'id', 'material_ref'])
        num_plots = len(numerical_columns)
        num_cols = min(num_plots, 3)  
        num_rows = (num_plots - 1) // num_cols + 1 if num_plots > 1 else 1 

        plt.figure() 
        fig1, axes = plt.subplots(num_rows, num_cols, figsize=(15, 5*num_rows))

        if num_plots > 1:
            axes = axes.flatten()
        else:
            axes = [axes]

        for i, col in enumerate(numerical_columns):
            sns.histplot(nc_df[col], ax=axes[i], kde=True, bins=20)  # Adjust bins as needed
            # axes[i].set_title(col)

        for i in range(num_plots, num_rows * num_cols):
            fig1.delaxes(axes[i])

        plt.tight_layout()

        st.pyplot(fig1)

        #Plotting the boxplots of numerical columns
        st.write("")
        st.markdown("**Boxplots**")
        raw_numerical_columns = st.session_state.data.select_dtypes(include=['number']).columns.tolist()
        columns_to_drop = ['item_date', 'customer', 'country', 'product_ref', 'delivery date', 'id', 'material_ref']
        numerical_columns = [column for column in raw_numerical_columns if column not in columns_to_drop]

        nc_df = st.session_state.data.drop(columns=['item_date', 'customer', 'country', 'product_ref', 'delivery date', 'id', 'material_ref'])
        num_plots = len(numerical_columns)
        num_cols = min(num_plots, 3)  
        num_rows = (num_plots - 1) // num_cols + 1 if num_plots > 1 else 1 

        plt.figure()
        fig2, axes = plt.subplots(num_rows, num_cols, figsize=(15, 5*num_rows))

        if num_plots > 1:
            axes = axes.flatten()
        else:
            axes = [axes]
            
        for i, col in enumerate(numerical_columns):
                    sns.boxplot(data=nc_df[col], ax=axes[i])
                    # axes[i].set_title(col)

        for i in range(num_plots, num_rows * num_cols):
            fig2.delaxes(axes[i])

        plt.tight_layout()

        st.pyplot(fig2)

        #Heatmap
        st.write("")
        st.markdown("**Heatmap**")
        raw_numerical_columns = st.session_state.data.select_dtypes(include=['number']).columns.tolist()
        columns_to_drop = ['item_date', 'customer', 'country', 'product_ref', 'delivery date', 'id', 'material_ref']
        numerical_columns = [column for column in raw_numerical_columns if column not in columns_to_drop]
        numeric_df = st.session_state.data[numerical_columns]
        corr_matrix = numeric_df.corr()
        plt.figure(figsize=(10, 8))
        mask = np.triu(np.ones_like(corr_matrix))
        sns.heatmap(corr_matrix, annot=True, fmt=".2f", mask = mask)
        plt.title('Correlation Heatmap')
        plt.xlabel('Features')
        plt.ylabel('Features')
        st.pyplot(plt)

        col1,col2 = st.columns(2)

        #Piechart
        with col1:
            st.write("")
            st.markdown("**Piechart**")
            columns_to_visualize = ['country', 'status', 'item type']

            for col in columns_to_visualize:
                st.write(f"Pie Chart of {col}")
                fig, ax = plt.subplots(figsize=(10, 6))
                x = st.session_state.data[col].unique()
                y = st.session_state.data[col].value_counts()
                porcent = 100.*y/y.sum()

                patches, texts = plt.pie(y, startangle=90)
                labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(x, porcent)]

                sort_legend = True
                if sort_legend:
                    patches, labels, dummy =  zip(*sorted(zip(patches, labels, y),
                                                        key=lambda x: x[2],
                                                        reverse=True))

                ax.legend(patches, labels, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1), title=col)
                st.pyplot(fig)
        
        # Count plots
        with col2:
            st.write("")
            st.markdown("**Count Plots**")
            columns_to_visualize = ['country', 'status', 'item type']   

            for col in columns_to_visualize:
                st.write(f"Count Plot of {col}")
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.countplot(y=col, data=st.session_state.data, order=st.session_state.data[col].value_counts().index, ax=ax)
                ax.set_xlabel('Count')
                ax.set_ylabel(col)
                ax.legend(loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
                st.pyplot(fig)

    #Automated EDA
    st.write("")
    st.write("")
    st.subheader("Click on the button below to view automated EDA")
    auto_eda = st.button("Automated EDA", use_container_width=True)
    if auto_eda:
        st.markdown("**Interactive dashboard (D-Tale)**")
        save_to_dtale(st.session_state.data)
        st.markdown('<iframe src="/dtale/main/1" width="1000" height="600"></iframe>', unsafe_allow_html=True)
        st.markdown('<a href="/dtale/main/1" target="_blank">Open D-Tale</a>', unsafe_allow_html=True)
        
# Feature Engineering

if selected == "Feature Engineering":
    
    st.header("Feature Engineering", divider = 'orange')
    
    #Creating new feature
    st.session_state.data['item_date'] = pd.to_datetime(st.session_state.data['item_date'].astype(str), format='%Y%m%d.0')
    st.session_state.data['delivery date'] = pd.to_datetime(st.session_state.data['delivery date'].astype(str), format='%Y%m%d.0')

    st.session_state.data['item_year'] = st.session_state.data['item_date'].dt.year
    st.session_state.data['item_month'] = st.session_state.data['item_date'].dt.month
    st.session_state.data['item_day'] = st.session_state.data['item_date'].dt.day
    
    st.session_state.data['delivery_year'] = st.session_state.data['delivery date'].dt.year
    st.session_state.data['delivery_month'] = st.session_state.data['delivery date'].dt.month
    st.session_state.data['delivery_day'] = st.session_state.data['delivery date'].dt.day

    st.session_state.data['delivery_time_days'] = (st.session_state.data['delivery date'] - st.session_state.data['item_date']).dt.days
    st.session_state.data.drop(columns=['item_date', 'delivery date', 'item_year', 'item_month', 'item_day', 'delivery_year', 'delivery_month', 'delivery_day'], inplace=True)
    st.session_state.data['delivery_time_days'] = st.session_state.data['delivery_time_days'].abs()
    #st.dataframe(st.session_state.data)
    
    #Dropping irrelevant columns
    st.session_state.data.drop(columns=['id', 'material_ref'], axis=1, inplace=True)
    
    st.write("")
    st.write("")
    st.subheader("Display of the dataset after preprocessing and feature engineering")
    st.dataframe(st.session_state.data)

    #st.session_state.data.to_csv(r'C:\Users\sy090\Downloads\PROJECTS\copper_industry_data_modeling\preprocessed_data.csv', index=False)
    #st.session_state.data.to_csv(r'C:\Users\SAMEER YADAV\Downloads\Surabhi\copper_industry_data_modeling\preprocessed_data.csv', index=False)

# Model Development & Evaluation

if selected == "Model Development & Evaluation":

    st.header("Model Development & Evaluation", divider = 'orange')

    # Load the scaler
    with open('C:/Users/sy090/Downloads/PROJECTS/copper_industry_data_modeling/scaler_r.pkl', 'rb') as f:
        scaler_r = pickle.load(f)
    with open('C:/Users/sy090/Downloads/PROJECTS/copper_industry_data_modeling/scaler_c.pkl', 'rb') as f:
        scaler_c = pickle.load(f)

    #Loading regression models
    regression_models = {}
    for model_name in ["linear", "decision_tree", "random_forest", 
                    "gradient_boosting", "xgboost", "kneighbors"]:
        with open(f'C:/Users/sy090/Downloads/PROJECTS/copper_industry_data_modeling/{model_name}_regressor.pkl', 'rb') as f:
            regression_models[model_name] = pickle.load(f)

    #Loading classification models
    classification_models = {}
    for model_name in ["logistic_regression", "decision_tree", "random_forest", 
                    "xgboost", "knn", "naive_bayes"]:
        with open(f'C:/Users/sy090/Downloads/PROJECTS/copper_industry_data_modeling/{model_name}_classifier.pkl', 'rb') as f:
            classification_models[model_name] = pickle.load(f)

    # Task selection
    task = st.selectbox('Select Task', ['Regression', 'Classification'])

    # Input fields
    if task == 'Regression':
        # Model selection
        reg_model_name = st.selectbox('Select Regression Model', list(regression_models.keys()))
        regressor = regression_models[reg_model_name]

        # Collect input values for regression
        X_reg = st.session_state.data.drop(columns=['selling_price', 'customer', 'product_ref', 'status'])
        y_reg = st.session_state.data['selling_price']
        inputs_r = {}
        for col in X_reg.columns:
            inputs_r[col] = st.text_input(f'Enter value for {col}')
        
        # Predict selling price
        if st.button('Predict Selling Price'):
            input_df_r = pd.DataFrame([inputs_r])
            input_df_r = input_df_r.apply(pd.to_numeric, errors='ignore')
            input_df_r = scaler_r.transform(input_df_r)
            prediction = regressor.predict(input_df_r)
            st.write(f'Predicted Selling Price: {prediction[0]}')

    elif task == 'Classification':
        # Model selection
        cls_model_name = st.selectbox('Select Classification Model', list(classification_models.keys()))
        classifier = classification_models[cls_model_name]

        # Collect input values for classification
        # st.session_state.data[st.session_state.data['status'].isin(['WON', 'LOST'])]
        X_cls = st.session_state.data.drop(columns=['status', 'customer', 'thickness', 'width'])
        y_cls = st.session_state.data['status'].map({'Won': 1, 'Lost': 0})
        inputs_c = {}
        for col in X_cls.columns:
            inputs_c[col] = st.text_input(f'Enter value for {col}')
        
        # Predict status
        if st.button('Predict Status'):
            input_df_c = pd.DataFrame([inputs_c])
            input_df_c = input_df_c.apply(pd.to_numeric, errors='ignore')
            input_df_c = scaler_c.transform(input_df_c)
            prediction = classifier.predict(input_df_c)
            st.write('Predicted Status: Won' if prediction[0] == 1 else 'Predicted Status: Lost')    