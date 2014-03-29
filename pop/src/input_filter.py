#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys

def output(input_file, output_file, months):
    fin = open(input_file)
    fout = open(output_file, "w")
    for line in fin:
        user, item, rank, month, day = line.split(",")
        if not month in months:
            continue
        fout.write(line)
    fout.close()
    fin.close()

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "Format Error"
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        months = sys.argv[3:len(sys.argv)]
        output(input_file, output_file, months)
