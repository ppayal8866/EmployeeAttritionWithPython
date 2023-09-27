# -*- coding: utf-8 -*-
"""Copy of My HR Analysis Project Complete(Dont'touch)

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nO46VdJ78TlwNlwoN8ktwLmvlkoXqxel

# TASK #1: IMPORT LIBRARIES AND DATASETS
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

pd.set_option('max_rows', 99999)
pd.set_option('max_colwidth', 100)

# You will need to mount your drive using the following commands:
# For more information regarding mounting, please check this out: https://stackoverflow.com/questions/46986398/import-data-into-google-colaboratory

from google.colab import drive
drive.mount('/content/drive/')

"""## Reading  the dataset"""

# You have to include the full link to the csv file containing your dataset

employee_df = pd.read_csv('drive/MyDrive/Human_Resources.csv')
employee_df.head(5)

"""##Data Cleaning

###Ckecking duplicate records
"""

# No duplicate records
duplicate = employee_df[employee_df.duplicated()]
duplicate.count()

"""###Checking null values"""

#Checking null values
employee_df.isnull().sum()

"""## Data exploration

###Data shape
"""

print("Number of rows: ",len(employee_df),"\t","Number of columns: ",len(employee_df.columns))

"""###Dataframe information"""

employee_df.info()

"""###Descriptive statistics of dataframe"""

#Overall stats
overall_stat = employee_df.describe()
overall_stat

"""# TASK #2: VISUALIZE DATASET

## 3 Categorical columns to Numeric conversion
"""

# Let's replace 'Attritition' , 'overtime' , 'Over18' column with integers before performing any visualizations
employee_df['Attrition'] = employee_df['Attrition'].apply(lambda x:1 if x == 'Yes' else 0) #1: left/Yes & 0: stayed/No
employee_df['OverTime'] = employee_df['OverTime'].apply(lambda x:1 if x == 'Yes' else 0)
employee_df['Over18'] = employee_df['Over18'].apply(lambda x:1 if x == 'Y' else 0)

"""##Plot 1: Visualizing missing data"""

# Visualizing missing data with seaborn heatmap()
# sns.heatmap(employee_df.isnull(), yticklabels = False, cbar = False, cmap="Blues")

# Visualizing missing data with seaborn heatmap()
plt.figure(figsize=(12,8))
sns.heatmap(employee_df.isnull(), yticklabels = False, cbar = False, cmap="Blues")

plt.tight_layout()
plt.show()

"""##Plot 2: Bar chart of 'Gender' column"""

employee_df['Gender'].value_counts().plot(kind='bar',color=['salmon','lightblue'],title="Count of different gender")

employee_df['Gender'].value_counts()

"""##Plot 3: Pie chart of 'Attrition' column"""

#Pie chart: Left/Stayed
from matplotlib import legend

plt.figure(figsize=(10,6))
slices = employee_df['Attrition'].value_counts()

plt.pie(slices,
        autopct='%1.1f%%',
        explode=[0,0.15],
        labels=['Stayed', 'Left'],
        colors=['#008fd5','#e5ae37'],
        shadow=True,
        textprops = {"fontsize":13}
        )

plt.title('Distribution of attrition variable')
plt.legend(loc="upper right")
plt.tight_layout()
plt.show()

"""##Plot 4: Bar chart Gender vs. Attrition"""

#Bar chart Gender vs. Attrition
pd.crosstab(employee_df['Gender'],employee_df['Attrition'] ).plot(kind="bar",figsize=(10,6))
plt.title("Stay/Left vs Gender")
plt.xlabel("Stay/Left")
plt.ylabel("No of people who left based on gender")
plt.legend(['Stayed', 'Left'])
plt.xticks(rotation=0)
plt.tight_layout()

"""**bold text**##Plot 5: Histogram of all columns"""

# Several features such as 'MonthlyIncome' and 'TotalWorkingYears' are tail heavy
# It makes sense to drop 'EmployeeCount' and 'Standardhours' since they do not change from one employee to the other
plt.subplots(nrows=12,ncols=3, figsize=(20,20))
count = 0
for x in employee_df.columns:
    count = count+1
    plt.subplot(12,3,count)
    plt.hist(employee_df[x],edgecolor='black', bins=30, color = 'r')
    plt.title(x)
plt.tight_layout()
plt.show()

"""##Plot 5 Jobsatisfaction vs. JobRole"""

