#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys, os, datetime

def run_cmd(cmd):
    print "Running: %s" % cmd
    os.system(cmd)

def build_dir():
    date = datetime.datetime.now().strftime("%m%d%H%M%S")
    result_dir = "../ans/%s" % date
    cmd = "mkdir %s" % result_dir
    run_cmd(cmd)
    return result_dir

def process_filter(result_dir, input_file, filter_month):
    filter_input_file = "%s/filter_month.csv" % result_dir
    cmd = "python input_filter.py %s %s %s" % (input_file, filter_input_file,
            " ".join(filter_month))
    run_cmd(cmd)
    return filter_input_file

def process_gen_pop(result_dir, input_file):
    pop_file = "%s/pop.txt" % result_dir
    cmd = "python gen_pop.py %s %s" % (input_file, pop_file)
    run_cmd(cmd)
    return pop_file

def process_gen_like(result_dir, input_file, repeat, dynamic):
    like_file = "%s/like.txt" % result_dir
    cmd = "python gen_like_matrix.py %s %s %s %s" % \
            (input_file, like_file, repeat, dynamic)
    run_cmd(cmd)
    return like_file

def process_sort_pop(result_dir, pop_file, like_file, input_file):
    sort_file = "%s/sort.txt" % result_dir
    cmd = "python sort_pop.py %s %s %s %s" % (pop_file, like_file, \
            input_file, sort_file)
    run_cmd(cmd)
    return sort_file

def process_gen_topk(result_dir, input_file, sort_file, min_topk, max_topk):
    topk_file = "%s/topk.txt" % result_dir
    cmd = "python cal_topk.py %s %s %s %s %s" % (input_file, sort_file, \
            topk_file, str(min_topk), str(max_topk))
    run_cmd(cmd)
    return topk_file

def process_gen_ans(result_dir, topk_file, sort_file):
    ans_file = "%s/submit.txt" % result_dir
    cmd = "python gen_ans.py %s %s %s" % (topk_file, sort_file, ans_file)
    run_cmd(cmd)
    return ans_file


if __name__ == "__main__":
    if len(sys.argv) != 7:
        print "Format Error"
        exit(0)

    result_dir = build_dir()

    original_input_file = sys.argv[1]
    filter_month = sys.argv[2].split(",")
    min_topk = int(sys.argv[3])
    max_topk = int(sys.argv[4])
    repeat = sys.argv[5]
    dynamic = sys.argv[6]

    filter_input_file = process_filter(result_dir, original_input_file, \
            filter_month)
    pop_file = process_gen_pop(result_dir, filter_input_file)
    like_file = process_gen_like(result_dir, filter_input_file, repeat, dynamic)
    sort_file = process_sort_pop(result_dir, pop_file, like_file, \
            filter_input_file)
    topk_file = process_gen_topk(result_dir, filter_input_file, sort_file, \
            min_topk, max_topk)
    ans_file = process_gen_ans(result_dir, topk_file, sort_file)
    print "Finish %s" % ans_file
