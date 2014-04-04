#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys, collections

def cal_time(month, day):
    months = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return sum(months[0:int(month)]) + int(day)

def load_data(input_file):
    data = []
    fp = open(input_file)
    for line in fp:
        user, item, rank, month, day = line.strip().split(",")
        data.append((user, item, rank, month, day))
    fp.close()
    return data

def get_rank_score(rank, score):
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

def cal_decay(day, most_recent_day):
    return 0.99 ** (most_recent_day - day)

def cal_like(data, repeat_buy, dynamic, rank_score, decay):
    matrix = collections.defaultdict(lambda:collections.defaultdict(float))
    buy = collections.defaultdict(lambda:collections.defaultdict(int))
    action = collections.defaultdict(lambda:collections.defaultdict(int))
    most_recent_day = max([cal_time(item[3], item[4]) for item in data])

    for record in data:
        user, item, rank, month, day = record
        buy[user][item] += 1 if rank == "1" else 0
        action[user][rank] += 1

    for record in data:
        user, item, rank, month, day = record
        day = cal_time(month, day)
        gain = get_rank_score(rank, rank_score) * \
                (1.0 if dynamic == "0" or rank == "1" \
                else cal_dynamic(action[user][rank])) * \
                (1.0 if decay == "0" else cal_decay(day, most_recent_day))
        matrix[user][item] += gain

    if repeat_buy == "1":
        cal_repeat(buy, matrix)
    normalization(matrix)
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
    if len(sys.argv) < 6:
        print "Format Error"
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        repeat_buy = sys.argv[3]
        dynamic = sys.argv[4]
        decay = sys.argv[5]

        data = load_data(input_file)
        rank_score = [0.2, 1.0, 0.5, 0.8]
        if len(sys.argv) == 7:
            rank_score = map(lambda x: float(x), sys.argv[6].strip().split(','))
        matrix = cal_like(data, repeat_buy, dynamic, rank_score, decay)
        output(output_file, matrix)
