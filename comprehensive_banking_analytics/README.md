# Comprehensive Banking Analytics Project Overview

## Introduction

This project aims to provide a comprehensive analysis of banking data, including Exploratory Data Analysis (EDA), customer segmentation, credit risk assessment, and performance prediction. The goal is to gain insights into the data, identify key features influencing credit scores, and build predictive models to assess credit risk and performance.

## Prerequisites

Make sure you have the following libraries installed:

- pandas
- numpy
- seaborn
- scikit-learn
- xgboost
- imbalanced-learn
- matplotlib

You can install these libraries using pip:
```bash
pip install pandas numpy seaborn scikit-learn xgboost imbalanced-learn matplotlib
```

## Data

The dataset used in this project is a CSV file containing banking information. The data is loaded using pandas and various preprocessing steps are performed to prepare it for analysis and modeling.

## Project Structure

1. **Import Libraries**: Importing necessary libraries for data manipulation, visualization, and modeling.
2. **Data Loading**: Reading the data from a CSV file.
3. **Data Exploration**: Initial exploration of the data, checking for null values, and basic data information.
4. **Data Preprocessing**: Converting categorical columns to numerical values and handling missing values.
5. **Exploratory Data Analysis (EDA)**:
    - Histograms of numerical columns.
    - Boxplots of numerical columns.
    - Correlation heatmap.
    - Pairplot of numerical columns.
    - Distribution of the target variable (Credit Score).
    - Countplots to analyze the effect of different features on Credit Score.
6. **Feature Importance**: Using a Random Forest Classifier to identify important features.
7. **Customer Segmentation**: Using K-Means clustering for customer segmentation based on selected features.
8. **Credit Risk Assessment**: Building and evaluating various classification models to predict Credit Score.
9. **Performance Prediction**: Building and evaluating various regression models to predict Credit Score.

## Results

### Exploratory Data Analysis (EDA)
- Histograms and boxplots provided insights into the distribution and outliers of numerical features.
- The correlation heatmap helped identify relationships between features.
- Pairplots visualized the relationships between pairs of features.
- Countplots showed the distribution of Credit Scores based on various features.

### Feature Importance
- Random Forest Classifier identified the most important features influencing the Credit Score.

### Customer Segmentation
- K-means clustering segmented customers into distinct groups based on selected features.

### Credit Risk Assessment
- Various classification models were trained to predict Credit Score.
- Performance metrics like accuracy and classification reports were generated for each model.

### Performance Prediction
- Various regression models were trained to predict Credit Score.
- Performance metrics like RMSE and R2 score were generated for each model.

## Conclusion

This project demonstrated a comprehensive approach to analyzing banking data. By performing EDA, identifying important features, segmenting customers, and building predictive models, we gained valuable insights into the factors influencing Credit Scores and the overall performance of customers. The results can help in making informed decisions for credit risk assessment and customer segmentation.

## Future Work

- Fine-tuning models with hyperparameter optimization.
- Exploring additional feature engineering techniques.
- Implementing more advanced machine learning models.
- Integrating external data sources for enhanced predictions.

## License

This project is licensed under the MIT License.

## Images of the graphs

Histogram of all the relevant numerical columns

