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

def cal_user_activeness(data):
	buycnt = {}
	for r in data:
		user, brand, behavior, month, day = r[0],r[1],int(r[2]),int(r[3]),int(r[4])
		if user not in buycnt:
			buycnt[user] = [0, 0, 0, 0, 0]
		
		buycnt[user][behavior] += 1
		
		buycnt[user][4] += 1
	f = open('result/activeness.txt', 'w')
	for user in buycnt:
		if buycnt[user][1] == 0:
			continue
		f.write(user + '\t' + str(buycnt[user]) + '\n')
	f.close()

if __name__ == "__main__":
    input_file = '../data/user_brand_date_full.csv'
    output_file = 'result/behavior.txt'
    
    data = load_data(input_file)
    cal_user_activeness(data)