plt.figure(figsize=[20,20])
plt.subplot(411)
sns.countplot(x = 'JobRole', hue = 'JobSatisfaction', data = employee_df)

"""##Dropping unnecessary columns"""

# 4 colums dropperd: It makes sense to drop  'EmployeeCount' , 'Standardhours' and 'Over18' since they do not change from one employee to the other
# Let's drop 'EmployeeNumber' as well
employee_df.drop(['EmployeeCount', 'StandardHours', 'Over18', 'EmployeeNumber'], axis=1, inplace=True)

# Let's see how many employees left the company!
left_df        = employee_df[employee_df['Attrition'] == 1]
stayed_df      = employee_df[employee_df['Attrition'] == 0]

# Count the number of employees who stayed and left
# It seems that we are dealing with an imbalanced dataset
print("Total = ", len(employee_df))

print("Number of employees who left the company =", len(left_df))
print("Percentage of employees who left the company =", 1.*len(left_df)/len(employee_df)*100.0, "%")

print("Number of employees who did not leave the company (stayed) =", len(stayed_df))
print("Percentage of employees who did not leave the company (stayed) =", 1.*len(stayed_df)/len(employee_df)*100.0, "%")

left_df.describe()

#  Let's compare the mean and std of the employees who stayed and left
# 'age': mean age of the employees who stayed is higher compared to who left
# 'DailyRate': Rate of employees who stayed is higher
# 'DistanceFromHome': Employees who stayed live closer to home
# 'EnvironmentSatisfaction' & 'JobSatisfaction': Employees who stayed are generally more satisifed with their jobs
# 'StockOptionLevel': Employees who stayed tend to have higher stock option level

stayed_df.describe()

"""##Plot 6: Correlation matrix"""

correlations = employee_df.corr(method='pearson').abs()
f, ax = plt.subplots(figsize = (20, 20))
sns.heatmap(correlations, annot = True)

# JobLevel is strongly correlated with TotalWorkingYears
# MonthlyIncome is strongly correlated with JobLevel
# MonthlyIncome is strongly correlated with TotalWorkingYears
# Age is stongly correlated with monthly income

#Correlation of Independent Variables with the Dependent Variable(Attrition)
plt.figure(figsize=(8, 12))
heatmap = sns.heatmap(employee_df.corr()[['Attrition']].sort_values(by='Attrition', ascending=False), vmin=-1, vmax=1, annot=True, cmap='BrBG')
heatmap.set_title('Features Correlating with Attrition', fontdict={'fontsize':18}, pad=16);

"""## Plot 7: Histogram Age vs. Attrition"""

plt.figure(figsize=[25, 12])
sns.countplot(x = 'Age', hue = 'Attrition', data = employee_df)

"""##Plot 8: Histogram Attrition vs. JobRole, MaritalStatus, JobInvolvement, and JobLevel"""

plt.figure(figsize=[20,20])
plt.subplot(411)
sns.countplot(x = 'JobRole', hue = 'Attrition', data = employee_df)
plt.subplot(412)
sns.countplot(x = 'MaritalStatus', hue = 'Attrition', data = employee_df)
plt.subplot(413)
sns.countplot(x = 'JobInvolvement', hue = 'Attrition', data = employee_df)
plt.subplot(414)
sns.countplot(x = 'JobLevel', hue = 'Attrition', data = employee_df)

# Single employees tend to leave compared to married and divorced
# Sales Representitives tend to leave compared to any other job
# Less involved employees tend to leave the company
# Less experienced (low job level) tend to leave the company

"""###Plot 8.1: JobRole vs. MonthlyIncome"""

plt.figure(figsize=(10,7))
sns.barplot(x='JobRole', y='MonthlyIncome', hue='Attrition', data=employee_df)
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

"""##Plot 9: KDE of DistanceFromHome column"""

# KDE (Kernel Density Estimate) is used for visualizing the Probability Density of a continuous variable.
# KDE describes the probability density at different values in a continuous variable.

plt.figure(figsize=(12,7))

sns.kdeplot(left_df['DistanceFromHome'], label = 'Employees who left', shade = True, color = 'r')
sns.kdeplot(stayed_df['DistanceFromHome'], label = 'Employees who Stayed', shade = True, color = 'b')

plt.xlabel('Distance From Home')
plt.legend()

"""##Plot 10: KDE for YearsWithCurrManager column"""

plt.figure(figsize=(12,7))

