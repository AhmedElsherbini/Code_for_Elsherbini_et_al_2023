# Code_for_Elsherbini_et_al.,_2023

## 

**Where did we download the SARS-CoV2 sequences?**

After we did register at [GISAID](https://www.gisaid.org/).Then..
  
  ![alt text](https://github.com/AhmedElsherbini/Code_for_Elsherbini_et_al_2023/blob/main/gisaid.jpg)

**How did we preprocess our input sequence data?**

```python
for file in *.tar.xz ; do tar -xvf $file ; done 
```
Then count each clade sequence.
```python
for file in *.fasta ; do cat $file | grep ">" | wc -l >> count.txt ; done
```

open count.txt and based on the lowest class number we subsampled each class to this number using [seqtk](https://github.com/lh3/seqtk) tool.

In our case, it was the GV clade with 185,207 seq.
```python
for file in *.fasta ; do seqtk sample -s185207 $file 185207  > sample_$file.fa ; done
```

After subsampling, make sure that the number will be as it is expected. So, let's count again.

```python
for file in *.fa ; do cat $file | grep ">" | wc -l >> count.txt ; done
```


**How (did we/ to) produce Di and Tri nucleotide signal using GenoSig?**

Regardless of our work, this step can be used to produce Di and Tri nucleotide signals in just two steps.

This step was done in a normal PC with just 24 GB RAM and Intel core i5-8265U CPU @ 1.60GHz.

You do not need to install anything, download the GenoSig.zip (attached) --> unzip it. Then, just put your Fasta files in the "All" directory and then run the command line.


```python
perl genosig.pl
```
Then

```python
for file in *.csv ; do sed -i -e "/nan/d" $file  ; sed -i 's/^.*.hCoV-19/hCoV-19/' $file   ; sed -i 's/.AltKarlinSignature//' $file   ; sed -i -e 's/^/>/' $file ; cut -f1 < $file > data_$file.fasta ; done
```

This command does three things 1. Remove any line with nan values out of GenoSig output, remove any "hCoV-19/hCoV-19" before the name of the ID, and remove the string named "AltKarlinSignature".


**How did we prepare our MetaData?**


This command extracts the first column to make a FAKE file with fasta extension which can be used to extract metadata (aka y data in our in the ML part) I mean
make sure that the column ID starts with >xxxxxxx in both files. this command to add > at the start of the names

```python

for file in *.csv ; do  cut -f1 < $file > data_$file.fasta ; done
```


Small trick: name them all with start fake

Then get the MetaData ((aka y data in our workflow)) out of x files (Di+Tri signal data file) by using this loop 

Make sure you have the file named guide.csv in the same dir of the python script


```python
for file in *.fasta ; do python get_y_data.py -i $file ; done
```

```python
cat *.csv > x_data.csv
cat y_data > y_data.csv
```


So, I made a small script that can separate them either fix this problem or make a small dataset mini_x and mini_y

**How did we prepare our Machine Learning models?**


```python
python3 run.py -m PCA -i ./data/x_data.csv
python3 run.py -m compare -i ./data/x_data.csv
```
Then based on this comparison if you find that the RF is the best model is RF is the best  so we make another tool  
In this step we wanted So here we want to make models 

```python
python3 run.py -m train -i ./data/x_data.csv
```
you can find them in the folder models
here we used the whole dataset to make whole prediction results

```python
python3 run.py -m test -i ./data/x_data.csv
```



