#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
from collections import defaultdict as ddict

def load_user_brandlist(input_file):
    f = open(input_file)
    user_brandlist = {}
    for line in f:
        data = line.split()
        user_brandlist[data[0]] = data[1:len(data)]
    f.close()
    return user_brandlist

def load_topk(input_file):
    topk = {}
    f = open(input_file)
    for line in f:
        user, k = line.split(' ')
        topk[user] = int(k)
    f.close()

    return topk

def gen_ans(topk, user_brandlist):
    result = ddict(list)
    for user in user_brandlist:
        k = topk[user]
        if k == 0:
            continue
        result[user] = user_brandlist[user][:k]
    return result

def output(ans_file, result):
    f = open(ans_file, "w")
    for user in result:
        f.write(user + '\t' + result[user][0])
        for i in xrange(1, len(result[user])):
            f.write(',' + result[user][i]);
        f.write('\n')
    f.close()

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "Format Error"
    else:
        topk_file = sys.argv[1]
        sort_matrix_file = sys.argv[2]
        ans_file = sys.argv[3]
        topk = load_topk(topk_file)
        user_brandlist = load_user_brandlist(sort_matrix_file)
        result = gen_ans(topk, user_brandlist)
        output(ans_file, result)
