from input_filter import input_filter
from gen_pop import cal_pop
from gen_like_matrix import cal_like
from sort_pop2 import gen_matrix
from cal_topk import cal_topK
from gen_ans import gen_ans



def load_test(path):
    test = ddict(list)
    with file(path) as f:
        for line in f:
            elements = line.strip().split(',')
            if elements[2] != '1': continue
            uid = int(elements[0])
            bid = int(elements[1])
            test[uid].append(bid)
    return test

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

def cal_best(MaxTime, Keep):
    result = []
    for _ in xrange(MaxTime):
        ######
        #
        ######
        if(len(result) < Keep):
            result.append((F1, (p1, p2, p3, p4)))
        else:
            result.append((F1, (p1, p2, p3, p4)))
            result = sorted()[1:]
    return result


if __name__ == "__main__":
    test_data = load_test("../data/ali_order_brand_date_test.csv")
    input_file = "../data/ali_order_brand_date_train.csv"
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
    month_score = config["month_score"]
    rank_score = config["rank_score"]

    date = datetime.datetime.now().strftime("%m-%d.%H:%M:%S")
    submit_name = "../ans/%s_%s_%s_%d_%d_%s_%s_%s" % (date, \
            "".join(filter_pop_month), "".join(filter_like_month), \
            min_topk, max_topk, repeat, dynamic, decay)

    result_dir = build_dir()
    filtered_pop_input_data = input_filter(input_file, filter_pop_month)
    filtered_like_input_data = input_filter(input_file, filter_like_month)
    pop_data = cal_pop(filtered_pop_input_data)
    like_data = cal_like(filtered_like_input_data, repeat, dynamic, decay)
    sort_data = gen_matrix(pop_data, like_data, filtered_like_input_data)
    topk_data = cal_topK(filtered_like_input_data, sort_data, min_topk, max_topk)
    ans_data = gen_ans(topk_data, sort_data)

    print "Finish %s" % submit_name
