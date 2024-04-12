#!/usr/bin/env python
# coding: utf-8
# How to run this: dtale-streamlit run c:/your-path/your-script.py

# # Making a generalized ML Model where the best algorithm will be selected for the given dataset

#Importing the libraries

import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
import matplotlib.pyplot as plt
from ydata_profiling import ProfileReport
import dtale
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, mean_absolute_error, mean_squared_error, r2_score
from sklearn.naive_bayes import GaussianNB
import streamlit as st
from streamlit_option_menu import option_menu
from sklearn.impute import SimpleImputer
from dtale.views import startup
from dtale.app import get_instance

#Initializing the session state
if 'df' not in st.session_state:
    st.session_state.df = None

if 'target_column' not in st.session_state:
    st.session_state.target_column = None

if 'list_of_feature_columns' not in st.session_state:
    st.session_state.list_of_feature_columns = None

#Setting up dtale

def save_to_dtale(df):
    startup(data_id="1", data=df)

def retrieve_from_dtale():
    return get_instance("1").data

#Setting up the page

st.set_page_config(page_title= " Best Algorithm Selection| By Surabhi Yadav",
                   page_icon= ":robot:", 
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This app is created by *Surabhi Yadav!*"""})

with st.sidebar:
    selected = option_menu('MENU', ["Data Upload", "Automated EDA", "Missing Value Analysis", 
                                    "Obj to Num", "Boxplot Analysis", "Outlier Handling", 
                                    "Target Selection", "Main Algorithm"], 
                           icons=["cloud-arrow-up-fill", "hypnotize", "question-circle-fill", "repeat", 
                                  "bar-chart-line-fill", "exclamation-triangle-fill", 
                                  "bullseye", "hourglass-top"], 
                           menu_icon="menu-up",
                           default_index=0,
                           orientation="vertical",
                           styles={"nav-link": {"font-size": "15px", "text-align": "centre", "margin": "0px", 
                                                "--hover-color": "#00FFFF"},
                                   "icon": {"font-size": "15px"},
                                   "container" : {"max-width": "6000px"},
                                   "nav-link-selected": {"background-color": "##00FFFF"}})


#Collecting the data and generalising the code body to read any type of file

if selected == "Data Upload":

    st.header("Data Upload")

    def get_supported_read_functions():
        supported_read_functions = [getattr(pd, f) for f in dir(pd) if f.startswith('read_') and callable(getattr(pd, f))]
        supported_read_functions = [func for func in supported_read_functions if func.__name__ != 'read_clipboard']
        return supported_read_functions

    def read_any_format(data_file):
        supported_read_functions = get_supported_read_functions()

        for read_func in supported_read_functions:
            try:
                st.session_state.df = read_func(data_file)
                return st.session_state.df
            except Exception as e:
                continue
        return None

    data_file = st.file_uploader(label="File with any extension can be uploaded", type = None, label_visibility="visible")
    if data_file is not None:
        st.session_state.df = read_any_format(data_file)

    show_table = st.button("Show the dataset stored")
    if show_table:
        st.dataframe(st.session_state.df)
        startup(data_id="1", data=st.session_state.df)

#Showing the automated EDA

if selected == "Automated EDA":

    st.header("Showing the automated EDA done on the uploaded dataset")
    save_to_dtale(st.session_state.df)
    st.markdown('<iframe src="/dtale/main/1" width="1000" height="600"></iframe>', unsafe_allow_html=True)
    st.markdown('<a href="/dtale/main/1" target="_blank">Open D-Tale</a>', unsafe_allow_html=True)

#Missing value analysis

if selected == "Missing Value Analysis":
    
    st.header("Missing Value Analysis")
    #Checking for null values
    st.subheader("Before the missing value analysis")
    st.write(st.session_state.df.isnull().sum())


    #Removing null values or filling them out
    numeric_columns = st.session_state.df.select_dtypes(include=['number']).columns
    imputer = SimpleImputer(strategy='mean')
    df_imputed_numeric = imputer.fit_transform(st.session_state.df[numeric_columns])
    df_imputed_numeric = pd.DataFrame(df_imputed_numeric, columns=numeric_columns)
    st.session_state.df = pd.concat([df_imputed_numeric, st.session_state.df.select_dtypes(exclude=['number'])], axis=1)

    st.subheader("After the missing value analysis")
    st.write(st.session_state.df.isnull().sum())

#Converting a categorical column to numerical because it is one of the feature column

if selected == "Obj to Num":

    st.header("Converting a categorical column to numerical because it is one of the feature column")
    def convert_categorical_to_numerical(df, columns):
        for col in columns:
            df[col] = pd.factorize(df[col])[0]
        return df

    columns_to_convert_input = st.text_input("**Enter the name(s) of the column(s) that you need to convert [comma separated]**") #Can pass multiple values
    columns_to_convert = [col.strip() for col in columns_to_convert_input.split(",")]
    convert = st.button("Convert")
    if convert:
        st.session_state.df = convert_categorical_to_numerical(st.session_state.df, columns_to_convert)
        st.write(st.session_state.df)


#Plotting box plots to visualize the outliers
#Can't generalize this as it is upto a human to decide for what to exactly take as a feature

if selected == "Boxplot Analysis":
    st.header("Plotting box plots to visualize the outliers")

    list_of_feature_columns_input = st.text_input("**Enter the name(s) of the column(s) that you want as features [comma separated]**") #Can pass multiple values
    st.session_state.list_of_feature_columns = [col.strip() for col in list_of_feature_columns_input.split(",")]
    #list_of_feature_columns = ['Annual_Income', 'Monthly_Inhand_Salary', 'Num_Bank_Accounts', 'Num_Credit_Card', 'Interest_Rate', 'Num_of_Loan', 'Delay_from_due_date', 'Num_of_Delayed_Payment', 'Credit_Mix', 'Outstanding_Debt', 'Credit_History_Age', 'Monthly_Balance']
    #Annual_Income, Monthly_Inhand_Salary, Num_Bank_Accounts, Num_Credit_Card, Interest_Rate, Num_of_Loan, Delay_from_due_date, Num_of_Delayed_Payment, Credit_Mix, Outstanding_Debt, Credit_History_Age, Monthly_Balance
    plot = st.button("Plot")
    if plot:
        # Calculate the number of rows and columns for subplots
        num_plots = len(st.session_state.list_of_feature_columns)
        num_cols = min(num_plots, 3)  # Number of columns for subplots
        num_rows = (num_plots - 1) // num_cols + 1 if num_plots > 1 else 1  # Number of rows for subplots

        # Create a figure and axis objects
        fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 5*num_rows))

        # Flatten axes if necessary
        if num_plots > 1:
            axes = axes.flatten()
        else:
            axes = [axes]

        # Loop through each column and plot boxplot
        for i, col in enumerate(st.session_state.list_of_feature_columns):
            data = pd.DataFrame(st.session_state.df[col], columns=[col])
            sns.boxplot(data=data, ax=axes[i])
            axes[i].set_title(col)

        # Remove any unused subplots
        for i in range(num_plots, num_rows * num_cols):
            fig.delaxes(axes[i])

        # Adjust layout
        plt.tight_layout()

        # Show plots
        st.pyplot(fig)
    
#Filtering out columns which have outliers based on IQR method

if selected == "Outlier Handling":

    st.header("Filtering out columns which have outliers based on IQR method")

    def filter_col(df, columns):
        for col in columns:
            q1 = np.percentile(df[col], 25)
            q3 = np.percentile(df[col], 75)
            IQR = q3-q1
            lwr_bound = q1-(1.5*IQR)
            upr_bound = q3+(1.5*IQR)
            df = df[(df[col] > lwr_bound) & (df[col] < upr_bound)]
        return df
    
    list_of_feature_columns_input = st.text_input("**Enter the name(s) of the column(s) that you want as features [comma separated]**") #Can pass multiple values
    st.session_state.list_of_feature_columns = [col.strip() for col in list_of_feature_columns_input.split(",")]
    #list_of_feature_columns = ['Annual_Income', 'Monthly_Inhand_Salary', 'Num_Bank_Accounts', 'Num_Credit_Card', 'Interest_Rate', 'Num_of_Loan', 'Delay_from_due_date', 'Num_of_Delayed_Payment', 'Credit_Mix', 'Outstanding_Debt', 'Credit_History_Age', 'Monthly_Balance']
    #Annual_Income, Monthly_Inhand_Salary, Num_Bank_Accounts, Num_Credit_Card, Interest_Rate, Num_of_Loan, Delay_from_due_date, Num_of_Delayed_Payment, Credit_Mix, Outstanding_Debt, Credit_History_Age, Monthly_Balance
    handle = st.button("Handle")
    if handle:
        st.session_state.df = filter_col(st.session_state.df, st.session_state.list_of_feature_columns)
        st.dataframe(st.session_state.df)

#Taking the target column from the user

if selected == "Target Selection":

    st.header("Target Selection")
    target_column = st.text_input('**Enter the name of the target column as your_data_frame["your_column"]**')
    target = f"st.session_state.df['{target_column}']"

    submit = st.button('Submit')
    if submit:
        st.session_state.target_column = eval(target)

#Best Algorithm Selection

if selected == "Main Algorithm":

    st.header("Best Algorithm Selection")
    
    #Regression
    if isinstance(st.session_state.target_column, pd.Series) and st.session_state.target_column.dtype.kind in ['i', 'u', 'f']:
        st.write('Choosing regression models to proceed with')
        feature_column = st.session_state.df[st.session_state.list_of_feature_columns]
        target_column = st.session_state.target_column
        train_feature, test_feature, train_target, test_target = train_test_split(feature_column, target_column, random_state=42)
        correlations = feature_column.corrwith(target_column)
        correlation_threshold = 0.7
        is_linear = any(correlations.abs() >= correlation_threshold)
        
        if is_linear:
            st.write("The data is linear and continuous.")
            polynomial = PolynomialFeatures(degree=3)
            train_feature_poly = polynomial.fit_transform(train_feature)
            test_feature_poly = polynomial.transform(test_feature)
            num_curves = train_feature_poly.shape[1] - 1

            if num_curves == 0:
                st.write("Choosing Linear Regression")
                model = LinearRegression()
                model.fit(train_feature_poly, train_target)
                train_score = model.score(train_feature_poly, train_target)
                test_score = model.score(test_feature_poly, test_target)
                st.write("Train Score:", train_score)
                st.write("Test Score:", test_score)
                
            elif num_curves <= 3: 
                st.write("Choosing Polynomial Regression")
                model = make_pipeline(PolynomialFeatures(degree=3), LinearRegression())
                model.fit(train_feature_poly, train_target)
                train_score = model.score(train_feature_poly, train_target)
                test_score = model.score(test_feature_poly, test_target)
                st.write("Train Score:", train_score)
                st.write("Test Score:", test_score) 
                
            else:
                st.write("Choosing Ridge Regression")
                model = Ridge(alpha=1.0)

                st.write("Fitting Ridge Regression")
                model.fit(train_feature_poly, train_target)
                train_score = model.score(train_feature_poly, train_target)
                test_score = model.score(test_feature_poly, test_target)
                st.write("Train Score:", train_score)
                st.write("Test Score:", test_score)

                if train_score < 0.8 or test_score < 0.8:
                    st.write("Switching to Lasso Regression")
                    model = Lasso(alpha=1.0)
                    model.fit(train_feature_poly, train_target)
                    train_score = model.score(train_feature_poly, train_target)
                    test_score = model.score(test_feature_poly, test_target)
                    st.write("Train Score:", train_score)
                    st.write("Test Score:", test_score)

                    if train_score < 0.8 or test_score < 0.8:
                        st.write("Switching to Elastic Net Regression")
                        model = ElasticNet(alpha=1.0, l1_ratio=0.5)
                        model.fit(train_feature_poly, train_target)
                        train_score = model.score(train_feature_poly, train_target)
                        test_score = model.score(test_feature_poly, test_target)
                        st.write("Train Score:", train_score)
                        st.write("Test Score:", test_score)

        else:
            st.write("The data is non-linear and non-continuous")
            models = [
                DecisionTreeRegressor(),
                RandomForestRegressor(),
                GradientBoostingRegressor(),
                XGBRegressor(),
                KNeighborsRegressor(),
                SVR()
            ]
            
            mae = []
            mse = []
            rmse = []
            r2 = []
            model_names = ['DecisionTreeRegressor', 'RandomForestRegressor', 'GradientBoostingRegressor', 
                        'XGBRegressor', 'KNeighborsRegressor', 'SVR']
            index = ['mae', 'mse', 'rmse', 'r2']

            for model in models:
                model.fit(train_feature, train_target)
                train_score = model.score(train_feature, train_target)
                test_score = model.score(test_feature, test_target)
                train_pred = model.predict(train_feature)
                test_pred = model.predict(test_feature)
                mae.append(mean_absolute_error(test_target, test_pred))
                mse.append(mean_squared_error(test_target, test_pred))
                rmse.append(np.sqrt(mean_squared_error(test_target, test_pred)))
                r2.append(r2_score(test_target, test_pred))

            #Creating a Metrics Dictionary for the regression models
            evaluation_df = pd.DataFrame([mae, mse, rmse, r2], index = index, columns = model_names)
            evaluation_df = evaluation_df.transpose()
            evaluation_df = evaluation_df.rename_axis('Algorithms')
            st.write('\n\n', evaluation_df, '\n\n')

            chosen_model = evaluation_df['r2'].idxmax()
            highest_r2 = evaluation_df.loc[chosen_model, 'r2']
            st.write("The chosen model with the highest accuracy is:", chosen_model)
            st.write("R squared score given by the model is:", highest_r2)
            st.write("in percentage:", highest_r2*100, "%")

    #Classification
    elif isinstance(st.session_state.target_column, pd.Series) and st.session_state.target_column.dtype == 'object':
        st.write("Performing Classification")
        feature_column = st.session_state.df[st.session_state.list_of_feature_columns]
        target_column = st.session_state.target_column
        train_feature, test_feature, train_target, test_target = train_test_split(feature_column, target_column, random_state=42)
        num_unique_features = len(train_feature.value_counts())
        num_unique_target = len(train_target.value_counts())
        is_balanced = (num_unique_features == num_unique_target)

        if not is_balanced:
            st.write("The data is imbalanced. Balancing using SMOTE.")
            smote = SMOTE(random_state=42)
            train_feature, train_target = smote.fit_resample(train_feature, train_target)
        
        encoder = LabelEncoder()
        train_target_encoded = encoder.fit_transform(train_target)
        test_target_encoded = encoder.transform(test_target)

        models = [
            LogisticRegression(max_iter=1000, solver='liblinear'),
            DecisionTreeClassifier(),
            RandomForestClassifier(),
            XGBClassifier(),
            KNeighborsClassifier(),
            SVC(),
            GaussianNB()
        ]
        
        accuracy = []
        precision = []
        recall = []
        f1_scores = []
        model_names = ['LogisticRegression', 'DecisionTreeClassifier', 'RandomForestClassifier', 'XGBClassifier', 
                    'KNeighborsClassifier', 'SVC', 'GaussianNB']
        index = ['accuracy', 'precision', 'recall', 'f1_Score']

        for model in models:
            model.fit(train_feature, train_target_encoded)
            train_pred = model.predict(train_feature)
            test_pred = model.predict(test_feature)
            accuracy.append(accuracy_score(test_target_encoded, test_pred))
            precision.append(precision_score(test_target_encoded, test_pred, average = 'macro'))
            recall.append(recall_score(test_target_encoded, test_pred, average = 'macro'))
            f1_scores.append(f1_score(test_target_encoded, test_pred, average = 'macro'))

        #Creating a Metrics Dictionary for the classification models
        evaluation_df = pd.DataFrame([accuracy, precision, recall, f1_scores], index = index, columns = model_names)
        evaluation_df = evaluation_df.transpose()
        evaluation_df = evaluation_df.rename_axis('Algorithms')
        st.write('\n\n', evaluation_df, '\n\n')
        
        chosen_model = evaluation_df['accuracy'].idxmax()
        highest_accuracy = evaluation_df.loc[chosen_model, 'accuracy']
        st.write("The chosen model with the highest accuracy is:", chosen_model)
        st.write("Accuracy given by the model is:", highest_accuracy)
        st.write("in percentage:", highest_accuracy*100, "%")

    else:
        st.write("Not performing classification as target data type is not suitable.")