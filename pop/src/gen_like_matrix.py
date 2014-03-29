#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys, collections

def load_data(input_file):
    data = []
    fp = open(input_file)
    for line in fp:
        user, item, rank, month, day = line.split(",")
        data.append((user, item, rank))
    fp.close()
    return data

def get_rank_score(rank):
    score = [0.2, 1.0, 0.5, 0.8]
    return score[int(rank) - 1]

def construct():
    return collections.defaultdict(float)

def cal_like(data):
    matrix = collections.defaultdict(lambda:collections.defaultdict(float))
    for record in data:
        user, item, rank = record
        matrix[user][item] += get_rank_score(rank)
    return matrix

def normalization(matrix):
    for user in matrix:
        sum_score = sum(matrix[user].values()) 
        for item in matrix[user]:
            matrix[user][item] /= sum_score

def output(output_file, matrix):
    fp = open(output_file, "w")
    for user in matrix:
        fp.write(user + ' ')
        items = matrix[user].items()
        line = ["%s:%s" % (str(item[0]), str(item[1])) for item in items]
        fp.write(",".join(line) + "\n")
    fp.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Format Error"
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        data = load_data(input_file)
        matrix = cal_like(data)
        normalization(matrix)
        output(output_file, matrix)
