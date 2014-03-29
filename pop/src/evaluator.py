#!/usr/bin/python
#-*- coding: utf-8 -*-

def load_base(path):
    base = collections.defaultdict(list)
    with file(path) as f:
        for line in f:
            elements = line.strip().split(',')
            if elements[2] != '1':
                continue
            uid = int(elements[0])
            bid = int(elements[1])
            base[uid].append(bid)
    return base

def load_predict(path):
    predict = dict()
    with file(path) as f:
        for line in f:
            elements = line.strip().split(' ')
            uid = int(elements[0])
            predict[uid] = map(lambda x: int(x), elements[1].split(','))
    return predict

def evaluate(base, predict):
    hitBrand = 0
    pBrand = 0
    for uid in predict:
        pBrand += len(predict[uid])
        hitBrand += len(set(predict[uid]) & set(base[uid]))
    P = 1.0*hitBrand/pBrand

    hitBrand = 0
    bBrand = 0
    for uid in base:
        bBrand += len(base[uid])
        hitBrand += len(set(predict[uid]) & set(base[uid]))
    R = 1.0*hitBrand/bBrand

    F1 = 2*P*R/(P+R)
    print "F1=%f\nP=%f\nR=%f\n" % (F1, P, R)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: %s raw_train_data output_test_data\n" % sys.argv[0]
        return 0
    base = load_base(sys.argv[1])
    predict = load_predict(sys.argv[2])
    evaluate(base, predict)
