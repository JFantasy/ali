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
    return score[int(rank)]

def cal_repeat(buy, matrix):
    for user in buy:
        for item in buy[user]:
            if buy[user][item] == 1:
                matrix[user][item] -= 0.4
            elif buy[user][item] > 2:
                matrix[user][item] += buy[user][item]

def cal_dynamic(action):
    return max(0.97 ** (action - 1), 0.4)

def cal_like(data, repeat_buy, dynamic):
    matrix = collections.defaultdict(lambda:collections.defaultdict(float))
    buy = collections.defaultdict(lambda:collections.defaultdict(int))
    action = collections.defaultdict(lambda:collections.defaultdict(int))

    for record in data:
        user, item, rank = record
        buy[user][item] += 1 if rank == "1" else 0
        action[user][rank] += 1

    for record in data:
        user, item, rank = record
        gain = get_rank_score(rank) * (1.0 if dynamic == "0" or rank == "1" \
                else cal_dynamic(action[user][rank]))
        matrix[user][item] += gain

    if repeat_buy == "1":
        cal_repeat(buy, matrix)
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
    if len(sys.argv) < 5:
        print "Format Error"
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        repeat_buy = sys.argv[3]
        dynamic = sys.argv[4]

        data = load_data(input_file)
        matrix = cal_like(data, repeat_buy, dynamic)
        normalization(matrix)
        output(output_file, matrix)
