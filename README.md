# Code_for_Elsherbini_et_al.,_2023

## 


**How did we download the SARS-CoV2 sequences?**

Firstly for the main dataset until 3-Nov-22 (n= 1131185)
After we did register at [GISAID](https://www.gisaid.org/),...
  
  ![alt text](https://github.com/AhmedElsherbini/Code_for_Elsherbini_et_al_2023/blob/main/gisaid.jpg)

Clear. right?
What about the validation dataset (n = 67,399) from 4-Nov-2022 to 30-11-2023?

Here is an example of how we downloaded Clade G.
![alt text](https://github.com/AhmedElsherbini/Code_for_Elsherbini_et_al_2023/blob/main/Slide16.jpg)

**How did we preprocess our input sequence data for the main dataset?**

Firstly, we needed to unzip our data.

```bash
for file in *.tar.xz ; do tar -xvf $file ; done 
```
We have 9 files and each file represents one clade, let's count each clade.

```bash
for file in *.fasta ; do cat $file | grep ">" | wc -l >> count.txt ; done
```
We decided to exclude (S and O), as the first had very few sequences in relative to the smallest clade (< 10 % to GV clade) and the second represented unclassified/noisy isolates and both clades did not belong to the trajectory of virus evolution. Also, no sequence data for very early clades like (L and V).

Ok, now we need to normalize our data. Then,..

Open count.txt and based on the smallest clade, we subsampled each clade using [seqtk](https://github.com/lh3/seqtk) tool.

In our case, it was the GV clade with 185,207 seq.

```bash
for file in *.fasta ; do seqtk sample -s185207 $file 185207  > sample_$file.fa ; done
```

After subsampling, make sure that the number will be as it is expected. So, let's count again.

```bash
for file in *.fa ; do cat $file | grep ">" | wc -l >> count.txt ; done
```


**How (did we/ to) produce Di and Tri nucleotide signal using GenoSig?**

Regardless of this work, this step can be used to produce Di and Tri nucleotide signals in just two steps.

Important: GenoSig is a variant of [PaSiT](https://academic.oup.com/bioinformatics/article/36/8/2337/5695704) and both of them are developed by [Gleb Goussarav](https://github.com/GlebGoussarov).

Just in a normal PC (24 GB RAM and Intel core i5-8265U CPU @ 1.60GHz), it took ~7 minutes (wall-clock time) for a dataset of ~37.8 GB).

You do not need to install anything, download the GenoSig.zip (attached) --> unzip it. Then, just put your Fasta files in the "All" directory and then run the command line.


```bash
perl genosig.pl
```
Then,..

```bash
for file in *.csv ; do sed -i -e "/nan/d" $file  ; sed -i 's/^.*.hCoV-19/hCoV-19/' $file   ; sed -i 's/.AltKarlinSignature//' $file   ; sed -i -e 's/^/>/' $file ; cut -f1 < $file > data_$file.fasta ; done
```

This command does three things. Firstly, remove any line with nan values out of GenoSig output, remove any "hCoV-19/hCoV-19" before the name of the ID, and remove the string named "AltKarlinSignature".

But, it does also produce a FASTA file with just headers, why?

This is step 1. in the next phase.

**How did we prepare our MetaData?**

Back again to the SARS-CoV2 project...

This is a crucial step. Well, the MetaData in our work is two information the clade and the continent. The clade was concluded from the name of the Fasta file, while the continent needed a lot work.

How did we get the continent? From the header of the fasta file (>SARS-COV-3356667-EGYPT-....) you can find the country. right? So, using a Python script we looped over each header in all of the files and based on a country-continent association (aka guide.csv) file, we were able to conclude for each sequence which continent it belong.

These steps explain in detail this process.

Step.1:

This command extracts the first column to make a FAKE file with Fasta extension which can be used to extract metadata (aka y data in our next section related to Machine learning) I mean
make sure that the column ID starts with >xxxxxxx in both files. this command to add > at the start of the names

```bash

for file in *.csv ; do  cut -f1 < $file > data_$file.fasta ; done
```


Small trick: name them all with start fake

Then get the MetaData ((aka y data in our workflow)) out of x files (Di+Tri signal data file) by using this loop 

Step.2:

So, let's extract the MetaData. 
Make sure you have the file named guide.csv in the same dir of the python script

Important: Make sure that the name of the file is the clade.

```python
for file in *.fasta ; do python get_y_data.py -i $file ; done
```

Step.3:

Let's merge.

```bash
cat *.csv > x_data.csv
cat y_data > y_data.csv
```
Always remember that the X file is the Di and Tri frequency signal and the Y file is the MetaData

So, I made a small script that can separate them either fix this problem or make a small dataset mini_x and mini_y

**How did we prepare our Machine Learning models?**


![alt text](https://github.com/AhmedElsherbini/Code_for_Elsherbini_et_al_2023/blob/main/Slide8.jpg)

Well, there are plenty of GUI/CLI platforms for ML training or testing, you can use whatever platform you like according to your skills and preferences.

Important: the ML scripts in our work were developed initially by [Ahmed M. Elshal](https://github.com/Ahmed-M-Elshal). 

In this work, with python3 scikit-learn mainly, we compared the ML algorithms using (compare_ML_models.zip). As Random Forest (RF) turned out to be the best model, we made (ML_anlysis.zip) which we can train and test using RF only.


To get started with our ML work, follow these steps :

Clone the repository

```bash
git clone https://github.com/AhmedElsherbini/Code_for_Elsherbini_et_al_2023.git
cd Code_for_Elsherbini_et_al_2023
cd ML_anlysis
```
Create the conda environment with the dependencies

```bash
conda env create -f enviroment.yml
```
Activate the conda environment

```bash
conda activate GenoSig_MLDL
```




Check the table below:
- Note: Arguments are case sensitive, only write in CAPSLOCK mode.

| Argument  |  Function |
|---|---|
| -x | the data input to the model including the features|
|  -y |  The label/target/class that the model will predict|
| -m  |  The tool mood. We have different modes listed in (PCA , ML_train , ML_test , DL_train or DL_test) |
| -s  |  Number of splits which required to the cross validation|(10 is the most used)

**Examples:**

```python
python3 run.py -m PCA -x ./data/x_data.csv -y ./data/y_data.csv 
```
DL and RF were the best, therefore we used them for models.

Take care: RF with 100 estimators is quite slow more than DL, especially with cross-validation. 

```python
python3 run.py -m DL_train -x ./data/x_data.csv -y ./data/y_data.csv -s 10
```

Here to test the whole dataset against the computed model, use it afterwards for the confusion matrix, and draw some Chord graphs.

```python
python3 run.py -m DL_test -x ./data/x_data.csv -y ./data/y_data.csv
```

**How did we make the confusion matrix and Chord diagram?**

In Excel or CSV, just we copied the ground truth and compared it to the predicted class from the previous "run.py -m test...." command.

Then we used this up there R script named **confusion_matrix.html**.

**How did we make the statistics?**

Up there, the R script is named **Stat.html**.


## Contributing
Pull requests are very welcome. 

For major changes, please open an issue (or Email me) first to discuss what you would like to change.

Contact me directly by email: drahmedsherbini@yahoo.com

