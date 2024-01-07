#import lib
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
from sklearn.utils import shuffle
from sklearn import tree
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder



#loading the training dataset
####################
def load_train_data(f_name):
    X = pd.read_csv(f_name)
    
    y = pd.read_csv(f_name.replace('x','y'))
    data = pd.merge(X, y, on='ID')
    data = shuffle(data)
    
    y1 = data.iloc[:, -3]
   
    y2 = data.iloc[:, -2]
    
    y3 = data.iloc[:, -1]
    
    X = data.iloc[:, 1:-3]
    #X = X.drop('ID',axis = 1)
    X = X.fillna(X.mean())
    
    t1 = list(np.unique(y1))
    t2 = list(np.unique(y2))
    t3 = list(np.unique(y3))
    return data, X, y1, y2, y3, t1, t2, t3


#loading the test dataset
####################
def load_test_data(f_name):
    data = pd.read_csv(f_name)
    features = data.iloc[:, 1:]
    features = features.fillna(features.mean())
    return data, features

#plot the pca figure
####################
def plot_2d_pca(pca, data, targets, f_name, figsize = (8,8)):
    fig = plt.figure(figsize = figsize)
    ax = fig.add_subplot(1,1,1) 
    ax.set_xlabel('PCA1=%f'% pca.explained_variance_ratio_[0], fontsize = 15)
    ax.set_ylabel('PCA2=%f'% pca.explained_variance_ratio_[1], fontsize = 15)
    colors = ["r","g","y","b","c","k","#D226D2", "#D2CF26", "#EAD66A","#33FFDD","#90FF33","#FFBE33","#CEE3CE"] #if you draw more than 12 class, ext. will be omitted in PCA unless you add col.code
    
    for target, color in zip(targets,colors):
        indicesToKeep = data['class'] == target
        color = np.random.rand(3,)
        ax.scatter(data.loc[indicesToKeep, 'pc1']
                   , data.loc[indicesToKeep, 'pc2']
                   , c = [color]
                   , s = 50)
    ax.legend(targets)
    ax.grid()
    plt.savefig("result/2D_PCA_of_%s.jpg" %(f_name)) #save your file!
    plt.close()


#train the ML models and return some usefule metadata
def train_test(clf, X_train, y_train, X_val, y_val, targets):
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_train)
    train_acc = accuracy_score(y_train, y_pred)
    train_performance = train_acc
    
    y_pred = clf.predict(X_val)
    val_acc = accuracy_score(y_val, y_pred)
    val_performance = val_acc
    c_report = classification_report(y_val, y_pred, target_names = targets, output_dict=True)
    cm = confusion_matrix(y_val, y_pred)
    
    return clf, train_performance, val_performance, c_report, cm


#print the ML performance
def represent_performance(clf_name, train_performance, val_performance):
    print(clf_name,'_train_accuracy =', train_performance)
    print(clf_name,'_valid_accuracy =', val_performance)
    




# Define your deep learning model
def create_model(input_dim, num_classes):
    # Build the neural network model
    model = Sequential()
    model.add(Dense(1024, input_dim=input_dim, activation='relu'))
    model.add(Dense(512, activation='relu'))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(num_classes, activation='sigmoid'))  # Use num_classes instead of y.shape

    # Compile the model
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    return model

#train the ML models and return some usefule metadata
def train_test_dl(clf, X_train, y_train, X_val, y_val, targets):
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_train)
    y_pred = y_pred.argmax(axis=1)
    train_acc = accuracy_score(y_train, y_pred)
    train_performance = train_acc
    
    y_pred = clf.predict(X_val)
    y_pred = y_pred.argmax(axis=1)
    val_acc = accuracy_score(y_val, y_pred)
    val_performance = val_acc
    c_report = classification_report(y_val, y_pred, target_names = targets, output_dict=True)
    cm = confusion_matrix(y_val, y_pred)
    
    return clf, train_performance, val_performance, c_report, cm

# Train and evaluate the model using cross-validation
def train_test_cross_val(X, y, n_splits=5):
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    
    train_performances = []
    val_performances = []
    c_reports = []
    cms = []

    X = X.values

    # Create a LabelEncoder object
    label_encoder = LabelEncoder()

    # Fit and transform the labels to numerical values
    y = label_encoder.fit_transform(y)
    
    
    targets = np.unique(label_encoder.inverse_transform(y))

    

    for train_index, val_index in skf.split(X, y):
        X_train, X_val = X[train_index], X[val_index]
        y_train, y_val = y[train_index], y[val_index]

        model = create_model(input_dim=X.shape[1], num_classes=len(targets))
        clf, train_performance, val_performance, c_report, cm = train_test_dl(model, X_train, y_train, X_val, y_val, targets)

        train_performances.append(train_performance)
        val_performances.append(val_performance)
        c_reports.append(c_report)
        cms.append(cm)
    pickle.dump(model, open('./models/cont_dl_model.sav', 'wb'))
    return train_performances, val_performances, c_reports, cms , model