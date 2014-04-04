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

def get_month_score(month, score):
    return score[int(month)]

def get_rank_score(rank, score):
    return score[int(rank)]

def normalization(pop):
    score_sum = 0.0
    for item in pop:
        score_sum += pop[item]
    for item in pop:
        pop[item] /= score_sum

def cal_pop(data, month_score = [0.2, 0.4, 0.6, 0.8, 1.0], 
                  rank_score = [0.25, 1.0, 0.5, 0.75]):
    pop = {}
    for record in data:
        pop[record[1]] = 0.0
    for record in data:
        pop[record[1]] += get_month_score(record[3], month_score) * \
                get_rank_score(record[2], rank_score)
    normalization(pop)
    return pop

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print 'Format Error'
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        data = load_data(input_file)
        month_score = [0.2, 0.4, 0.6, 0.8, 1.0]
        rank_score = [0.25, 1.0, 0.5, 0.75]
        if len(sys.argv) == 5:
            month_score = map(lambda x: float(x), sys.argv[3].strip().split(','))
            rank_score = map(lambda x: float(x), sys.argv[4].strip().split(','))
        pop = cal_pop(data, month_score, rank_score)
        output(output_file, pop)
