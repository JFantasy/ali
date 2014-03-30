#!/usr/bin/python
#-*- coding: utf-8 -*-
import sys
from collections import defaultdict as ddict

def load_data(path):
    predict = ddict(list)
    with file(path) as f:
        for line in f:
            elements = line.strip().split('\t')
            uid = int(elements[0])
            predict[uid] = map(lambda x: int(x), elements[1].split(','))
    return predict

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
    print "F1=%f\nP=%f\nR=%f\n" % (F1, P, R)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: %s base_data predict_data\n" % sys.argv[0]
        exit(0)
    base = load_data(sys.argv[1])
    predict = load_data(sys.argv[2])
    evaluate(base, predict)