![Histogram](https://github.com/surabhi0901/comprehensive_banking_analytics/assets/78378870/183f58d8-b7f0-4df7-b429-7602c6cd6858)

Boxplots of all the relevant numerical columns

![Boxplots](https://github.com/surabhi0901/comprehensive_banking_analytics/assets/78378870/ee2e3b85-fafb-4afd-87af-4b03ee61419d)

Correlation Heatmap

![Correlation Heatmap](https://github.com/surabhi0901/comprehensive_banking_analytics/assets/78378870/f16b4ae4-96c6-48af-8f4b-d996438c1b70)

Pairplot

![Pairplot](https://github.com/surabhi0901/comprehensive_banking_analytics/assets/78378870/63d46b1a-11c7-4d1b-b0c7-0eca680ef192)

Vizualization of the target column distribution

![Credit Score Distribution](https://github.com/surabhi0901/comprehensive_banking_analytics/assets/78378870/aff6f6eb-0962-42d6-a917-16ada7e1c1ba)

Barplots

![Credit Score based on Num of Bank Acc](https://github.com/surabhi0901/comprehensive_banking_analytics/assets/78378870/e206b8bc-52f2-4799-8a46-903b584b215b)

![Credit Score based on Num of Bank Credit Cards](https://github.com/surabhi0901/comprehensive_banking_analytics/assets/78378870/07941ca0-541a-4ec3-924a-2f0bdedae4ad)

![Credit Score based on Num of Loans](https://github.com/surabhi0901/comprehensive_banking_analytics/assets/78378870/ef131a7a-93ea-4db4-b7e3-e7e42490515e)

![Credit Score based on Num of Bank Credit Inquiries](https://github.com/surabhi0901/comprehensive_banking_analytics/assets/78378870/7f16193b-6004-468b-a385-b61bee1141b6)

![Credit Score based on Credit Mix](https://github.com/surabhi0901/comprehensive_banking_analytics/assets/78378870/056aabb5-0ed8-4754-8214-cb131fffae3f)

Feature importance to help with feature selection

![Random Forest Feature Importances](https://github.com/surabhi0901/comprehensive_banking_analytics/assets/78378870/0553abb8-25cf-4ff6-b6bd-a52d471b3fd9)

## Customer Segmentation

Graph showing elbow method to get the k value

![Graph for elbow method](https://github.com/surabhi0901/comprehensive_banking_analytics/assets/78378870/4687feb0-74e7-4492-ae37-9312e85a2c0f)

Customer Segmentation by K-means Clustering

![Customer Segmentation by K-means Clustering](https://github.com/surabhi0901/comprehensive_banking_analytics/assets/78378870/fc306afb-873e-493e-addb-2106086ac90c)

## Credit Risk Assessment

Classifier: Logistic Regression
Accuracy: 0.93325
Classification Report:
              precision    recall  f1-score   support

           0       1.00      1.00      1.00      5874
           1       0.91      0.96      0.94     10599
           2       0.87      0.73      0.79      3527

    accuracy                           0.93     20000
   macro avg       0.93      0.90      0.91     20000
weighted avg       0.93      0.93      0.93     20000

----------
Classifier: Decision Tree
Accuracy: 1.0
Classification Report:
              precision    recall  f1-score   support

           0       1.00      1.00      1.00      5874
           1       1.00      1.00      1.00     10599
           2       1.00      1.00      1.00      3527

    accuracy                           1.00     20000
   macro avg       1.00      1.00      1.00     20000
weighted avg       1.00      1.00      1.00     20000

----------
Classifier: Random Forest
Accuracy: 1.0
Classification Report:
              precision    recall  f1-score   support

           0       1.00      1.00      1.00      5874
           1       1.00      1.00      1.00     10599
           2       1.00      1.00      1.00      3527

    accuracy                           1.00     20000
   macro avg       1.00      1.00      1.00     20000
weighted avg       1.00      1.00      1.00     20000

----------
Classifier: XGBoost
Accuracy: 1.0
Classification Report:
              precision    recall  f1-score   support

           0       1.00      1.00      1.00      5874
           1       1.00      1.00      1.00     10599
           2       1.00      1.00      1.00      3527

    accuracy                           1.00     20000
   macro avg       1.00      1.00      1.00     20000
weighted avg       1.00      1.00      1.00     20000

----------
Classifier: KNN
Accuracy: 0.7768
Classification Report:
              precision    recall  f1-score   support

           0       0.76      0.82      0.79      5874
           1       0.80      0.78      0.79     10599
           2       0.72      0.69      0.71      3527

    accuracy                           0.78     20000
   macro avg       0.76      0.76      0.76     20000
weighted avg       0.78      0.78      0.78     20000

----------
Classifier: Naive Bayes
Accuracy: 0.6292
Classification Report:
              precision    recall  f1-score   support

           0       0.64      0.73      0.68      5874
           1       0.81      0.51      0.62     10599
           2       0.44      0.83      0.57      3527

    accuracy                           0.63     20000
   macro avg       0.63      0.69      0.63     20000
weighted avg       0.69      0.63      0.63     20000

----------

## Performance Prediction

----------

Model: Linear Regression
Root Mean Squared Error (RMSE): 2.8070534180026826e-15
R2 Score: 1.0

Model: Decision Tree Regressor
Root Mean Squared Error (RMSE): 0.0
R2 Score: 1.0

Model: Random Forest Regressor
Root Mean Squared Error (RMSE): 0.0
R2 Score: 1.0

Model: Gradient Boosting Regressor
Root Mean Squared Error (RMSE): 1.794278735749497e-05
R2 Score: 0.999999999294415

Model: XGBoost Regressor
Root Mean Squared Error (RMSE): 3.329686164276412e-06
R2 Score: 0.9999999999757017

Model: KNeighbors Regressor
Root Mean Squared Error (RMSE): 0.4220118481749061
R2 Score: 0.6096817763207161

----------
