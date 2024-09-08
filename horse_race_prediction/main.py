#Datasets are available on the following this link: https://drive.google.com/file/d/1QIA7LTQVv_JYPRekSUPGXSBEuUdpTjA5/view?usp=sharing

# Importing neccessary libraries

import pandas as pd
import glob
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np 
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.feature_selection import RFE
from imblearn.over_sampling import SMOTE

'''
# Combining the files

races_files = glob.glob(r'C:\\Users\\sy090\\Downloads\\PROJECTS\\horse_race_prediction\\data\\races_*.csv')
races_list = [pd.read_csv(file) for file in races_files]
races_combined = pd.concat(races_list, ignore_index=True)
full_path = r'C:\\Users\\sy090\\Downloads\\PROJECTS\\horse_race_prediction\\races_combined.csv'
races_combined.to_csv(full_path, index=False)

horses_files = glob.glob(r'C:\\Users\\sy090\\Downloads\\PROJECTS\\horse_race_prediction\\data\\horses_*.csv')
horses_list = [pd.read_csv(file) for file in horses_files]
horses_combined = pd.concat(horses_list, ignore_index=True)
full_path = r'C:\\Users\\sy090\\Downloads\\PROJECTS\\horse_race_prediction\\horses_combined.csv'
horses_combined.to_csv(full_path, index=False)
'''
# Reading the combined files

races_combined = pd.read_csv(r'C:\\Users\\sy090\\Downloads\\PROJECTS\\horse_race_prediction\\races_combined.csv')
horses_combined = pd.read_csv(r'C:\\Users\\sy090\\Downloads\\PROJECTS\\horse_race_prediction\\horses_combined.csv')
# print("Before cleaning the combined race dataset")
# print(races_combined.isnull().sum())
# print(races_combined.info())
# print("\n\nBefore cleaning the combined horse dataset")
# print(horses_combined.isnull().sum())
# print(horses_combined.info())

forward_csv = pd.read_csv(r'C:\\Users\\sy090\\Downloads\\PROJECTS\\horse_race_prediction\\forward.csv')
# print("\n\nBefore cleaning the additional info dataset")
# print(forward_csv.isnull().sum())
# print(forward_csv.info())

# Cleaning the data

# Drop columns with more than 50% missing values
races_cleaned = races_combined.drop(columns=['hurdles', 'band'])
horses_cleaned = horses_combined.drop(columns=['overWeight', 'outHandicap', 'headGear', 'price'])

# Impute missing numerical values with median
races_cleaned['prize'].fillna(races_cleaned['prize'].median(), inplace=True)
horses_cleaned['age'].fillna(horses_cleaned['age'].median(), inplace=True)
horses_cleaned['saddle'].fillna(horses_cleaned['saddle'].median(), inplace=True)
horses_cleaned['RPR'].fillna(horses_cleaned['RPR'].median(), inplace=True)
horses_cleaned['TR'].fillna(horses_cleaned['TR'].median(), inplace=True)
horses_cleaned['OR'].fillna(horses_cleaned['OR'].median(), inplace=True)

forward_cleaned = forward_csv.copy()
forward_cleaned['RPRc'].fillna(forward_cleaned['RPRc'].median(), inplace=True)
forward_cleaned['TRc'].fillna(forward_cleaned['TRc'].median(), inplace=True)
forward_cleaned['OR'].fillna(forward_cleaned['OR'].median(), inplace=True)

