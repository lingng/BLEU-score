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

def brevity_penalty(candidate, reference):
	if candidate > reference:
		return 1
	else:
		tmp = 1-float(reference)/float(candidate)
		return math.pow(math.e, tmp)

def modified_precision(clipped_count, candidate_length):
	precision = float(clipped_count)/float(candidate_length)
	return math.log(precision)

def get_clipped_dic(candidate_dic, reference_dic):
	clipped_dic = {}
	for key, value in candidate_dic.iteritems():
		if reference_dic.has_key(key):
			ref_v = reference_dic[key]
			clipped_dic[key] = min(value, ref_v)
	return clipped_dic

def get_clipped_dic_count(clipped_dic):
	count = 0
	for key, value in clipped_dic.iteritems():
		count += value
	return count

"""
	Generate Ngram for each line.

	@line: a line of words
	@n: ngram
	return: a dictionary of words and its counts
"""
def generate_ngram(line, n):
	ngram_dic = {}
	word_list = line.split(" ")
	
	for i in range(0, len(word_list)-n+1):
		key = ""
		for j in range(0,  n):
			key += word_list[i+j]
			key += "/"

		if ngram_dic.has_key(key):
			ngram_dic[key] += 1
		else:
			ngram_dic[key] = 1
	return ngram_dic

def generate_n_gram(candidate, reference, n):
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

	
def get_count(candidate, reference, n):
	can_dic, ref_dic, can_len = generate_n_gram(candidate, reference, n)
	can_clipped_dic = get_clipped_dic(can_dic, ref_dic)
	can_clipped_count = get_clipped_dic_count(can_clipped_dic)
	return can_clipped_count, can_len

"""
	Merge dictionary list.

	@dic_base: A list of dictionaries
	@dic_add: A list of dictionaries
	return: A merged list of dictionaries
"""
def merge_dic_list(dic_base, dic_add):
	for i in range(0, len(dic_base)):
		dic_base[i] = merge_dic(dic_base[i], dic_add[i])
	return dic_base

"""
	Merge the base dictionary and new dictionary.
	Use the max value for the key

	@dic_base: Dictionary of words
	@dic_add: Dictionary of words
	return: A merged dictionary
"""
def merge_dic(dic_base, dic_add):
	for key, value in dic_add.iteritems():
		if dic_base.has_key(key):
			dic_base[key] = max(value, dic_base[key])
		else:
			dic_base[key] = value
	return dic_base

"""
	Construct a list of reference ngram dictionaries from the reference path.
	Since there might be multiple references, need to merge the count for each reference.

	@reference_path: The directory to single/multiple refernce(s)
	@n: n-gram
	return: a list of dictionaries
"""
def construct_ref_dic_list(reference_path, n):
	dic_list = []
	for subdir, dirs, files in os.walk(reference_path):
		for f in files:
			if f == ".DS_Store":
				continue
			tmplist = []
			path = os.path.join(subdir, f)
			reference = codecs.open(path, encoding='utf-8')

			while 1:
				line = reference.readline()
				if not line:
					break
				line = line.strip()
				refdic = generate_ngram(line, n)
				tmplist.append(refdic)

			if len(dic_list) == 0:
				dic_list = tmplist
			else:
				dic_list = merge_dic_list(dic_list, tmplist)
	return dic_list

def construct_can_dic_list(candidate_path, n):
	dic_list = []
	candidate = codecs.open(candidate_path, encoding='utf-8')

	while 1:
		line = candidate.readline()
		if not line:
			break
		line = line.strip()
		candic = generate_ngram(line, n)
		dic_list.append(candic)
	return dic_list

def get_clipped_count(canlist, reflist):
	canlen = 0
	clipcount = 0
	for i in range(0, len(canlist)):
		for key, value in canlist[i].iteritems():
			if reflist[i].has_key(key):
				clipcount += min(value, reflist[i][key])
			canlen += value
	return clipcount, canlen

def get_candidate_length(candidate_path):
	length = 0
	candidate = codecs.open(candidate_path, encoding='utf-8')
	while 1:
		line = candidate.readline()
		if not line:
			break
		line = line.strip()
		length += len(line.split(" "))
	return length

def merge_ref_length(length_list, tmplist):
	for i in range(0, len(length_list)):
		length_list[i] = min(length_list[i], tmplist[i])
	return length_list

def get_reference_length(reference_path):
	length_list = []
	for subdir, dirs, files in os.walk(reference_path):
		for f in files:
			if f == ".DS_Store":
				continue
			tmplist = []
			path = os.path.join(subdir, f)
			reference = codecs.open(path, encoding='utf-8')

			while 1:
				line = reference.readline()
				if not line:
					break
				line = line.strip()
				tmplist.append(len(line.split(" ")))
			if len(length_list) == 0:
				length_list = tmplist
			else:
				length_list = merge_ref_length(length_list, tmplist)
	length = 0
	for i in range(0, len(length_list)):
		length += length_list[i]
	return length

def get_candidate_lines(candidate_path):
	count = 0
	candidate = codecs.open(candidate_path, encoding='utf-8')
	while 1:
		line = candidate.readline()
		if not line:
			break
		count += 1
	return count

def get_ref_lines(reference_path):
	for subdir, dirs, files in os.walk(reference_path):
		for f in files:
			if f == ".DS_Store":
				continue
			path = os.path.join(subdir, f)
			reference = codecs.open(path, encoding='utf-8')
			count = 0
			while 1:
				line = reference.readline()
				if not line:
					break
				count += 1
			print count

