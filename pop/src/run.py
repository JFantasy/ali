#/usr/bin/python
#-*- coding: utf-8 -*-

import sys, os, datetime, json

def run_cmd(cmd):
    print "Running: %s" % cmd
    os.system(cmd)

def build_dir():
    result_dir = "../ans/tmp"
    cmd = "mkdir %s" % result_dir
    run_cmd(cmd)
    return result_dir

def process_filter(result_dir, input_file, filter_month, filter_type):
    filter_input_file = "%s/filter_%s_month.csv" % (result_dir, filter_type)
    cmd = "python input_filter.py %s %s %s" % (input_file, filter_input_file,
            " ".join(filter_month))
    run_cmd(cmd)
    return filter_input_file

def process_gen_pop(result_dir, input_file):
    pop_file = "%s/pop.txt" % result_dir
    cmd = "python gen_pop.py %s %s" % (input_file, pop_file)
    run_cmd(cmd)
    return pop_file

def process_gen_like(result_dir, input_file, repeat, dynamic, decay):
    like_file = "%s/like.txt" % result_dir
    cmd = "python gen_like_matrix.py %s %s %s %s %s" % \
            (input_file, like_file, repeat, dynamic, decay)
    run_cmd(cmd)
    return like_file

def process_gen_bonus(result_dir, input_file, bonus):
    bonus_file = "%s/bonus.txt" % result_dir
    cmd = "python gen_bonus.py %s %s %s" % (input_file, bonus_file, bonus)
    run_cmd(cmd)
    return bonus_file

def process_sort_pop(result_dir, pop_file, like_file, bonus_file, input_file):
    sort_file = "%s/sort.txt" % result_dir
    cmd = "python sort_pop.py %s %s %s %s %s" % (pop_file, like_file, \
            bonus_file, input_file, sort_file)
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

def clear_files(result_dir, ans_file, submit_path):
    submit_file = submit_path + \
            '/'+ submit_path[submit_path.find('_')+1:] + '.txt'
    cmd = "mkdir %s; mv %s %s" % (submit_path, ans_file, submit_file)
    run_cmd(cmd)
    cmd = "cp config.json %s" % (submit_path+'/')
    run_cmd(cmd)
    cmd = "rm -rf %s" % result_dir
    run_cmd(cmd)

if __name__ == "__main__":
    original_input_file = "../data/ali_order_brand_date_full.csv"
    conf_file = file("config.json")
    config = json.load(conf_file)
    conf_file.close()

    filter_pop_month = map(lambda x: str(x), config["pop_month"])
    filter_like_month = map(lambda x: str(x), config["like_month"])
    min_topk = config["min_topk"]
    max_topk = config["max_topk"]
    repeat = config["repeat"]
    dynamic = config["dynamic"]
    decay = config["decay"]
    bonus = config["bonus"]
    month_score = config["month_score"]
    rank_score = config["rank_score"]

    date = datetime.datetime.now().strftime("%m-%d.%H:%M:%S")
    submit_name = "../ans/%s_%s_%s_%d_%d_%s_%s_%s_%s" % (date, \
            "".join(filter_pop_month), "".join(filter_like_month), \
            min_topk, max_topk, repeat, dynamic, decay, bonus)

    result_dir = build_dir()

    filter_pop_input_file = process_filter(result_dir, original_input_file, \
            filter_pop_month, "pop")
    filter_like_input_file = process_filter(result_dir, original_input_file, \
            filter_like_month, "like")
    pop_file = process_gen_pop(result_dir, filter_pop_input_file)
    like_file = process_gen_like(result_dir, filter_like_input_file, repeat, \
            dynamic, decay)
    bonus_file = process_gen_bonus(result_dir, filter_like_input_file, bonus)
    sort_file = process_sort_pop(result_dir, pop_file, like_file, bonus_file, \
            filter_like_input_file)
    topk_file = process_gen_topk(result_dir, filter_like_input_file, \
            sort_file, min_topk, max_topk)
    ans_file = process_gen_ans(result_dir, topk_file, sort_file)

    clear_files(result_dir, ans_file, submit_name)

    print "Finish %s" % submit_name
