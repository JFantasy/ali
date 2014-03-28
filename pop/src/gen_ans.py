#!/usr/bin/python
#-*- coding: utf-8 -*-

from datetime import datetime

def load_data(input_file):
    f = open(input_file)
    data = []
    for line in f:
        data.append(line.split(","))
    f.close()
    return data

def load_buyrate(input_file):
	f = open(input_file)
	buyrate = {}
	for line in f:
		user, rate = line.split(' ')
		buyrate[user] = float(rate)

	return buyrate

def load_sort_matrix(input_file):
	f = open(input_file)
	user_brandlist = {}
	for line in f:
		data = line.split(' ')
		user_brandlist[data[0]] = data[1:len(data)-1]

	f.close()
	return user_brandlist

def gen_ans(buyrate, user_brandlist):

	date = datetime.now().strftime('%Y%m%d%H%M%S')
	f = open('../ans/submit_' + date + '.txt', 'w')
	for user in user_brandlist:
		topK = min(len(user_brandlist[user]), max(5,  min(10, int(len(user_brandlist[user]) * buyrate[user]))))
		if topK == 0:
			continue
		f.write(user + ' ' + user_brandlist[user][0])
		for i in range(1, topK):
			f.write(',' + user_brandlist[user][i]);
		f.write('\n')

	f.close()

if __name__ == "__main__":

	data = load_data('../data/ali_order_brand_date_full.csv')
	buyrate = load_buyrate('../data/buyrate.txt')
	user_brandlist = load_sort_matrix('../data/sort_matrix.txt')
	gen_ans(buyrate, user_brandlist)
