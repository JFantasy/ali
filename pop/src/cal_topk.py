#!/usr/bin/python
#-*- coding: utf-8 -*-

def load_data(input_file):
    fp = open(input_file)
    data = []
    for line in fp:
        data.append(line.split(","))
    fp.close()
    return data

def load_user_brandlist(input_file):
	f = open(input_file)
	user_brandlist = {}
	for line in f:
		data = line.split(' ')
		user_brandlist[data[0]] = data[1:len(data)-1]

	f.close()
	return user_brandlist

#计算用户购买率
def cal_user_buyrate(data):
	buycnt = {}
	for r in data:
		user,brand,behavior,month,day = r[0],r[1],r[2],int(r[3]),int(r[4])
		if user not in buycnt:
			buycnt[user] = [0, 0, 0, 0, 0, 0]
		
		if behavior == '1':
			buycnt[user][month-4] += 1
			buycnt[user][5] += 1.0 / 5

	buyrate = {}
	for user in buycnt:
		buyrate[user] = int(buycnt[user][5])
	
	return buyrate		

def cal_topK(buyrate, user_brandlist, output_file):
	f = open(output_file, 'w')
	for user in user_brandlist:
		list_len = len(user_brandlist[user])
		topK = min(list_len, max(3, min(15, int(buyrate[user])*3)))
		f.write(user + ' ' + str(topK) + '\n')

	f.close()

if __name__ == "__main__":
	data = load_data('../../data/user_brand_date_full.csv')
	user_brandlist = load_user_brandlist('../data/sort_matrix.txt')
	buyrate = cal_user_buyrate(data)
	cal_topK(buyrate, user_brandlist, '../data/topk.txt')

