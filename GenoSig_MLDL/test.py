#import lib
import numpy as np
from utils import *
import pickle

def testML_model(f_name):
    data, X = load_test_data(f_name)
    X_test = np.asarray(X, dtype= float)
    
    ##############################################################
    # load the model from disk
    loaded_model = pickle.load(open('./models/clade_rf_model.sav', 'rb'))
    y_pre = loaded_model.predict(X_test)
    y_pre = pd.DataFrame(y_pre, columns= ['RFCLADE'])
    result = pd.concat([data[['ID']], y_pre[['RFCLADE']]], axis = 1,)
    
    # load the model from disk
    loaded_model = pickle.load(open('./models/cont_rf_model.sav', 'rb'))
    y_pre = loaded_model.predict(X_test)
    y_pre = pd.DataFrame(y_pre, columns= ['RFCONT'])
    result = pd.concat([result, y_pre[['RFCONT']]], axis = 1,)
    result.to_csv('./result/result_rf.csv', index=False)


def testDL_model(f_name):
    data, X = load_test_data(f_name)
    X_test = np.asarray(X, dtype= float)
    
    ##############################################################
    # load the model from disk
    loaded_model = pickle.load(open('./models/clade_DL_model.sav', 'rb'))
    y_pre = loaded_model.predict(X_test)
    y_pre = y_pre.argmax(axis=1)
    y_pre = pd.DataFrame(y_pre, columns= ['RFCLADE'])
    result = pd.concat([data[['ID']], y_pre[['RFCLADE']]], axis = 1,)
    
    # load the model from disk
    loaded_model = pickle.load(open('./models/cont_DL_model.sav', 'rb'))
    y_pre = loaded_model.predict(X_test)
    y_pre = y_pre.argmax(axis=1)
    y_pre = pd.DataFrame(y_pre, columns= ['RFCONT'])
    result = pd.concat([result, y_pre[['RFCONT']]], axis = 1,)
    result.to_csv('./result/result_dl.csv', index=False)