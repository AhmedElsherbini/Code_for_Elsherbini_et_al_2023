#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 19:03:30 2021

@author: ahmed_elsherbini
"""

#####################
# Create the parser


# Add the arguments

import argparse
import os 
import sys
from io import StringIO
from Bio import SeqIO
import regex
import re
import pandas as pd
import csv
#########################################################################################
my_parser = argparse.ArgumentParser(description='Welcome to our tool, make sure your files exsit in the data folder!')

print("Make sure you have guide.csv in the same dir")
my_parser.add_argument('-i','--input',
                       action='store',
                        metavar='input',
                       type=str,
                       help='input file')

args = my_parser.parse_args()
###############

inpt_f = args.input
#################

inclade = inpt_f[:-5]
cmd1 = "sed 's, ,_,g' -i %s" %(inpt_f) #replace the " " with "_" in ID headers inside fasta files sometime in bioythin refuse ID with space!
os.system(cmd1)
clade = [inclade] * int(len([1 for line in open(inpt_f) if line.startswith(">")])) #lets make a clade column actually we download the file clade by clade 
list_id = [] #list of ids
conte = [] #list of countinets
date = [] #list of ID

with open('guide.csv', mode='r') as inp:
    reader = csv.reader(inp)
    dict_from_csv = {rows[0]:rows[1] for rows in reader}

for seq_record in SeqIO.parse(inpt_f, "fasta"):
    x = 0
    list_id.append(">%s"%(seq_record.id)) #let's know the ID for first column
    date.append(str(seq_record.id[-21:-11])) #this is a constant way to get the collection date
    for key in dict_from_csv:
        if any(regex.findall('hCoV-19/%s/'%(key), str(seq_record.id))):
            conte.append(dict_from_csv[key])
            x = 1
    if x == 0: #like if all the keys in the dict are not in this string put "na"
      conte.append("Unknown") 
            
df = pd.DataFrame({"ID":list_id,"Clade":clade,"Continent":conte,"Collection_date":date}) #the order as Dr.myasara wants
df.to_csv('y_data_%s.csv'%(inpt_f[:-6]), index = False)
print("Done for this time")



