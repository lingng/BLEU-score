#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CSCI 544 Homework 8 calculatebleu.py
Yuting ZHANG
6099111047
yutingz@usc.edu
"""

import sys
import os
import codecs
import math

# def brevity_penalty(candidate, reference):
# 	ref_len = len(reference.split(" "))
# 	can_len = len(candidate.split(" "))
# 	penalty = min(1, float(can_len)/float(ref_len))
# 	return penalty

def get_clipped_count(candidate_dic, reference_dic):
	clipped_dic = {}
	for key, value in candidate_dic.iteritems():
		if reference_dic.has_key(key):
			ref_v = reference_dic[key]
			clipped_dic[key] = min(value, ref_v)

	return clipped_dic

"""
	Generate ngrams for candidate and reference.
	Use / to separate each word to generate key for the dictionary. # List is not hashable

	@candidate: candidate translation sentence
	@reference: reference translation sentence
	@n: number for the ngram
	return: [can_dic, ref_dic, can_len]
		can_dic: candidate ngram count dictionary
		ref_dic: reference ngram count dictionary
		can_len: the number of ngrams generated from the candidate translation
"""
def generate_ngram(candidate, reference, n):
	can_dic = {}
	ref_dic = {}
	can_list = candidate.split(" ")
	ref_list = reference.split(" ")
	can_len = 0
	
	for i in range(0, len(can_list)-n+1):
		key = ""
		for j in range(0, n):
			key += can_list[i+j]
			key += "/"
		can_len += 1
		if can_dic.has_key(key):
			can_dic[key] += 1
		else:
			can_dic[key] = 1

	for i in range(0, len(ref_list)-n+1):
		key = ""
		for j in range(0,  n):
			key += ref_list[i+j]
			key += "/"

		if ref_dic.has_key(key):
			ref_dic[key] += 1
		else:
			ref_dic[key] = 1
	return can_dic, ref_dic, can_len


def get_count(candidate, reference):
	candidate = candidate.strip()
	reference = reference.strip()
	uni_c_dic, uni_r_dic, uni_c_len = generate_ngram(candidate, reference, 1)
	uni_clipped_dic = get_clipped_count(uni_c_dic, uni_r_dic)

	bi_c_dic, bi_r_dic, bi_c_len = generate_ngram(candidate, reference, 2)
	bi_clipped_dic = get_clipped_count(bi_c_dic, bi_r_dic)

	tri_c_dic, tri_r_dic, tri_c_len = generate_ngram(candidate, reference, 3)
	tri_clipped_dic = get_clipped_count(tri_c_dic, tri_r_dic)

	four_c_dic, four_r_dic, four_c_len = generate_ngram(candidate, reference, 4)
	four_clipped_dic = get_clipped_count(four_c_dic, four_r_dic)
	print uni_clipped_dic
	print bi_clipped_dic
	print tri_clipped_dic
	print four_clipped_dic
	print "----"
	# penalty = brevity_penalty(candidate, reference)

def main():
	candidate_path = sys.argv[1]
	reference_path = sys.argv[2]
	candidate = codecs.open(candidate_path, encoding='utf-8')
	reference = codecs.open(reference_path, encoding='utf-8')
	# candidate = open(candidate_path, 'r')
	# reference = open(reference_path, 'r')
	while 1:
		c_line = candidate.readline()
		r_line = reference.readline()
		if not c_line:
			break
		if not r_line:
			break
		count = get_count(c_line, r_line)


if __name__ == "__main__":
    main()