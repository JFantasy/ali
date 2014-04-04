#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys, collections

def load_pop(pop_file):
    pop = {}
    fp = open(pop_file)
    for line in fp:
        item, score = line.split()
        pop[item] = float(score)
    fp.close()
    return pop

def load_action(data_file):
    action = {}
    fp = open(data_file)
    for line in fp:
        user, item, rank, month, day = line.split(',')
        if rank != "1":
            if user in action:
                action[user][item] = 1
            else:
                action[user] = {item : 1}
    fp.close()
    return action

def load_like(like_file):
    like = collections.defaultdict(lambda: collections.defaultdict(float))
    fp = open(like_file)
    for line in fp:
        user = line.split()[0]
        items = line.split()[1].split(",")
        for record in items:
            item, score = record.split(":")
            like[user][item] = float(score)
    fp.close()
    return like

def load_bonus(bonus_file):
    bonus = collections.defaultdict(lambda: collections.defaultdict(int))
    fp = open(bonus_file)
    for line in fp:
        user, item = line.split()[0], line.split()[1]
        bonus[user][item] = int(line.split()[2])
    fp.close()
    return bonus

def check_bonus(matrix, bonus):
    all_item = sum([min(7, len(matrix[user])) for user in matrix])
    total = 0
    for user in matrix:
        for i in range(min(7, len(matrix[user]))):
            item = matrix[user][i][1]
            total += 1 if bonus[user][item] > 0 else 0

def gen_matrix(pop, like, action, bonus):
    matrix = {}
    for user in action:
        items = []
        bias = sum([pop[item] * like[user][item] for item in action[user]]) * 0.02
        for item in action[user]:
            items.append((pop[item] * like[user][item] + \
                    bonus[user][item] * bias, item))
        matrix[user] = map(lambda x: x[1], sorted(items, reverse = True))
    return matrix

def output(output_file, matrix):
    fp = open(output_file, "w")
    for user in matrix:
        fp.write(user + " ")
        for i in range(len(matrix[user])):
            fp.write(matrix[user][i] + " ")
        fp.write("\n")
    fp.close()


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print "Format Error"
    else:
        pop_file = sys.argv[1]
        like_file = sys.argv[2]
        bonus_file = sys.argv[3]
        data_file = sys.argv[4]
        output_file = sys.argv[5]

        pop = load_pop(pop_file)
        like = load_like(like_file)
        action = load_action(data_file)
        bonus = load_bonus(bonus_file)
        matrix = gen_matrix(pop, like, action, bonus)
        output(output_file, matrix)
