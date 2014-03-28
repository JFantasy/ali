f = open('ali_order_date.csv')

item_pop = {}
user_buy = {}
for line in f:
	data = line.split(',')
	user = data[0]
	item = data[1]
	rate = data[2]
	
	if item not in item_pop:
		item_pop[item] = 0
	if rate == '1':
		item_pop[item] += 1

	if user not in user_buy:
		user_buy[user] = 0
	if rate == '1':
		user_buy[user] += 1

item_pop_list = []
user_buy_list = []
for (k,v) in item_pop.items():
	item_pop_list.append((k, v));

for (k,v) in user_buy.items():
	user_buy_list.append((k, v));

item_pop_list = sorted(item_pop_list, cmp = lambda x, y : cmp(y[1], x[1]))
user_buy_list = sorted(user_buy_list, cmp = lambda x, y : cmp(y[1], x[1]))

fo = open('item_pop.csv', 'w')
for x in item_pop_list:
	fo.write(str(x[0]) + ',' + str(x[1]) + '\n')
fo.close()

fo = open('user_buy.csv', 'w')
for x in user_buy_list:
	fo.write(str(x[0]) + ',' + str(x[1]) + '\n')
fo.close()

f.close()