sns.kdeplot(left_df['YearsWithCurrManager'], label = 'Employees who left', shade = True, color = 'r')
sns.kdeplot(stayed_df['YearsWithCurrManager'], label = 'Employees who Stayed', shade = True, color = 'b')

plt.xlabel('Years With Current Manager')
plt.legend()

"""##Plot 11: KDE of TotalWorkingYears column"""

plt.figure(figsize=(12,7))

sns.kdeplot(left_df['TotalWorkingYears'], shade = True, label = 'Employees who left', color = 'r')
sns.kdeplot(stayed_df['TotalWorkingYears'], shade = True, label = 'Employees who Stayed', color = 'b')

plt.xlabel('Total Working Years')
plt.legend()

"""##Plot 12: Box plot MonthlyIncome vs. Gender"""

# Let's see the Gender vs. Monthly Income
plt.figure(figsize=(15, 7))
sns.boxplot(x = 'MonthlyIncome', y = 'Gender', data = employee_df)

"""##Plot 13: Box plot of MonthlyIncome vs. JobRole"""

# Let's see the monthly income vs. job role
plt.figure(figsize=(15, 10))
sns.boxplot(x = 'MonthlyIncome', y = 'JobRole', data = employee_df)

"""# TASK #3: CREATE TESTING AND TRAINING DATASET"""

# Data type conversions
employee_df['BusinessTravel'] = employee_df['BusinessTravel'].astype('category')
employee_df['Department'] = employee_df['Department'].astype('category')
employee_df['EducationField'] = employee_df['EducationField'].astype('category')
employee_df['Gender'] = employee_df['Gender'].astype('category')
employee_df['JobRole'] = employee_df['JobRole'].astype('category')
employee_df['MaritalStatus'] = employee_df['MaritalStatus'].astype('category')

employee_df.info()

#List of categories of each categorical columns

print("BusinessTravel: ",employee_df['BusinessTravel'].cat.categories)
print("Department: ",employee_df['Department'].cat.categories)
print("EducationField: ",employee_df['EducationField'].cat.categories)
print("Gender: ",employee_df['Gender'].cat.categories)
print("JobRole: ",employee_df['JobRole'].cat.categories)
print("MaritalStatus: ",employee_df['MaritalStatus'].cat.categories)

#Approach to encoding categorical values is to use a technique called label encoding. Label encoding is simply converting each value in a column to a number.
# cat code: The categorical type is a process of factorization. Meaning that each unique value or category is given a incremented integer value starting from zero.
employee_df["BusinessTravel"] = employee_df["BusinessTravel"].cat.codes
employee_df['Department']= employee_df['Department'].cat.codes
employee_df['EducationField']= employee_df['EducationField'].cat.codes
employee_df['Gender']= employee_df['Gender'].cat.codes
employee_df['JobRole']= employee_df['JobRole'].cat.codes
employee_df['MaritalStatus']= employee_df['MaritalStatus'].cat.codes

employee_df.head(5)

from sklearn.preprocessing import OneHotEncoder

onehotencoder = OneHotEncoder()

X_cat = employee_df[['BusinessTravel', 'Department', 'EducationField', 'Gender', 'JobRole', 'MaritalStatus']]
X_cat = onehotencoder.fit_transform(X_cat).toarray()
X_cat = pd.DataFrame(X_cat)
X_numerical = employee_df[['Age', 'DailyRate', 'DistanceFromHome',	'Education', 'EnvironmentSatisfaction', 'HourlyRate', 'JobInvolvement',	'JobLevel',	'JobSatisfaction',	'MonthlyIncome',	'MonthlyRate',	'NumCompaniesWorked',	'OverTime',	'PercentSalaryHike', 'PerformanceRating',	'RelationshipSatisfaction',	'StockOptionLevel',	'TotalWorkingYears'	,'TrainingTimesLastYear'	, 'WorkLifeBalance',	'YearsAtCompany'	,'YearsInCurrentRole', 'YearsSinceLastPromotion',	'YearsWithCurrManager']]
X_all = pd.concat([X_cat, X_numerical], axis = 1)

X_all.head(5)

# scalling pandas dataframe using Min-Max Normalization
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()

x = scaler.fit_transform(X_all)
x

x.shape

y = employee_df['Attrition']

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.25, random_state=42)

x_train.shape # Features

x_test.shape # Features

y_train.shape # Target variable

y_test.shape # Target variable

"""# TASK #4: TRAIN AND EVALUATE A LOGISTIC REGRESSION CLASSIFIER"""

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

