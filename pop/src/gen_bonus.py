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
        data.append((user, item, rank, cal_time(month, day)))
    fp.close()
    return data

def cal_bonus(data, bonus_day):
    bonus = collections.defaultdict(lambda: collections.defaultdict(int))
    most_recent_day = max([item[3] for item in data])
    for record in data:
        if most_recent_day - int(record[3]) < bonus_day:
            user, item = record[0], record[1]
            bonus[user][item] += 1
    return bonus

def output(output_file, bonus):
    fp = open(output_file, "w")
    for user in bonus:
        for item in bonus[user]:
            fp.write("%s %s %d\n" % (user, item, bonus[user][item]))
    fp.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "Format Error"
        exit(0)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    bonus_day = int(sys.argv[3])

    data = load_data(input_file)
    bonus = cal_bonus(data, bonus_day)
    output(output_file, bonus)
