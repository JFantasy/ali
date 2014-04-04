#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys

def input_filter(input_file, months):
    result = []
    fin = open(input_file)
    for line in fin:
        user, item, rank, month, day = line.strip().split(",")
        if not month in months:
            continue
        month = str(4 + int(month) - int(max(months)))
        result.append([user, item, rank, month, day])
    return result

def output(input_file, output_file, months):
    fin = open(input_file)
    fout = open(output_file, "w")
    for line in fin:
        user, item, rank, month, day = line.strip().split(",")
        if not month in months:
            continue
        month = str(4 + int(month) - int(max(months)))
        fout.write("%s,%s,%s,%s,%s\n" % (user, item, rank, month, day))
    fout.close()
    fin.close()

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "Format Error"
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        months = sys.argv[3:]
        output(input_file, output_file, months)
