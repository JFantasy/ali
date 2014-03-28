#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys

def load_data(input_file):
    fp = open(input_file)
    data = []
    for line in fp:
        data.append(lint.split(","))
    fp.close()

def output(output_file, pop):
    fp = open(output_file, pop)
    for item in pop:
        fp.write(item + str(pop[item]) + '\n')
    fp.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print 'Format Error'
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        data = load_data(input_file)
        pop = cal_pop(data)
        output(output_file, pop)