#np.random.seed(42)
model_logisticRegr = LogisticRegression()
model_logisticRegr.fit(x_train, y_train)

y_pred = model_logisticRegr.predict(x_test) # Make predictions on entire test data

y_pred

"""##Plot 14: Confusion matrix of logistic regression model"""

from sklearn import metrics
# Testing Set Performance

#-----confusion matrix------------------

cm = metrics.confusion_matrix(y_pred, y_test, labels=[0,1])  # 1: left and 0: stayed


# create heatmap
sns.heatmap(cm, annot=True, cmap='YlGnBu', fmt='g')

ax.xaxis.set_label_position('top')

plt.tight_layout()
plt.title('Confusion matrix')
plt.ylabel('Actual label')
plt.xlabel('Predicted label')

# The dimension of this matrix is 2*2 because this model is binary classification. There are two classes 0 and 1.
# Diagonal values represent accurate predictions, while non-diagonal elements are inaccurate predictions.
# In the output, 308 and 20 are actual predictions, and 37 and 3 are incorrect predictions.

print(metrics.classification_report(y_test, y_pred))
# 1: left and 0: stayed

# accuracy table for training and test data
from prettytable import PrettyTable

# Specifying the Column Names while initializing the Table
myTable = PrettyTable(["Accuracy on Training Set ", "Accuracy on Testing Set"])

# Adding rows
myTable.add_row([model_logisticRegr.score(x_train, y_train) * 100, 100 * accuracy_score(y_test, y_pred)])

print(myTable)

#Accuracy
acc_logReg= (100 * (accuracy_score(y_test, y_pred)))
acc_logReg

# Receiver Operating Characteristic(ROC) curve is a plot of the true positive rate against the false positive rate. It shows the tradeoff between sensitivity and specificity.


y_pred_proba = model_logisticRegr.predict_proba(x_test)[::,1]
fpr, tpr, _ = metrics.roc_curve(y_test,  y_pred_proba)
auc = metrics.roc_auc_score(y_test, y_pred_proba)
plt.plot(fpr,tpr,label="Logistic Regression, auc="+str(auc))
plt.legend(loc=4)
plt.show()

#AUC score for the case is 0.83. AUC score 1 represents a perfect classifier, and 0.5 represents a worthless classifier.

from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve

logit_roc_auc = roc_auc_score(y_test, model_logisticRegr.predict(x_test))
fpr, tpr, thresholds = roc_curve(y_test, model_logisticRegr.predict_proba(x_test)[:,1])
plt.figure()
plt.plot(fpr, tpr, label='Logistic Regression (area = %0.2f)' % logit_roc_auc +" " + " auc="+ str(auc))
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic')
plt.legend(loc="lower right")
plt.savefig('Log_ROC')
plt.show()

"""# TASK #7: TRAIN AND EVALUATE A RANDOM FOREST CLASSIFIER"""

from sklearn.ensemble import RandomForestClassifier

model_randomForest = RandomForestClassifier()
model_randomForest.fit(x_train, y_train)

y_pred = model_randomForest.predict(x_test)

y_pred

"""##Plot 15: Confusion matrix of random forest model"""

from sklearn import metrics
# Testing Set Performance

#-----confusion matrix------------------

cm = metrics.confusion_matrix(y_pred, y_test, labels=[0,1])  # 1: left and 0: stayed


# create heatmap
sns.heatmap(cm, annot=True, cmap='YlGnBu', fmt='g')

ax.xaxis.set_label_position('top')

plt.tight_layout()
plt.title('Confusion matrix')
plt.ylabel('Actual label')
plt.xlabel('Predicted label')

# The dimension of this matrix is 2*2 because this model is binary classification. There are two classes 0 and 1.
# Diagonal values represent accurate predictions, while non-diagonal elements are inaccurate predictions.
# In the output, 308 and 20 are actual predictions, and 37 and 3 are incorrect predictions.

print(metrics.classification_report(y_test, y_pred))
# 1: left and 0: stayed

# accuracy table for training and test data
from prettytable import PrettyTable

# Specifying the Column Names while initializing the Table
myTable = PrettyTable(["Accuracy on Training Set ", "Accuracy on Testing Set"])

# Adding rows
myTable.add_row([model_randomForest.score(x_train, y_train)* 100, 100 * accuracy_score(y_test, y_pred)])

print(myTable)

#Accuracy
acc_rForest= (100 * (accuracy_score(y_test, y_pred)))
acc_rForest

