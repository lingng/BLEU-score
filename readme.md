## BLEU Score

An implementation of [BLEU evaluation metric](https://aclweb.org/anthology/P/P02/P02-1040.pdf).

#### How to run the code

	$ python calculatebleu.py /path/to/candidate /path/to/reference
	
The first parameter will be the path to the candidate translation (a single file), and the second parameter will be a path to the reference translations (either a single file, or a directory if there are multiple reference translations). 

The program will write an output file called bleu_out.txt which contains a single floating point number, representing the BLEU score of the candidate translation relative to the set of reference translations.
	
#### Result comparison

Language |	Candidate |	Reference |	BLEU score
-------- | --------- | ---------- |  ---------- 
German|candidate-1.txt|reference-1.txt|0.151184476557
Greek|candidate-2.txt|reference-2.txt|0.0976570839819
Portuguese|candidate-3.txt|reference-3.txt|0.227803041867

####Notes

* The candidate and reference files will be in UTF-8 encoding.
* You may assume a line-by-line correspondence of sentences between the candidate and reference translations.
