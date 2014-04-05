import random
import json
from time import time

from gen_pop import cal_pop
from gen_like_matrix import cal_like
from sort_pop import gen_matrix
from cal_topk import cal_topK
from gen_ans import gen_ans
from gen_bonus import cal_bonus

from collections import defaultdict as ddict



def load_test(month):
    path = "../data/ali_order_brand_date_full.csv"
    test = ddict(list)
    with file(path) as f:
        for line in f:
            elements = line.strip().split(',')
            if int(elements[4]) != month: continue
            if elements[2] != '1': continue
            uid = elements[0]
            bid = elements[1]
            test[uid].append(bid)
    return test

def load_data(period):
    path = "../data/ali_order_brand_date_full.csv"
    result = []
    fin = open(path)
    for line in fin:
        user, item, rank, month, day = line.strip().split(",")
        if not month in period:
            continue
        month = str(4 + int(month) - int(max(period)))
        result.append((user, item, rank, month, day))
    return result

def filter_action(data):
    action = {}
    for line in data:
        user, item, rank, month, day = line
        if rank != "1":
            if user in action:
                action[user][item] = 1
            else:
                action[user] = {item : 1}
    return action

def evaluate(test, predict):
    hitBrand = 0
    pBrand = 0
    for uid in predict:
        pBrand += len(predict[uid])
        hitBrand += len(set(predict[uid]) & set(test[uid]))
    P = 1.0*hitBrand/pBrand

    hitBrand = 0
    bBrand = 0
    for uid in test:
        bBrand += len(test[uid])
        hitBrand += len(set(predict[uid]) & set(test[uid]))
    R = 1.0*hitBrand/bBrand
    F1 = 2*P*R/(P+R) if (P+R)!=0 else 0
    return F1

def generate_parameters():
    l1 = random.randint(1, 100)/100.0
    l2 = random.randint(1, 100)/100.0
    l3 = random.randint(1, 100)/100.0
    l4 = random.randint(1, 100)/100.0
    return (l1, l2, l3, l4)

def cal_best(test, period, MaxTime, Keep):
    result = []
    random.seed(time())
    for _ in xrange(MaxTime):
        p = generate_parameters()
        predict = cal_predict(period, p)
        F1 = evaluate(test, predict)
        if(len(result) < Keep):
            result.append((F1, p))
        else:
            result.append((F1, p))
            result = sorted()[1:]
    return result

def cal_predict(period, p):
    conf_file = file("config.json")
    config = json.load(conf_file)
    conf_file.close()

    filter_pop_month = map(lambda x: str(x), period)
    filter_like_month = map(lambda x: str(x), period)
    min_topk = config["min_topk"]
    max_topk = config["max_topk"]
    repeat = config["repeat"]
    dynamic = config["dynamic"]
    decay = config["decay"]
    bonus = config["bonus"]
    month_score = config["month_score"]
    rank_score = config["rank_score"]

    filtered_pop_input_data = load_data(filter_pop_month)
    filtered_like_input_data = load_data(filter_like_month)
    action_data = filter_action(filtered_like_input_data)
    pop_data = cal_pop(filtered_pop_input_data, [0.2, 0.4, 0.6, 0.8, 1.0], p)
    bonus_data = cal_bonus(filtered_like_input_data, bonus)
    like_data = cal_like(filtered_like_input_data, repeat, dynamic, decay, p)
    sort_data = gen_matrix(pop_data, like_data, action_data, bonus_data)
    topk_data = cal_topK(filtered_like_input_data, sort_data, min_topk, max_topk)
    ans_data = gen_ans(topk_data, sort_data)
    return ans_data

if __name__ == "__main__":
    MAXTIME = 1
    MAINTAIN = 20
    test = load_test(7)
    best_results1 = cal_best(test, [4,5,6], MAXTIME, MAINTAIN)

    test = load_test(8)
    best_results2 = cal_best(test, [5,6,7], MAXTIME, MAINTAIN)
    best_results3 = cal_best(test, [4,5,6,7], MAXTIME, MAINTAIN)
    with file("rank_score.txt", "w") as f: 
        f.write("####################\n4,5,6 -> 7\n####################\n")
        for result in best_results1:
            f.write("%.3f\t%5.2f %5.2f %5.2f %5.2f\n" % \
            (result[0], result[1][0], result[1][1], result[1][2], result[1][3]))
        f.write("\n\n\n")
        f.write("####################\n5,6,7 -> 8\n####################\n")
        for result in best_results2:
            f.write("%.3f\t%5.2f %5.2f %5.2f %5.2f\n" % \
            (result[0], result[1][0], result[1][1], result[1][2], result[1][3]))
        f.write("\n\n\n")
        f.write("####################\n4,5,6,7 -> 8\n####################\n")
        for result in best_results3:
            f.write("%.3f\t%5.2f %5.2f %5.2f %5.2f\n" % \
            (result[0], result[1][0], result[1][1], result[1][2], result[1][3]))