def main():
	candidate_path = sys.argv[1]
	reference_path = sys.argv[2]

	# single file
	if os.path.isfile(reference_path):
		can_len, ref_len = 0, 0

		uni_c, uni_t = 0, 0
		bi_c, bi_t = 0, 0
		tri_c, tri_t = 0, 0
		four_c, four_t = 0, 0

		candidate = codecs.open(candidate_path, encoding='utf-8')
		reference = codecs.open(reference_path, encoding='utf-8')

		while 1:
			c_line = candidate.readline()
			r_line = reference.readline()
			if not c_line:
				break
			if not r_line:
				break
			c_line = c_line.strip()
			r_line = r_line.strip()
			can_len += len(c_line.split(" "))		
			ref_len += len(r_line.split(" "))

			c_c, t_c = get_count(c_line, r_line, 1)
			uni_c += c_c
			uni_t += t_c

			c_c, t_c = get_count(c_line, r_line, 2)
			bi_c += c_c
			bi_t += t_c

			c_c, t_c = get_count(c_line, r_line, 3)
			tri_c += c_c
			tri_t += t_c

			c_c, t_c = get_count(c_line, r_line, 4)
			four_c += c_c
			four_t += t_c

		uni_p = modified_precision(uni_c, uni_t)
		bi_p = modified_precision(bi_c, bi_t)
		tri_p = modified_precision(tri_c, tri_t)
		four_p = modified_precision(four_c, four_t)
		bp = brevity_penalty(can_len, ref_len)
		print uni_c, uni_t, uni_p
		print bi_c, bi_t, bi_p
		print tri_c, tri_t, tri_p
		print four_c, four_t, four_p
		print can_len, ref_len, bp

		val = [0.25*uni_p, 0.25*bi_p, 0.25*tri_p, 0.25*four_p]

		tmpsum = math.fsum(val)
		score = bp*math.exp(tmpsum)

		print score
		with open('bleu_out.txt', 'w') as fout:
			fout.write(str(score))

	# directory
	else:
		uni_ref_list = construct_ref_dic_list(reference_path, 1)
		bi_ref_list = construct_ref_dic_list(reference_path, 2)
		tri_ref_list = construct_ref_dic_list(reference_path, 3)
		four_ref_list = construct_ref_dic_list(reference_path, 4)

		uni_can_list = construct_can_dic_list(candidate_path, 1)
		bi_can_list = construct_can_dic_list(candidate_path, 2)
		tri_can_list = construct_can_dic_list(candidate_path, 3)
		four_can_list = construct_can_dic_list(candidate_path, 4)
		
		uni_c, uni_t = get_clipped_count(uni_can_list, uni_ref_list)
		bi_c, bi_t = get_clipped_count(bi_can_list, bi_ref_list)
		tri_c, tri_t = get_clipped_count(tri_can_list, tri_ref_list)
		four_c, four_t = get_clipped_count(four_can_list, four_ref_list)

		can_len = get_candidate_length(candidate_path)
		ref_len = get_reference_length(reference_path)

		uni_p = modified_precision(uni_c, uni_t)
		bi_p = modified_precision(bi_c, bi_t)
		tri_p = modified_precision(tri_c, tri_t)
		four_p = modified_precision(four_c, four_t)
		bp = brevity_penalty(can_len, ref_len)

		val = [0.25*uni_p, 0.25*bi_p, 0.25*tri_p, 0.25*four_p]

		tmpsum = math.fsum(val)
		score = bp*math.exp(tmpsum)

		print score
		with open('bleu_out.txt', 'w') as fout:
			fout.write(str(score))
	# print ref_len
	# can_len, ref_len = 0, 0

	# uni_c, uni_t = 0, 0
	# bi_c, bi_t = 0, 0
	# tri_c, tri_t = 0, 0
	# four_c, four_t = 0, 0

	# while 1:
	# 	c_line = candidate.readline()
	# 	r_line = reference.readline()
	# 	if not c_line:
	# 		break
	# 	if not r_line:
	# 		break
	# 	c_line = c_line.strip()
	# 	r_line = r_line.strip()
	# 	can_len += len(c_line.split(" "))		
	# 	ref_len += len(r_line.split(" "))

	# 	c_c, t_c = get_count(c_line, r_line, 1)
	# 	uni_c += c_c
	# 	uni_t += t_c

	# 	c_c, t_c = get_count(c_line, r_line, 2)
	# 	bi_c += c_c
	# 	bi_t += t_c

	# 	c_c, t_c = get_count(c_line, r_line, 3)
	# 	tri_c += c_c
	# 	tri_t += t_c

	# 	c_c, t_c = get_count(c_line, r_line, 4)
	# 	four_c += c_c
	# 	four_t += t_c

	# uni_p = modified_precision(uni_c, uni_t)
	# bi_p = modified_precision(bi_c, bi_t)
	# tri_p = modified_precision(tri_c, tri_t)
	# four_p = modified_precision(four_c, four_t)
	# bp = brevity_penalty(can_len, ref_len)
	# print uni_c, uni_t, uni_p
	# print bi_c, bi_t, bi_p
	# print tri_c, tri_t, tri_p
	# print four_c, four_t, four_p
	# print can_len, ref_len, bp

	# val = [0.25*uni_p, 0.25*bi_p, 0.25*tri_p, 0.25*four_p]

	# tmpsum = math.fsum(val)
	# score = bp*math.exp(tmpsum)

	# print score
	# with open('bleu_out.txt', 'w') as fout:
	# 	fout.write(str(score))

if __name__ == "__main__":
    main()