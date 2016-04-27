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

def get_clipped_count(clipped_dic):
	count = 0
	for key, value in clipped_dic.iteritems():
		count += value
	return count


def generate_ref_ngram(reference, n):
	ref_dic = {}
	ref_list = reference.split(" ")
	
	for i in range(0, len(ref_list)-n+1):
		key = ""
		for j in range(0,  n):
			key += ref_list[i+j]
			key += "/"

		if ref_dic.has_key(key):
			ref_dic[key] += 1
		else:
			ref_dic[key] = 1
	return ref_dic


def get_count(candidate, reference, n):
	can_dic, ref_dic, can_len = generate_ngram(candidate, reference, n)
	can_clipped_dic = get_clipped_dic(can_dic, ref_dic)
	can_clipped_count = get_clipped_count(can_clipped_dic)
	return can_clipped_count, can_len

def construct_ref_dic_list(reference_path, n):
	# construct_ref_dic_list(reference_path)
	dic_list = []
	for subdir, dirs, files in os.walk(reference_path):
		for f in files:
			if f == ".DS_Store":
				continue
			path = os.path.join(subdir, f)
			reference = codecs.open(path, encoding='utf-8')
			while 1:
				line = reference.readline()
				if not line:
					break
				line = line.strip()
				refdic = generate_ref_ngram(line, n)
				dic_list.append(refdic)
	for item in dic_list:
		print item
		print "---"
	print len(dic_list)


def main():
	candidate_path = sys.argv[1]
	reference_path = sys.argv[2]
	# candidate = codecs.open(candidate_path, encoding='utf-8')
	# reference = codecs.open(reference_path, encoding='utf-8')

	construct_ref_dic_list(reference_path, 1)
	
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

	# with open('bleu_out.txt', 'w') as fout:
	# 	fout.write(str(score))

if __name__ == "__main__":
    main()