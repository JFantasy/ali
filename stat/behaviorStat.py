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
			

if __name__ == "__main__":
    input_file = '../data/user_brand_date_full.csv'
    output_file = 'result/behavior.txt'
    data = load_data(input_file)
    result = cal_behavior(data)
    output(output_file, result)