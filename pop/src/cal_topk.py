#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys

def load_data(input_file):
    fp = open(input_file)
    data = []
    for line in fp:
        data.append(line.strip().split(","))
    fp.close()
    return data

def load_user_brandlist(input_file):
	f = open(input_file)
	user_brandlist = {}
	for line in f:
		data = line.split()
		user_brandlist[data[0]] = data[1:]
	f.close()
	return user_brandlist

#计算用户购买率
def cal_user_buyrate(data):
	buycnt = {}
	for r in data:
		user, brand, behavior, month, day = r[0],r[1],r[2],int(r[3]),int(r[4])
		if user not in buycnt:
			buycnt[user] = [0, 0, 0, 0, 0, 0]
		
		if behavior == '1':
			buycnt[user][month-4] += 1
			
			#add the total buy behavior
			buycnt[user][5] += 1

	buyrate = {}
	for user in buycnt:
		buyrate[user] = int((buycnt[user][2] + buycnt[user][3] + buycnt[user][4]) / 2.5)
	
	return buyrate		

def cal_topK(data, user_brandlist, min_topk, max_topk):
	result = {}
	buyrate = cal_user_buyrate(data)
	for user in user_brandlist:
		list_len = len(user_brandlist[user])
		topK = min(list_len, min(max_topk, buyrate[user]))
		if topK < min_topk:
			topK = min(list_len, min_topk)
		result[user] = topK
	return result

def output(output_file, result):
	f = open(output_file, 'w')
	for user in result:
		f.write(user + ' ' + str(result[user]) + '\n')
	f.close()

if __name__ == "__main__":
	if len(sys.argv) != 6:
		print "Format Error"
		data = load_data('../data/ali_order_brand_date_last_2_month.csv')
		user_brandlist = load_user_brandlist('../data/sort_matrix_last_2_month.txt')
		buyrate = cal_user_buyrate(data)
		cal_topK(buyrate, user_brandlist, '../data/topk.txt', 3, 7)
	else:
		input_file = sys.argv[1]
		sort_matrix_file = sys.argv[2]
		topk_file = sys.argv[3]
		min_topk = int(sys.argv[4])
		max_topk = int(sys.argv[5]) 
		# data = load_data('../data/ali_order_brand_date_last_2_month.csv')
		# user_brandlist = load_user_brandlist('../data/sort_matrix_last_2_month.txt')
		# buyrate = cal_user_buyrate(data)
		# cal_topK(buyrate, user_brandlist, '../data/topk.txt')
		data = load_data(input_file)
		user_brandlist = load_user_brandlist(sort_matrix_file)
		result = cal_topK(data, user_brandlist, min_topk, max_topk)
		output(topk_file, result)
