#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys

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
        fp.write(item + ' ' + str(pop[item]) + '\n')
    fp.close()

def get_score(month):
    score = [0.2, 0.4, 0.6, 0.8, 1.0]
    rank = int(month) - 4
    return score[rank]

def normalization(pop):
    score_sum = 0.0
    for item in pop:
        score_sum += pop[item]
    for item in pop:
        pop[item] /= score_sum

def cal_pop(data):
    pop = {}
    month = {}
    for record in data:
        if record[2] != "1":
            continue
        month[record[3]] = 1
        if record[1] in pop:
            pop[record[1]] += get_score(record[3])
        else:
            pop[record[1]] = get_score(record[3])

    normalization(pop)
    return pop

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print 'Format Error'
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        data = load_data(input_file)
        pop = cal_pop(data)
        output(output_file, pop)
