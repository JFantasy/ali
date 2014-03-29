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

def load_click(data_file):
    click = {}
    fp = open(data_file)
    for line in fp:
        user, item, rank, month, day = line.split(',')
        if rank != "1":
            if user in click:
                click[user][item] = 1
            else:
                click[user] = {item : 1}
    fp.close()
    return click

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

def gen_matrix(pop, click):
    matrix = {}
    for user in click:
        items = []
        for item in click[user]:
            items.append((pop[item] * like[user][item], item))
        matrix[user] = sorted(items, reverse = True)
    return matrix

def output(output_file, matrix):
    fp = open(output_file, "w")
    for user in matrix:
        fp.write(user + " ")
        for i in range(len(matrix[user])):
            fp.write(matrix[user][i][1] + " ")
        fp.write("\n")
    fp.close()


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print "Format Error"
    else:
        pop_file = sys.argv[1]
        like_file = sys.argv[2]
        data_file = sys.argv[3]
        output_file = sys.argv[4]

        pop = load_pop(pop_file)
        like = load_like(like_file)
        click = load_click(data_file)
        matrix = gen_matrix(pop, click)
        output(output_file, matrix)
