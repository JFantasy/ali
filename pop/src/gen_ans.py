#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
from datetime import datetime

def load_user_brandlist(input_file):
	f = open(input_file)
	user_brandlist = {}
	for line in f:
		data = line.split(' ')
		user_brandlist[data[0]] = data[1:len(data)-1]

	f.close()
	return user_brandlist

def load_topk(input_file):
	topk = {}
	f = open(input_file)
	for line in f:
		user, k = line.split(' ')
		topk[user] = int(k)
	f.close()

	return topk

def gen_ans(user_brandlist, topk):
	date = datetime.now().strftime('%m%d_%H%M%S')
	f = open('../ans/' + date + '.txt', 'w')
	for user in user_brandlist:
		k = topk[user]
		if k == 0:
			continue
		f.write(user + '\t' + user_brandlist[user][0])
		for i in range(1, k):
			f.write(',' + user_brandlist[user][i]);
		f.write('\n')

	f.close()

if __name__ == "__main__":
	if len(sys.argv) < 5:
		print "Format Error"
	else:
		topk_file = sys.argv[1]
		sort_matrix_file = sys.argv[2]
		topk = load_topk('../data/topk.txt')
		user_brandlist = load_user_brandlist('../data/sort_matrix_last_2_month.txt')
		gen_ans(user_brandlist, topk)
