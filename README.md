# Code_for_Elsherbini_et_al.,_2023

## 

**Where did we download the SARS-CoV2 sequences?**

* [here](https://www.gisaid.org/)
   

**How did we prepare our data?**

```python
for file in *.tar.xz ; do tar -xvf $file ; done 
```
Then count each clade sequence.
```python
for file in *.fasta ; do cat $file | grep ">" | wc -l >> count.txt ; done
```

open count.txt and based on the lowest class number we subsampled each class to this number using seqtk tool.

```python
for file in *.fasta ; do seqtk sample -s185207 $file 185207  > sample_$file.fa ; done
```

After subsampling, make sure that the number will be as it is expected. So, let's count again

```python
for file in *.fa ; do cat $file | grep ">" | wc -l >> count.txt ; done
```


**How to produce Di and Tri nucleotide signal using GenoSig?**

Regardless of our work, this step can be used to produce Di and Tri nucleotide signals in just two steps.

This step was done in a normal PC with just 24 GB RAM and Intel core i5-8265U CPU @ 1.60GHz.

You do not need to install anything , just put your Fasta files in the "All" directory and then run the command-line


```python
perl genosig.pl
```
Then

```python
for file in *.csv ; do sed -i -e "/nan/d" $file  ; sed -i 's/^.*.hCoV-19/hCoV-19/' $file   ; sed -i 's/.AltKarlinSignature//' $file   ; sed -i -e 's/^/>/' $file ; cut -f1 < $file > data_$file.fasta ; done
```

This command does three things 1. Remove any line with nan values out of genoSig output. remove any "strings" before the name of the ID. remove the string named "AltKarlinSignature".


**How did we prepare our Metadata?**


This command to extract the first column to make a FAKE file with fasta extension which can be used to extract metadata (aka y data in our workflow) I mean
make sure that the column ID starts with >xxxxxxx in both files. this command to add > in the start of the names

```python

for file in *.csv ; do  cut -f1 < $file > data_$file.fasta ; done
```


Small trick: name them all with start fake

#then get the metadate ((aka y data in our workflow)) out of x files (Di+Tri signal data file) by using this stupid loop 
#make sure you have the file named guide.csv in the same dir of the python script


```python
for file in *.fasta ; do python get_y_data.py -i $file ; done
```

```python
cat *.csv > x_data.csv
cat y_data > y_data.csv
```


so I made a small script that can sepreate them either fix this problem or make a small dataset mini_x and mini_y

**How did we prepare our Machine Learning models?**


```python
python3 run.py -m PCA -i ./data/x_data.csv
python3 run.py -m compare -i ./data/x_data.csv
```
Then based on this comparesion if you find that the RF is the best model is RF is the best  so we make another tool  
In this step we wanted So here we want to make models 

```python
python3 run.py -m train -i ./data/x_data.csv
```
you can find them in the folder models
here we used the whole dataset to make whole prediction results

```python
python3 run.py -m test -i ./data/x_data.csv
```



