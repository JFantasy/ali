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
	# f = open('../data/buy_month_stat.txt', 'w')
	# for user in buycnt:
	# 	f.write(user + ' ')
	# 	for i in range(5):
	# 		f.write(str(i+4) + ':' + str(buycnt[user][i]) + ' ')
	# 	f.write('\n')
	
	# f.close()

	#min_max normalization
	# min_tot = 10000
	# max_tot = 0
	# min_buy = 10000
	# max_buy = 0
	# for user in buycnt:
	# 	min_tot = min(min_tot, buycnt[user][1])
	# 	max_tot = max(max_tot, buycnt[user][1])
	# 	min_buy = min(min_buy, buycnt[user][0])
	# 	max_buy = max(max_buy, buycnt[user][0])

	# buyrate = {}
	# #output buy rate

	# alpha = 0.5
	# for user in buycnt:
	# 	buy_norm = buycnt[user][0]*1.0/(max_buy - min_buy)
	# 	tot_norm = buycnt[user][1]*1.0/(max_tot - min_tot)
	# 	buycnt_norm = (1 + alpha * alpha) * (buy_norm * tot_norm) / (alpha * alpha * buy_norm + tot_norm)
	# 	buyrate[user] = buycnt_norm;
	
	# return buyrate
	#fo.close()

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