# Impute missing categorical values with mode
races_cleaned['rclass'].fillna(races_cleaned['rclass'].mode()[0], inplace=True)
races_cleaned['title'].fillna(races_cleaned['title'].mode()[0], inplace=True)
races_cleaned['ages'].fillna(races_cleaned['ages'].mode()[0], inplace=True)
races_cleaned['condition'].fillna(races_cleaned['condition'].mode()[0], inplace=True)
horses_cleaned['trainerName'].fillna(horses_cleaned['trainerName'].mode()[0], inplace=True)
horses_cleaned['jockeyName'].fillna(horses_cleaned['jockeyName'].mode()[0], inplace=True)
horses_cleaned['positionL'].fillna(horses_cleaned['positionL'].mode()[0], inplace=True)
horses_cleaned['dist'].fillna(horses_cleaned['dist'].mode()[0], inplace=True)
horses_cleaned['father'].fillna(horses_cleaned['father'].mode()[0], inplace=True)
horses_cleaned['mother'].fillna(horses_cleaned['mother'].mode()[0], inplace=True)
horses_cleaned['gfather'].fillna(horses_cleaned['gfather'].mode()[0], inplace=True)

forward_cleaned['course'].fillna(forward_cleaned['course'].mode()[0], inplace=True)
forward_cleaned['condition'].fillna(forward_cleaned['condition'].mode()[0], inplace=True)
forward_cleaned['rclass'].fillna(forward_cleaned['rclass'].mode()[0], inplace=True)
forward_cleaned['jockeyName'].fillna(forward_cleaned['jockeyName'].mode()[0], inplace=True)

# Verify the missing values have been handled
missing_values_races_cleaned = races_cleaned.isnull().sum()
missing_values_horses_cleaned = horses_cleaned.isnull().sum()
missing_values_forward_cleaned = forward_cleaned.isnull().sum()

print("After cleaning the combined race dataset")
print(missing_values_races_cleaned)
print("\n\nAfter cleaning the combined horse dataset")
print(missing_values_horses_cleaned)
print("\n\nAfter cleaning the additional info dataset")
print(missing_values_forward_cleaned)

# Visualing the dataset: EDA

# Distribution graphs (histogram/bar graph) of column data
def plotPerColumnDistribution(df, nGraphShown, nGraphPerRow):
    nunique = df.nunique()
    df = df[[col for col in df if nunique[col] > 1 and nunique[col] < 50]] # For displaying purposes, pick columns that have between 1 and 50 unique values
    nRow, nCol = df.shape
    columnNames = list(df)
    nGraphRow = int((nCol + nGraphPerRow - 1) / nGraphPerRow)  # Convert to integer
    plt.figure(num=None, figsize=(6 * nGraphPerRow, 8 * nGraphRow), dpi=80, facecolor='w', edgecolor='k')
    for i in range(min(nCol, nGraphShown)):
        plt.subplot(nGraphRow, nGraphPerRow, i + 1)
        columnDf = df.iloc[:, i]
        if not np.issubdtype(type(columnDf.iloc[0]), np.number):
            valueCounts = columnDf.value_counts()
            valueCounts.plot.bar()
        else:
            columnDf.hist()
        plt.ylabel('counts')
        plt.xticks(rotation=90)
        plt.title(f'{columnNames[i]} (column {i})')
    plt.tight_layout(pad=1.0, w_pad=1.0, h_pad=1.0)
    plt.show()

# Correlation matrix
def plotCorrelationMatrix(df, graphWidth):
    df = df.select_dtypes(include=[np.number])  # Keep only numeric columns
    df = df.dropna(axis='columns')  # Drop columns with NaN
    df = df[[col for col in df if df[col].nunique() > 1]]  # Keep columns where there are more than 1 unique values
    if df.shape[1] < 2:
        print(f'No correlation plots shown: The number of non-NaN or constant columns ({df.shape[1]}) is less than 2')
        return
    corr = df.corr()
    plt.figure(num=None, figsize=(graphWidth, graphWidth), dpi=80, facecolor='w', edgecolor='k')
    corrMat = plt.matshow(corr, fignum=1)
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.gca().xaxis.tick_bottom()
    plt.colorbar(corrMat)
    plt.title('Correlation Matrix', fontsize=15)
    plt.show()

