#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys

def load_data(input_file):
    fp = open(input_file)
    data = []
    for line in fp:
        data.append(line.strip().split(","))
    fp.close()

def get_filter(data):
    pass

def output(output_file, filter_items):
    fp = open(output_file, "w")
    fp.write('\n'.join(filter_items))
    fp.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Format Error"
        exit(0)
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    data = load_data(input_file)
    filter_items = get_filter(data)
    output(output_file, filter_items)
