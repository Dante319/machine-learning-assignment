import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
import pandas as pd

df = pd.read_csv('dataset/winequality-red.csv')
df.info()
print(df.head())
print(df.describe())

f,ax = plt.subplots(figsize=(18, 18))
sns.heatmap(df.corr(), annot=True, linewidths=.5, fmt= '.1f',ax=ax)
plt.show()
sns.barplot(x='quality', y='sulphates',data=df)
plt.show()
sns.barplot(x = 'quality', y='volatile acidity', data = df)
plt.show()
sns.barplot(x = 'quality', y='alcohol', data = df)
plt.show()
#showing counts before categorize quality column
df['quality'].value_counts()
#categorize wine quality
bins = (2,6.5,8)
group_names = ['bad','good']
categories = pd.cut(df['quality'], bins, labels = group_names)
df['quality'] = categories
#after categorize
df['quality'].value_counts()
#barplot of quality vs alcohol.
# more alcohol, better red wine
sns.barplot(x='quality', y='alcohol',data=df)
plt.show()
#barplot of quality vs volatile acidity
#less volatile acidity, better red wine.
sns.barplot(x='quality', y='volatile acidity',data=df)
plt.show()
#splitting data to X ve y
X = df.drop(['quality'], axis = 1)
y = df['quality']
# Encoding our dependent variable:Quality column
from sklearn.preprocessing import LabelEncoder
labelencoder_y = LabelEncoder()
y = labelencoder_y.fit_transform(y)
print(y)

# Splitting the dataset into the Training set and Test set.%20 of dataset for test set,%80 for training set.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# Feature Scaling to X_train and X_test to classify better.
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

#I'll use Kernel SVM model to classify.
# Fitting Kernel SVM to the Training set
from sklearn.svm import SVC
classifier = SVC(kernel = 'rbf', random_state = 0)
classifier.fit(X_train, y_train)
#Predicting the Test Set
y_pred = classifier.predict(X_test)

#making confusing matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm,annot=True,fmt='2.0f')
plt.show()

#k-Fold cross validation for improving our model
from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator = classifier, X = X_train,
                             y = y_train, cv = 10)
#we can see model's average accuracy
print("Mean Accuracy: ")
print(accuracies.mean())

#here is the model's standart deviation
print("Standard Deviation: ")
print(accuracies.std())

#Grid search for best model and parameters
from sklearn.model_selection import GridSearchCV
parameters = [{'C': [1, 10, 100, 1000], 'kernel': ['linear']},
              {'C': [1, 10, 100, 1000], 'kernel': ['rbf'],
               'gamma': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]}]
grid_search = GridSearchCV(estimator = classifier,
                           param_grid = parameters,
                           scoring = 'accuracy',
                           cv = 10,)
grid_search.fit(X_train, y_train)
best_accuracy = grid_search.best_score_
best_parameters = grid_search.best_params_
#here is the best accuracy
print("Best Accuracy: ")
print(best_accuracy)

#and here is best parameters
print("Best Parameters:")
print(best_parameters)

# Fitting Kernel SVM to the Training set with best parameters
from sklearn.svm import SVC
classifier = SVC(kernel = 'rbf', random_state = 0, gamma = 0.9)
#classifier1 = SVC(kernel = 'linear', random_state = 0, gamma = 0.6)
classifier.fit(X_train, y_train)
#classifier1.fit(X_train, y_train)

#Predicting the Test Set
y_pred = classifier.predict(X_test)
#y_pred1 = classifier.predict(X_test)

#making confusing matrix again
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm,annot=True,fmt='2.0f')
plt.show()
#cm = confusion_matrix(y_test, y_pred1)
#sns.heatmap(cm,annot=True,fmt='2.0f')
#plt.show()