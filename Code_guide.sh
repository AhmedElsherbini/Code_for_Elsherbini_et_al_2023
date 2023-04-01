###########################
#part 1
#After you download the data from gisaid 
#https://www.epicov.org/epi3/frontend#2aa67
#unzip
#extraction of super big fasta files may be done in HPC for very big files #you have seven classes exclude S and O
for file in *.tar.xz ; do tar -xvf $file ; done 
#then to count the each clade sequences.
for file in *.fasta ; do echo  $file >> count.txt  ; done
for file in *.fasta ; do cat $file | grep ">" | wc -l >> count.txt ; done
#open count.txt.And based on the lowest class number you subsample each class to this number #in July 182645 # in Nobember 185207 based on class GV
#then I normalized  the comparesion (among the clades not continets) the fasta files by rarefaction/subsampling I mean (what is the smallest clade let's us say 182645)
for file in *.fasta ; do seqtk sample -s185207 $file 185207  > sample_$file.fa ; done
##############qc step#take care extension is fa not FASTA
#Just to make sure that the nimver will be as it is expected like 185207 for all classes
for file in *.fa ; do cat $file | grep ">" | wc -l >> count.txt ; done
#download all sample_files and put them in the dir of genosig
#to move files with large space
tar vc sample* | xz -9v > sample_data.tar.xz
##############
#open the tool genosig
# add the fasta file in the All directory and then run the perl scirpt 
##########################
#this step was done in normal PC with just 24 gRAM
perl genosig.pl
##########################
#the out put of genosig/pasit is csv but they are not clean ....
#this command do three things 1. remove any line with nan values out of genosig output . remove any strings before the name of the ID . remove the string named AltKarlinSignature
for file in *.csv ; do sed -i -e "/nan/d" $file  ; sed -i 's/^.*.hCoV-19/hCoV-19/' $file   ; sed -i 's/.AltKarlinSignature//' $file   ; sed -i -e 's/^/>/' $file ; cut -f1 < $file > data_$file.fasta ; done
#then name all of your files as clean
#end of part 1


###################################################################################################################################################################################
#part 2
#this command to extract the first column to make a FAKE file with fasta extension which can be used to extract metadata (aka y data in our workflow) I mean
#make sure that the column ID starts with >xxxxxxx in both files. this command to add > in the start of the names

for file in *.csv ; do  cut -f1 < $file > data_$file.fasta ; done


#name them all with start fake
####################################
#then get the metadate ((aka y data in our workflow)) out of x files (ditri signal data file) by using this stupid loop 
#make sure you have the file named guide.csv in the same dir of the python script
for file in *.fasta ; do python get_y_data.py -i $file ; done
#end of part 2
###################################################################################################################################################################################
#part 3
#however, ..........................................
#Manually
#before you concat files to each others make sure that only one line header do exsit(ID, AA, AC, AG,.....) or in case of y_data ID, country,
#make sure that both file are csv even if the extension is csv
#make sure that the 1st column is named ID.
#make sure that they fellow the same order/sequences of clades in both files. like in both we start in clade_G and end up with clade_GRY
#make sure that both files the x and the y have the same size

#then
#cat *.csv > x_data.csv
#cat y_data > y_data.csv
#for x_data I observed that there is a problem in the comma sepreation.
#so I made a small script that can sepreate them either fix this problem or make a small dataset mini_x and mini_y

#end of part 3
###################################################################################################################################################################################
#part 4
#part4 is relate to ML we have two tool (one to compare models and two to train and test based on the best model )
#if you put your results into the dir name data
python3 run.py -m PCA -i ./data/x_data.csv
python3 run.py -m compare -i ./data/x_data.csv

###################################################################################
#then based on this comparesion if you find that the RF is the best model is RF is the best  so we make another tool  
#so here we want to make models 
python3 run.py -m train -i ./data/x_data.csv
#you can find them in the folder models
#here we used the whole dataset to make whole prediction results
python3 run.py -m test -i ./data/x_data.csv
####################################################
#to make the confusion matrix #you have to compare the prediction results to the abosulte trurth which is (aka the metadata file of training y_data.csv )

