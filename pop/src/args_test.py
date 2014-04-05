import random
import json
from time import time

from input_filter import input_filter
from gen_pop import cal_pop
from gen_like_matrix import cal_like
from sort_pop import gen_matrix
from cal_topk import cal_topK
from gen_ans import gen_ans
from gen_bonus import cal_bonus



def load_test():
    path = "../data/ali_order_brand_date_test.csv"
    test = ddict(list)
    with file(path) as f:
        for line in f:
            elements = line.strip().split(',')
            if elements[2] != '1': continue
            uid = int(elements[0])
            bid = int(elements[1])
            test[uid].append(bid)
    return test

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
    F1 = 2*P*R/(P+R)
    return F1

def generate_parameters():
    l1 = random.randint(1, 100)/100.0
    l2 = random.randint(1, 100)/100.0
    l3 = random.randint(1, 100)/100.0
    l4 = random.randint(1, 100)/100.0
    return (l1, l2, l3, l4)

def cal_best(test, MaxTime, Keep):
    result = []
    random.seed(time())
    for _ in xrange(MaxTime):
        p = generate_parameters()
        predict = cal_predict(p)
        F1 = evaluate(test, predict)
        if(len(result) < Keep):
            result.append((F1, p))
        else:
            result.append((F1, p))
            result = sorted()[1:]
    return result

def cal_predict(p):
    input_file = "../data/ali_order_brand_date_full.csv"
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

    filtered_pop_input_data = input_filter(input_file, filter_pop_month)
    filtered_like_input_data = input_filter(input_file, filter_like_month)
    action_data = filter_action(filtered_like_input_data)
    pop_data = cal_pop(filtered_pop_input_data)
    bonus_data = cal_bonus(filtered_like_input_data, bonus)
    like_data = cal_like(filtered_like_input_data, repeat, dynamic, decay)
    sort_data = gen_matrix(pop_data, like_data, action_data, bonus_data)
    topk_data = cal_topK(filtered_like_input_data, sort_data, min_topk, max_topk)
    ans_data = gen_ans(topk_data, sort_data)
    return ans_data

if __name__ == "__main__":
    test = load_test()
    best_results = cal_best(test, 100000, 20)
    for result in best_results:
        print "%.3f\t%5f %5f %5f %5f\n" % \
        (result[0], result[1][0], result[1][1], result[1][2], result[1][3])