"""# TASK #:8 TRAIN AND EVALUATE A DEEP LEARNING MODEL"""

import tensorflow as tf
tf.random.set_seed(42)

nn_model = tf.keras.models.Sequential()
nn_model.add(tf.keras.layers.Dense(units=500, activation='relu', input_shape=(50, )))
nn_model.add(tf.keras.layers.Dense(units=500, activation='relu'))
nn_model.add(tf.keras.layers.Dense(units=500, activation='relu'))
nn_model.add(tf.keras.layers.Dense(units=1, activation='sigmoid'))

nn_model.summary()

nn_model.compile(optimizer='Adam', loss='binary_crossentropy', metrics = ['accuracy'])

# oversampler = SMOTE(random_state=0)
# smote_train, smote_target = oversampler.fit_sample(X_train, y_train)
# epochs_hist = model.fit(smote_train, smote_target, epochs = 100, batch_size = (,50))
epochs_hist = nn_model.fit(x_train, y_train, epochs = 100, batch_size = 50)

y_pred = nn_model.predict(x_test)
y_pred = (y_pred > 0.5)

y_pred

epochs_hist.history.keys()

"""##Plot 16: Line chart of model loss of epochs_hist variable"""

plt.plot(epochs_hist.history['loss'])
plt.title('Model Loss Progress During Training')
plt.xlabel('Epoch')
plt.ylabel('Training Loss')
plt.legend(['Training Loss'])

"""##Plot 17: Line chart of model accuracy of epochs_hist variable"""

plt.plot(epochs_hist.history['accuracy'])
plt.title('Model Accuracy Progress During Training')
plt.xlabel('Epoch')
plt.ylabel('Training Accuracy')
plt.legend(['Training Accuracy'])

"""##Plot 18: Confusion matrix of NN model"""

from sklearn import metrics
# Testing Set Performance

#-----confusion matrix------------------

cm = metrics.confusion_matrix( y_test,y_pred, labels=[0,1])  # 1: left and 0: stayed


# create heatmap
sns.heatmap(cm, annot=True, cmap='YlGnBu', fmt='g')

ax.xaxis.set_label_position('top')

plt.tight_layout()
plt.title('Confusion matrix')
plt.ylabel('Actual label')
plt.xlabel('Predicted label')

# The dimension of this matrix is 2*2 because this model is binary classification. There are two classes 0 and 1.
# Diagonal values represent accurate predictions, while non-diagonal elements are inaccurate predictions.
# In the output, 308 and 20 are actual predictions, and 37 and 3 are incorrect predictions.

print(metrics.classification_report(y_test, y_pred))

#Accuracy
acc_nn= (100 * (accuracy_score(y_test, y_pred)))
acc_nn



"""#Model comparision"""

# accuracy table for each model on testing dataset
from prettytable import PrettyTable

# Specifying the Column Names while initializing the Table
myTable = PrettyTable(["Models ", "Accuracy on Testing Set"])

# Adding rows
myTable.add_row(["Logistic Regression", acc_logReg])
myTable.add_row(["Random Forest", acc_rForest])
myTable.add_row(["Artificial Neural Net", acc_nn])


print(myTable)

"""#Plot 19: ROC curve of models"""

# Receiver Operating Characteristic(ROC) curve is a plot of the true positive rate against the false positive rate.
#It shows the tradeoff between sensitivity and specificity.

# ROC curve: Logistic Regression
plt.figure(figsize=(10,6))
y_pred_proba = model_logisticRegr.predict_proba(x_test)[::,1]
fpr, tpr, _ = metrics.roc_curve(y_test,  y_pred_proba)
auc = metrics.roc_auc_score(y_test, y_pred_proba)
plt.plot(fpr, tpr, label='Logistic Regression (area = %.2f)' %auc)


# ROC curve: Random Forest
y_pred_proba = model_randomForest.predict_proba(x_test)[::,1]
fpr, tpr, _ = metrics.roc_curve(y_test,  y_pred_proba)
auc = metrics.roc_auc_score(y_test, y_pred_proba)

plt.plot(fpr, tpr, label='Random Forest (area = %.2f)' %auc)
plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r', label='Reference line')
plt.xlabel('False positive rate(Specificity)')
plt.ylabel('True positive rate(Sensitivity)')
plt.legend(loc="lower right")
plt.title("ROC curve for model evaluation")
plt.show()




#AUC score for the case is 0.81. AUC score 1 represents a perfect classifier, and 0.5 represents a worthless classifier.
