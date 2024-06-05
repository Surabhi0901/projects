#Importing necessary libraries

import pickle
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, classification_report, roc_auc_score
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, RandomForestClassifier
from xgboost import XGBRegressor, XGBClassifier
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pandas as pd

#Uploading the data

data = pd.read_csv(r"C:\Users\sy090\Downloads\PROJECTS\copper_industry_data_modeling\preprocessed_data.csv")

#Define target and features for regression
X_reg = data.drop(columns=['selling_price', 'customer', 'product_ref', 'status'])
y_reg = data['selling_price']

#Split the data for regression
X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)

#Define regression models
regression_models = {
    "Linear": LinearRegression(),
    "Decision Tree": DecisionTreeRegressor(),
    "Random Forest": RandomForestRegressor(),
    "Gradient Boosting": GradientBoostingRegressor(),
    "XGBoost": XGBRegressor(),
    "KNeighbors": KNeighborsRegressor()
}

# Train, predict, and evaluate each regression model, and save them
for name, regressor in regression_models.items():
    regressor.fit(X_train_reg, y_train_reg)
    y_pred_reg = regressor.predict(X_test_reg)
    mse = mean_squared_error(y_test_reg, y_pred_reg)
    rmse = mse ** 0.5
    r2 = r2_score(y_test_reg, y_pred_reg)
    print(f"Model: {name}")
    print(f"Root Mean Squared Error (RMSE): {rmse}")
    print(f"R2 Score: {r2}")
    print("----------")
    with open(f'C:/Users/sy090/Downloads/PROJECTS/copper_industry_data_modeling/{name.replace(" ", "_").lower()}_regressor.pkl', 'wb') as f:
        pickle.dump(regressor, f)

# Define target and features for classification
classification_data = data[data['status'].isin(['Won', 'Lost'])]
X_cls = classification_data.drop(columns=['status', 'customer', 'thickness', 'width'])
y_cls = classification_data['status'].map({'Won': 1, 'Lost': 0})

# Split the data for classification
X_train_cls, X_test_cls, y_train_cls, y_test_cls = train_test_split(X_cls, y_cls, test_size=0.2, random_state=42)

# Define classification models
classification_models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, solver='liblinear'),
    "Decision Tree": DecisionTreeClassifier(),
    "Random Forest": RandomForestClassifier(),
    "XGBoost": XGBClassifier(),
    "KNN": KNeighborsClassifier(),
    "Naive Bayes": GaussianNB()
}

# Train, predict, and evaluate each classification model, and save them
for name, classifier in classification_models.items():
    classifier.fit(X_train_cls, y_train_cls)
    y_pred_cls = classifier.predict(X_test_cls)
    accuracy = accuracy_score(y_test_cls, y_pred_cls)
    report = classification_report(y_test_cls, y_pred_cls, output_dict=True)
    auc = roc_auc_score(y_test_cls, classifier.predict_proba(X_test_cls)[:, 1])
    print(f"Classifier: {name}")
    print(f"Accuracy: {accuracy}")
    print(f"AUC: {auc}")
    print("Classification Report:")
    print(classification_report(y_test_cls, y_pred_cls))
    print("----------")
    with open(f'C:/Users/sy090/Downloads/PROJECTS/copper_industry_data_modeling/{name.replace(" ", "_").lower()}_classifier.pkl', 'wb') as f:
        pickle.dump(classifier, f)

# Save the scaler
scaler_r = StandardScaler()
X_train_scaled_r = scaler_r.fit_transform(X_train_reg)
X_test_scaled_r = scaler_r.transform(X_test_reg)
with open('C:/Users/sy090/Downloads/PROJECTS/copper_industry_data_modeling/scaler_r.pkl', 'wb') as f:
    pickle.dump(scaler_r, f)

scaler_c = StandardScaler()
X_train_scaled_c = scaler_c.fit_transform(X_train_cls)
X_test_scaled_c = scaler_c.transform(X_test_cls)
with open('C:/Users/sy090/Downloads/PROJECTS/copper_industry_data_modeling/scaler_c.pkl', 'wb') as f:
    pickle.dump(scaler_c, f)