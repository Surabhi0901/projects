# Horse Race Prediction

This project aims to predict horse racing outcomes using machine learning techniques. The dataset includes detailed information on horse races and individual horses from 1990 to 2020. Given the complexity and inherent unpredictability of horse racing, this project seeks to explore various machine learning models and feature engineering techniques to improve prediction accuracy.

## Datasets

Datasets are available at the following link: [Download Datasets](https://drive.google.com/file/d/1QIA7LTQVv_JYPRekSUPGXSBEuUdpTjA5/view?usp=sharing)

## Importing Necessary Libraries

The project uses several Python libraries including pandas, numpy, matplotlib, and scikit-learn for data manipulation, visualization, and machine learning model building.

## Combining the Files

The data consists of multiple CSV files for races and horses, which are combined into single DataFrames for easier analysis.

## Reading the Combined Files

The combined datasets are read into pandas DataFrames for further processing and analysis.

## Cleaning the Data

- Dropped columns with more than 50% missing values.
- Imputed missing numerical values with the median.
- Imputed missing categorical values with the mode.
- Verified that missing values have been handled.

## Visualizing the Dataset: EDA

- **Distribution Graphs**: Created histograms and bar graphs to visualize the distribution of column data.
- **Correlation Matrix**: Generated a correlation matrix to examine the relationships between numerical features.
- **Scatter and Density Plots**: Created scatter and density plots for numerical features to visualize their relationships.

## Modeling and Evaluation

### Step 1: Prepare Data for Modeling

- Separated features (X) and target variable (y).
- Applied frequency encoding for categorical variables.
- Split data into training and test sets.
- Standardized the data.

### Step 2: Handle Imbalanced Data using SMOTE

Used SMOTE to handle class imbalance in the training data.

### Step 3: Model Selection

Evaluated the following models:
- Logistic Regression
- Random Forest
- Gradient Boosting

Generated classification reports and confusion matrices for each model.

### Step 4: Feature Selection using Recursive Feature Elimination (RFE)

- Applied RFE to select the most important features.
- Trained and evaluated a RandomForestClassifier using selected features.

### Step 5: Hyperparameter Tuning using GridSearchCV

- Performed hyperparameter tuning for RandomForestClassifier using GridSearchCV.
- Evaluated the best model from GridSearchCV.

### Step 6: Model Evaluation

- Evaluated the final model performance using classification reports and confusion matrices.
