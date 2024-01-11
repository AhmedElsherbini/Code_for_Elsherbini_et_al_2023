# Import the argparse library
import argparse
import os
from pca import PCA_model
from train import *
from test import *

#####################
# Create the parser
#os.system("mkdir result models")
directory_path = "result models"

if not os.path.exists(directory_path):
    os.system(f"mkdir {directory_path}")
    print(f"Directory '{directory_path}' created.")
else:
    print(f"Directory '{directory_path}' already exists.")

my_parser = argparse.ArgumentParser(description='Welcome to our tool, make sure your files exsit in the data folder!')
print("$ python3 run.py -x data/x_data.csv -y data/y_data.csv -m dl_train -s 2")
# Add the arguments



my_parser.add_argument('-m','--mode',
                       action='store',
                        metavar='mode',
                       type=str,
                       help='PCA or ML_train or ML_test or DL_train or DL_test')

my_parser.add_argument('-x','--X_input',
                       action='store',
                       metavar='X_input',
                       type=str,
                       help='the path to your file')

my_parser.add_argument('-y','--y_input',
                       action='store',
                       metavar='y_input',
                       type=str,
                       help='the path to your file')

my_parser.add_argument('-s','--splits',
                       action='store',
                       metavar='splits',
                       type=int,
                       help='the number of splits in cross validation')

# Execute the parse_args() method
args = my_parser.parse_args()
###############
fg  = args.mode
f_name = args.X_input
y_name = args.y_input
n_splits = args.splits
################
if (fg == "PCA"):
      PCA_model(f_name)

elif (fg == "ml_train"):
      trainML_model(f_name,y_name)
      
elif(fg == "ml_test"):
    testML_model(f_name)  

elif(fg == "dl_train"):
    trainDL_model(f_name,y_name,n_splits)


elif(fg == "dl_test"):
    testDL_model(f_name)  

