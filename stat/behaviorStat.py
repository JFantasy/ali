#!/usr/bin/python
#-*- coding: utf-8 -*-


def load_data(input_file):
    fp = open(input_file)
    data = []
    for line in fp:
        data.append(line.split(","))
    fp.close()
    return data

def output(output_file, pop):
    fp = open(output_file, "w")
    for item in pop:
        fp.write(item[0] + '\t' + item[1] + '\t' + str(item[2]) + '\n')
    fp.close()

def cal_behavior(data):
	result = []
	for i in range(0, len(data)):
		record = data[i];
		if record[2] == '1':
			click = 0
			for j in range(i-1, 0, - 1):
				prev = data[j]
				if prev[2] != '0' or prev[1] != record[1] or prev[0] != record[0] :
					break
				click += 1
			result.append((record[0], record[1], click))

	return result

#计算用户购买率
def cal_userbuyrate(data):
	buyrate = {}
	for record in data:
		user = record[0]
		if user not in buyrate:
			buyrate[user] = [0, 0]
		buyrate[user][1] += 1
		if record[2] == '1':
			buyrate[user][0] += 1

	#min_max normalize
	min_tot = 10000
	max_tot = 0
	min_buy = 10000
	max_buy = 0
	for user in buyrate:
		min_tot = min(min_tot, buyrate[user][1])
		max_tot = max(max_tot, buyrate[user][1])
		min_buy = min(min_buy, buyrate[user][0])
		max_buy = max(max_buy, buyrate[user][0])

	#output buy rate
	fo = open('result/buyrate.txt', 'w')
	alpha = 0.5
	for user in buyrate:
		buy_norm = buyrate[user][0]*1.0/(max_buy - min_buy)
		tot_norm = buyrate[user][1]*1.0/(max_tot - min_tot)
		buyrate_norm = (1 + alpha * alpha) * (buy_norm * tot_norm) / (alpha * alpha * buy_norm + tot_norm)
		fo.write(user + ' ' + str(buyrate_norm) + '\n')
	
	fo.close()

if __name__ == "__main__":
    input_file = '../data/user_brand_date_full.csv'
    output_file = 'result/behavior.txt'
    data = load_data(input_file)
    #result = cal_behavior(data)
    #output(output_file, result)
    cal_userbuyrate(data)