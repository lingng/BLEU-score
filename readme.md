## BLEU Score

An implementation of [BLEU evaluation metric](https://aclweb.org/anthology/P/P02/P02-1040.pdf).

#### How to run the code

	$ python calculatebleu.py /path/to/candidate /path/to/reference
	
#### Result comparison

Language |	Candidate |	Reference |	BLEU score
-------- | --------- | ---------- |  ---------- 
German|candidate-1.txt|reference-1.txt|0.151184476557
Greek|candidate-2.txt|reference-2.txt|0.0976570839819
Portuguese|candidate-3.txt|reference-3.txt|0.227803041867

####Notes

* The candidate and reference files will be in UTF-8 encoding.
* You may assume a line-by-line correspondence of sentences between the candidate and reference translations.
