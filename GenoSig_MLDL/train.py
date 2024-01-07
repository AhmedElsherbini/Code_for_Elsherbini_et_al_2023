#import lib
import pandas as pd
import numpy as np
from utils import *

from sklearn.preprocessing import LabelEncoder, LabelBinarizer, OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
import warnings
from sklearn.model_selection import cross_val_score
#!conda install -c conda-forge xgboost

def trainML_model(f_name):
    data, X, y1, y2, y3, t1, t2, t3 = load_train_data(f_name)
    Features = np.asarray(X, dtype= float)
    Labels1 = np.asarray(y1)
    Labels2 = np.asarray(y2)
    Labels3 = np.asarray(y3)
    Col = data.columns[1:-3]
    
    #let's divide the data 30 % for learning and 70 % for testing
    X_train1, X_val1, y_train1, y_val1 = train_test_split(Features, Labels1, test_size=0.2, random_state=42, stratify= Labels1)
    X_train2, X_val2, y_train2, y_val2 = train_test_split(Features, Labels2, test_size=0.2, random_state=42, stratify= Labels2)

    ##############################################################
    
    clf = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 0)
    rf_clf, rf_train_performance, rf_val_performance, rf_report, rf_cm = train_test(clf, X_train1, y_train1, X_val1, y_val1, t1)
    scores = cross_val_score(rf_clf, Features, Labels1, cv=10)
    print("%0.2f accuracy of RF_clade with a standard deviation of %0.2f" % (scores.mean(), scores.std()))
    df2 = pd.DataFrame(scores)
    df2.to_csv( 'result/CV_accuracy_RF_clade_report_of_%s.csv'%(f_name[7:-4]))
    df = pd.DataFrame(rf_report).transpose()
    df.to_csv( 'result/clade_rf_report_of_%s.csv'%(f_name[7:-4]))
    # save the model to disk
    pickle.dump(rf_clf, open('./models/clade_rf_model.sav', 'wb'))
  

    
    #############################################################  
    
    rf_clf, rf_train_performance, rf_val_performance, rf_report, rf_cm = train_test(clf, X_train2, y_train2, X_val2, y_val2, t2)
    scores = cross_val_score(rf_clf, Features, Labels2, cv=10)
    df2 = pd.DataFrame(scores)
    df = pd.DataFrame(rf_report).transpose()
    df.to_csv( 'result/cont_rf_report_of_%s.csv'%(f_name[7:-4]))
    df2.to_csv( 'result/CV_accuracy_rf_cont_report_of_%s.csv'%(f_name[7:-4]))
    # save the model to disk
    pickle.dump(rf_clf, open('./models/cont_rf_model.sav', 'wb'))
  
  
    #########################################################################


def trainDL_model(f_name):
    data, X, y1, y2, y3, t1, t2, t3 = load_train_data(f_name)
    Features = np.asarray(X, dtype= float)
    Labels1 = np.asarray(y1)
    Labels2 = np.asarray(y2)
    Labels3 = np.asarray(y3)
    Col = data.columns[1:-3]
    
    #let's divide the data 30 % for learning and 70 % for testing
    X_train1, X_val1, y_train1, y_val1 = train_test_split(Features, Labels1, test_size=0.2, random_state=42, stratify= Labels1)
    X_train2, X_val2, y_train2, y_val2 = train_test_split(Features, Labels2, test_size=0.2, random_state=42, stratify= Labels2)


    ##############################################################

    dl_train_performance, dl_val_performance, dl_report, dl_cm , model = train_test_cross_val(X, y1, n_splits=5)
    # Print or use the results as needed
    print("Average Training Performance:", np.mean(dl_train_performance))
    print("Average Validation Performance:", np.mean(dl_val_performance))

    df2 = pd.DataFrame(dl_train_performance)
    df2.to_csv( 'result/CV_accuracy_DL_clade_report_of_%s.csv'%(f_name[7:-4]))
    df = pd.DataFrame(dl_report).transpose()
    df.to_csv( 'result/clade_DL_report_of_%s.csv'%(f_name[7:-4]))
    # save the model to disk

    pickle.dump(model, open('./models/clade_DL_model.sav', 'wb'))


    #################################################################

    dl_train_performance, dl_val_performance, dl_report, dl_cm , model = train_test_cross_val(X, y2, n_splits=5)
    # Print or use the results as needed
    print("Average Training Performance:", np.mean(dl_train_performance))
    print("Average Validation Performance:", np.mean(dl_val_performance))

    df2 = pd.DataFrame(dl_train_performance)
    df2.to_csv( 'result/CV_accuracy_DL_cont_report_of_%s.csv'%(f_name[7:-4]))
    df = pd.DataFrame(dl_report).transpose()
    df.to_csv( 'result/cont_DL_report_of_%s.csv'%(f_name[7:-4]))
    # save the model to disk

    pickle.dump(model, open('./models/cont_DL_model.sav', 'wb'))

  
