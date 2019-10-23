import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model.logistic import LogisticRegressionCV
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, f1_score
from sklearn import svm
from sklearn.linear_model import Perceptron

from sklearn.metrics import f1_score, classification_report

from sklearn.ensemble import RandomForestClassifier

import torch
from sklearn.naive_bayes import MultinomialNB
from torch.autograd import Variable
from torchvision import datasets, transforms
from torch import nn, optim
import torch.nn.functional as F

import matplotlib.pyplot as plt

df = pd.read_csv('data/test.csv')
#df.rename(columns = {0:'label',1: 'text'}, inplace = True)

X = df['responseBody'].astype('U')
y = df['attacked']

#print(df.loc[df['label'] == 'ham'].count())

seed = 5
test_size = 0.33
#split dataset into train and test sets
X_train_raw, X_test_raw, y_train, y_test = train_test_split(X, y,
                                                            test_size=test_size,
                                                            random_state=seed)

#Convert to a matrix of TF-IDF features
vectorizer = TfidfVectorizer(min_df=2, ngram_range=(1, 5), stop_words='english', max_features= 50000,strip_accents='unicode', norm='l2')
X_train = vectorizer.fit_transform(X_train_raw)
X_test = vectorizer.transform(X_test_raw)

print(X_train.shape)
#Model training

# Naive Bayes
mnb_classifier = MultinomialNB()
mnb_classifier.fit(X_train, y_train)
mnb_predictions =  mnb_classifier.predict(X_test)
score = accuracy_score(y_test, mnb_predictions)
f_score = f1_score(y_test, mnb_predictions, average='micro')
print("The accuracy score (MultinomialNB) is:", score)
print("The F score-Micro (MultinomialNB) is:", f_score)


# Random Forest
rf_clf = RandomForestClassifier(n_estimators=100, max_depth=2, random_state=0)
rf_clf.fit(X_train, y_train)
rf_predictions =  rf_clf.predict(X_test)
score = accuracy_score(y_test, rf_predictions)
f_score = f1_score(y_test, rf_predictions, average='micro')
print("The accuracy score (Random Forest) is:", score)
print("The F score-Micro (Random Forest) is:", f_score)

from sklearn import metrics


# Logistic Regression
lr_classifier = LogisticRegressionCV()
lr_classifier.fit(X_train, y_train)
lt_predictions = lr_classifier.predict(X_test)
score = accuracy_score(y_test, lt_predictions)
f_score = f1_score(y_test, lt_predictions, average='micro')
print("The accuracy score (Logistic Regression) is:", score)
print("The F score-Micro (Logistic Regression) is:", f_score)

cnf_matrix = metrics.confusion_matrix(y_test, rf_predictions)

# import required modules
import seaborn as sns

class_names=[0,1] # name  of classes
fig, ax = plt.subplots()
tick_marks = np.arange(len(class_names))
plt.xticks(tick_marks, class_names)
plt.yticks(tick_marks, class_names)
# create heatmap
sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="YlGnBu" ,fmt='g')
ax.xaxis.set_label_position("top")
plt.tight_layout()
plt.title('Confusion matrix', y=1.1)
plt.ylabel('Actual label')
plt.xlabel('Predicted label')


print("Accuracy:",metrics.accuracy_score(y_test, lt_predictions))
print("Precision:",metrics.precision_score(y_test, lt_predictions))
print("Recall:",metrics.recall_score(y_test, lt_predictions))


y_pred_proba = lr_classifier.predict_proba(X_test)[::,1]
fpr, tpr, _ = metrics.roc_curve(y_test,  y_pred_proba)
auc = metrics.roc_auc_score(y_test, y_pred_proba)
plt.plot(fpr,tpr,label="data 1, auc="+str(auc))
plt.legend(loc=4)
plt.show()

# Perceptron
perceptron_classifier = Perceptron(random_state=11)
perceptron_classifier.fit(X_train, y_train)
perc_predictions = perceptron_classifier.predict(X_test)
score = accuracy_score(y_test, perc_predictions)
f_score = f1_score(y_test, perc_predictions, average='micro')
print("The accuracy score (Perceptron) is:", score)
print("The F score-Micro (Perceptron) is:", f_score)

# Support Vector Machine
svm_classifier = svm.SVC(gamma='scale')
svm_classifier.fit(X_train, y_train)
svm_predictions = svm_classifier.predict(X_test)
score = accuracy_score(y_test, svm_predictions)
f_score = f1_score(y_test, svm_predictions, average='micro')
print("The accuracy score (SVM) is:", score)
print("The F score-Micro (SVM) is:", f_score)

#print('Number of spam messages: %s' % df[df[0] == 1][0].count())
#print('Number of ham messages: %s' % df[df[0] == 0][0].count())


class Model(nn.Module):
    def __init__(self, input, hidden, output):
        super(Model, self).__init__()
        self.l1 = nn.Linear(input, hidden)
        self.l2 = nn.Linear(hidden, hidden)
        self.l3 = nn.Linear(hidden, output)

    def forward(self, x):
        out = F.relu(self.l1(x))
        out = F.relu(self.l2(out))
        out = self.l3(out)
        return out
input = 1000
hidden=100
output = 2

model = Model(input, hidden, output)
print(model)

features_train, features_test, labels_train, labels_test = train_test_split(X, y, shuffle=True, random_state=34)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
criterion = nn.CrossEntropyLoss()

def train(epochs):
    x_train = Variable(torch.from_numpy(features_train)).float()
    y_train = Variable(torch.from_numpy(labels_train)).long()
    model.train()
    for epoch in range(epochs):
        optimizer.zero_grad()
        y_pred = model(x_train)
        loss = criterion(y_pred, y_train)
        print ("epoch #",epoch)
        print ("loss: ", loss.item())
        pred = torch.max(y_pred, 1)[1].eq(y_train).sum()
        print ("acc:(%) ", 100*pred/len(x_train))
        loss.backward()
        optimizer.step()

def test(epochs):
    model.eval()
    x_test = Variable(torch.from_numpy(features_test)).float()
    y_test = Variable(torch.from_numpy(labels_test)).long()
    for epoch in range(epochs):
        with torch.no_grad():
            y_pred = model(x_test)
            loss = criterion(y_pred, y_test)
            print ("epoch #",epoch)
            print ("loss: ", loss.item())
            pred = torch.max(y_pred, 1)[1].eq(y_test).sum()
            print ("acc (%): ", 100*pred/len(x_test))

            
def y_prediction_nn_model(model, x_data):
    return model(x_data)
  
def save_nn_model(model, path):
    torch.save(model.state_dict(), PATH)
 
def load_nn_model(path):
    input = 1000
    hidden=100
    output = 2
    model = Model(input, hidden, output)
    
    model.load_state_dict(torch.load(path))
    model.eval()