# Scatter and density plots
def plotScatterMatrix(df, plotSize, textSize, sample_size=500):
    df = df.select_dtypes(include=[np.number])  # keep only numerical columns
    df = df.dropna(axis='columns')  # Remove columns with NaN values
    df = df[[col for col in df if df[col].nunique() > 1]]  # keep columns where there are more than 1 unique values
    columnNames = list(df)
    if len(columnNames) > 10:  # reduce the number of columns for matrix inversion of kernel density plots
        columnNames = columnNames[:10]
    df = df[columnNames]
    
    if len(df) > sample_size:  # Sample the data if it's too large
        df = df.sample(sample_size)
    
    ax = pd.plotting.scatter_matrix(df, alpha=0.75, figsize=[plotSize, plotSize], diagonal='kde')
    corrs = df.corr().values
    for i, j in zip(*plt.np.triu_indices_from(ax, k=1)):
        ax[i, j].annotate('Corr. coef = %.3f' % corrs[i, j], (0.8, 0.2), xycoords='axes fraction', ha='center', va='center', size=textSize)
    plt.suptitle('Scatter and Density Plot')
    plt.show()
    
plotPerColumnDistribution(horses_cleaned, 10, 5)
plotCorrelationMatrix(horses_cleaned, 8)
plotScatterMatrix(horses_cleaned, 20, 10)

# Step 1: Prepare Data for Modeling
# Assuming 'res_win' is the target variable (1 for win, 0 for no win)
X = horses_cleaned.drop(columns=['res_win'])
y = horses_cleaned['res_win']

# Frequency Encoding for categorical variables
for col in X.select_dtypes(include=['object']).columns:
    freq_encoding = X[col].value_counts().to_dict()
    X[col] = X[col].map(freq_encoding)

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Step 2: Handle Imbalanced Data using SMOTE
sm = SMOTE(random_state=42)
X_train_res, y_train_res = sm.fit_resample(X_train, y_train)

# Step 3: Model Selection
models = {
    'Logistic Regression': LogisticRegression(max_iter=1000),
    'Random Forest': RandomForestClassifier(),
    'Gradient Boosting': GradientBoostingClassifier()
}

for name, model in models.items():
    model.fit(X_train_res, y_train_res)
    y_pred = model.predict(X_test)
    print(f"Model: {name}")
    print(classification_report(y_test, y_pred))
    print(confusion_matrix(y_test, y_pred))
    print("\n")

# Step 4: Feature Selection using Recursive Feature Elimination (RFE)
# Use RandomForestClassifier as an example
rfe_selector = RFE(estimator=RandomForestClassifier(), n_features_to_select=10, step=1)
rfe_selector = rfe_selector.fit(X_train_res, y_train_res)

# Select the important features
selected_features = X.columns[rfe_selector.support_]
print("Selected Features: ", selected_features)

# Train and evaluate model using selected features
X_train_res_rfe = rfe_selector.transform(X_train_res)
X_test_rfe = rfe_selector.transform(X_test)

rf_rfe = RandomForestClassifier()
rf_rfe.fit(X_train_res_rfe, y_train_res)
y_pred_rfe = rf_rfe.predict(X_test_rfe)
print("Random Forest with RFE")
print(classification_report(y_test, y_pred_rfe))
print(confusion_matrix(y_test, y_pred_rfe))
print("\n")

# Step 5: Hyperparameter Tuning using GridSearchCV
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_features': ['auto', 'sqrt', 'log2'],
    'max_depth': [4, 6, 8],
    'criterion': ['gini', 'entropy']
}

grid_search = GridSearchCV(estimator=RandomForestClassifier(), param_grid=param_grid, cv=5, n_jobs=-1)
grid_search.fit(X_train_res_rfe, y_train_res)

best_rf = grid_search.best_estimator_
y_pred_best = best_rf.predict(X_test_rfe)
print("Best Random Forest after GridSearchCV")
print(classification_report(y_test, y_pred_best))
print(confusion_matrix(y_test, y_pred_best))
print("\n")

# Step 6: Model Evaluation
# Evaluate the final model performance
final_model = best_rf
y_pred_final = final_model.predict(X_test_rfe)
print("Final Model Evaluation")
print(classification_report(y_test, y_pred_final))
print(confusion_matrix(y_test, y_pred_final))